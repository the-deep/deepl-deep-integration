import os
import boto3
from botocore.exceptions import ClientError
import json
from enum import Enum

DEFAULT_AWS_REGION = "us-east-1"

AWS_REGION = os.environ.get("AWS_REGION", DEFAULT_AWS_REGION)
PREDICTION_QUEUE_NAME = os.environ.get("PREDICTION_QUEUE")
ENDPOINT_NAME_MODEL = os.environ.get("EP_NAME_MODEL")

sqs_client = boto3.client('sqs', region_name=AWS_REGION)

sagemaker_rt = boto3.client("runtime.sagemaker", region_name="us-east-1")  # todo: update the region later.


class PredictionStatus(Enum):
    FAILED = 0
    SUCCESS = 1


def send_message2sqs(
    entry_id,
    entry,
    predictions,
    callback_url,
    prediction_status
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


def get_predictions(entry):
    data = {
        "columns": ["excerpt"],
        "index": [0],
        "data": [entry]
    }
    try:
        response = sagemaker_rt.invoke_endpoint(
            EndpointName=ENDPOINT_NAME_MODEL,
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

    for record in records:
        entry_id = record['body']
        entry = record['messageAttributes']['entry']['stringValue']
        callback_url = record['messageAttributes']['callback_url']['stringValue']
        print(f"Processing entry id {entry_id}")

        predictions, prediction_status = get_predictions(entry)

        sqs_message = {
            'entry_id': entry_id,
            'entry': entry,
            'predictions': predictions,
            'callback_url': callback_url,
            'prediction_status': prediction_status
        }
        send_message2sqs(**sqs_message)
