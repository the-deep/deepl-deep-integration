import os
import boto3
from botocore.exceptions import ClientError
import json
from enum import Enum
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from postprocess_raw_preds import get_predictions_all, get_clean_thresholds, get_clean_ratios

logging.getLogger().setLevel(logging.INFO)

DEFAULT_AWS_REGION = "us-east-1"

AWS_REGION = os.environ.get("AWS_REGION", DEFAULT_AWS_REGION)
PREDICTION_QUEUE_NAME = os.environ.get("PREDICTION_QUEUE")
MODEL_ENDPOINT_NAME = os.environ.get("MODEL_ENDPOINT_NAME")
GEOLOCATION_FN_NAME = os.environ.get("GEOLOCATION_FN_NAME")
RELIABILITY_FN_NAME = os.environ.get("RELIABILITY_FN_NAME")
MODEL_INFO_FN_NAME = os.environ.get("MODEL_INFO_FN_NAME")

sqs_client = boto3.client('sqs', region_name=AWS_REGION)

sagemaker_rt = boto3.client("runtime.sagemaker", region_name="us-east-1")  # todo: update the region later.
geolocation_client = boto3.client("lambda", region_name="us-east-1")
reliability_client = boto3.client("lambda", region_name="us-east-1")
model_info_client = boto3.client("lambda", region_name=AWS_REGION)


class PredictionStatus(Enum):
    FAILED = 0
    SUCCESS = 1


def send_message2sqs(
    entry_id,
    entry,
    pred_tags,
    pred_thresholds,
    tags_selected,
    callback_url,
    prediction_status,
    geolocations,
    reliability_score,
    model_info
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
    if pred_tags:
        message_attributes['pred_tags'] = {
            'DataType': 'String',
            'StringValue': json.dumps(pred_tags)
        }
    if pred_thresholds:
        message_attributes['pred_thresholds'] = {
            'DataType': 'String',
            'StringValue': json.dumps(pred_thresholds)
        }
    if tags_selected:
        message_attributes['tags_selected'] = {
            'DataType': 'String',
            'StringValue': json.dumps(tags_selected)
        }
    message_attributes['geolocations'] = {
        'DataType': 'String',
        'StringValue': json.dumps(geolocations)
    }
    message_attributes['reliability_score'] = {
        'DataType': 'String',
        'StringValue': reliability_score if reliability_score.strip() else " "
    }
    message_attributes['model_info'] = {
        'DataType': 'String',
        'StringValue': json.dumps(model_info)
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
        logging.error("Message not sent to the processed SQS.")


def get_geolocations(entry):
    try:
        response = geolocation_client.invoke(
            FunctionName=GEOLOCATION_FN_NAME,
            Payload=json.dumps({'entry': entry})
        )
        json_response = response['Payload'].read().decode("utf-8")
        return {'locations': json.loads(json_response)['locations']}
    except ClientError as error:
        logging.error(f"Error occurred while fetching geolocations {error}. Returning empty list.")
        return {'locations': []}


def get_reliability_score(publishing_org, authoring_org):
    try:
        response = reliability_client.invoke(
            FunctionName=RELIABILITY_FN_NAME,
            Payload=json.dumps({
                "publishing_organization": publishing_org,
                "authoring_organization": authoring_org
            })
        )
        json_response = response["Payload"].read().decode("utf-8")
        return {
            "score": json.loads(json_response)["prediction"]
        }
    except ClientError as error:
        logging.error(f"Error occurred while fetching reliablity score {error}")
        return {"score": ""}


def get_model_info():
    try:
        response = model_info_client.invoke(
            FunctionName=MODEL_INFO_FN_NAME
        )
        json_response = response["Payload"].read().decode("utf-8")
        return json.loads(json_response)["body"]

    except ClientError as error:
        logging.error(f"Error occurred while fetching model info {error}")
        return {}


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
        pred_tags = get_clean_ratios(pred_response['raw_predictions'])
        pred_thresholds = get_clean_thresholds(pred_response['thresholds'])
        tags_selected = get_predictions_all(pred_response['raw_predictions'])
        prediction_status = PredictionStatus.SUCCESS.value
    except ClientError as error:
        logging.error(f"Error occurred while getting predictions: {error}")
        pred_response = None
        prediction_status = PredictionStatus.FAILED.value

    return pred_tags, pred_thresholds, tags_selected, str(prediction_status)


def predict_entry_handler(event, context):
    records = event['Records']

    geolocations = []
    for record in records:
        entry_id = record['body']
        entry = record['messageAttributes']['entry']['stringValue']
        publishing_organization = record['messageAttributes']['publishing_organization']['stringValue']
        authoring_organization = json.loads(record['messageAttributes']['authoring_organization']['stringValue'])
        callback_url = record['messageAttributes']['callback_url']['stringValue']
        logging.info(f"Processing entry id {entry_id}")

        with ThreadPoolExecutor(max_workers=5) as executor:
            futs = []
            futs.append(executor.submit(get_predictions, entry=entry))
            futs.append(executor.submit(get_geolocations, entry=entry))
            futs.append(executor.submit(get_reliability_score,
                                        publishing_org=publishing_organization,
                                        authoring_org=authoring_organization))

            results = [fut.result() for fut in as_completed(futs)]

        for result in results:
            if type(result) == dict:
                if 'locations' in result:
                    geolocations = result['locations']
                if 'score' in result:
                    reliability_score = result['score']
            elif type(result) == tuple:
                pred_tags, pred_thresholds, tags_selected, prediction_status = result

        sqs_message = {
            'entry_id': entry_id,
            'entry': entry,
            'pred_tags': pred_tags,
            'pred_thresholds': pred_thresholds,
            'tags_selected': tags_selected,
            'callback_url': callback_url,
            'prediction_status': prediction_status,
            'geolocations': geolocations,
            'reliability_score': reliability_score,
            'model_info': get_model_info()
        }
        send_message2sqs(**sqs_message)
