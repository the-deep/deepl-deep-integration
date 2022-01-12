import os
import boto3
from botocore.exceptions import ClientError
import json
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed

DEFAULT_AWS_REGION = "us-east-1"

AWS_REGION = os.environ.get("AWS_REGION", DEFAULT_AWS_REGION)
PREDICTION_QUEUE_NAME = os.environ.get("PREDICTION_QUEUE")
MODEL_ENDPOINT_NAME = os.environ.get("MODEL_ENDPOINT_NAME")
GEOLOCATION_FN_NAME = os.environ.get("GEOLOCATION_FN_NAME")

sqs_client = boto3.client('sqs', region_name=AWS_REGION)

sagemaker_rt = boto3.client("runtime.sagemaker", region_name="us-east-1")  # todo: update the region later.
geolocation_client = boto3.client("lambda", region_name="us-east-1")


class PredictionStatus(Enum):
    FAILED = 0
    SUCCESS = 1


def send_message2sqs(
    entry_id,
    entry,
    predictions,
    callback_url,
    prediction_status,
    geolocations
):
    message_attributes = {}
    message_attributes['entry'] = {
        'DataType': 'String',
        'StringValue': entry
    }
    message_attributes['prediction_status'] = {
        'DataType': 'Number',
        'StringValue': prediction_status
    }
    if predictions:
        message_attributes['predictions'] = {
            'DataType': 'String',
            'StringValue': json.dumps(predictions)
        }
    message_attributes['geolocations'] = {
        'DataType': 'String',
        'StringValue': json.dumps(geolocations)
    }
    if callback_url:
        message_attributes['callback_url'] = {
            'DataType': 'String',
            'StringValue': callback_url
        }

    if PREDICTION_QUEUE_NAME:
        sqs_client.send_message(
            QueueUrl=PREDICTION_QUEUE_NAME,
            MessageBody=entry_id,
            DelaySeconds=0,
            MessageAttributes=message_attributes
        )
    else:
        print("Message not sent to the processed SQS.")


def get_geolocations(entry):
    try:
        response = geolocation_client.invoke(
            FunctionName=GEOLOCATION_FN_NAME,
            Payload=json.dumps({'entry': entry})
        )
        json_response = response['Payload'].read().decode("utf-8")
        return {'locations': json.loads(json_response)['locations']}
    except ClientError as error:
        print(f"Error occurred while fetching geolocations {error}. Returning empty list.")
        return {'locations': []}


def get_predictions(entry):
    data = {
        "columns": ["excerpt", "return_type"],
        "index": [0],
        "data": [[entry, "all_models"]]
    }
    try:
        response = sagemaker_rt.invoke_endpoint(
            EndpointName=MODEL_ENDPOINT_NAME,
            ContentType="application/json; format=pandas-split",
            Body=json.dumps(data)
        )
        pred_response = json.loads(response["Body"].read().decode("ascii"))
        prediction_status = PredictionStatus.SUCCESS.value
    except ClientError as error:
        print(f"Error occurred: {error}")
        pred_response = None
        prediction_status = PredictionStatus.FAILED.value

    return pred_response, str(prediction_status)


def predict_entry_handler(event, context):
    records = event['Records']

    geolocations = []
    for record in records:
        entry_id = record['body']
        entry = record['messageAttributes']['entry']['stringValue']
        callback_url = record['messageAttributes']['callback_url']['stringValue']
        print(f"Processing entry id {entry_id}")

        with ThreadPoolExecutor(max_workers=5) as executor:
            futs = []
            futs.append(executor.submit(get_predictions, entry=entry))
            futs.append(executor.submit(get_geolocations, entry=entry))

            results = [fut.result() for fut in as_completed(futs)]

        for result in results:
            if type(result) == dict:
                if 'locations' in result:
                    geolocations = result['locations']
            elif type(result) == tuple:
                predictions, prediction_status = result

        sqs_message = {
            'entry_id': entry_id,
            'entry': entry,
            'predictions': predictions,
            'callback_url': callback_url,
            'prediction_status': prediction_status,
            'geolocations': geolocations
        }
        send_message2sqs(**sqs_message)
