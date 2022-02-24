import os
import json
import boto3
import logging

logging.getLogger().setLevel(logging.INFO)

SQS_MSG_DELAY_SECS = 600

DEFAULT_AWS_REGION = "us-east-1"

AWS_REGION = os.environ.get("AWS_REGION", DEFAULT_AWS_REGION)
PREDICTION_QUEUE_NAME = os.environ.get("PREDICTION_QUEUE")

sqs_client = boto3.client('sqs', region_name=AWS_REGION)


def send_message2sqs(
    entry_id,
    entry,
    pred_tags,
    pred_thresholds,
    tags_selected,
    callback_url,
    prediction_status,
    geolocations,
    reliability_score
):
    message_attributes = {}
    message_attributes['entry'] = {
        'DataType': 'String',
        'StringValue': entry
    }
    if pred_tags:
        message_attributes['pred_tags'] = {
            'DataType': 'String',
            'StringValue': pred_tags  # already serialized
        }
    if pred_thresholds:
        message_attributes['pred_thresholds'] = {
            'DataType': 'String',
            'StringValue': pred_thresholds  # already serialized
        }
    if tags_selected:
        message_attributes['tags_selected'] = {
            'DataType': 'String',
            'StringValue': tags_selected  # already serialized
        }
    if callback_url:
        message_attributes['callback_url'] = {
            'DataType': 'String',
            'StringValue': callback_url
        }

    message_attributes['prediction_status'] = {
        'DataType': 'Number',
        'StringValue': prediction_status
    }
    message_attributes['geolocations'] = {
        'DataType': 'String',
        'StringValue': geolocations
    }
    message_attributes['reliability_score'] = {
        'DataType': 'String',
        'StringValue': reliability_score if reliability_score.strip() else " "
    }
    if PREDICTION_QUEUE_NAME:
        sqs_client.send_message(
            QueueUrl=PREDICTION_QUEUE_NAME,
            MessageBody=entry_id,
            DelaySeconds=SQS_MSG_DELAY_SECS,
            MessageAttributes=message_attributes
        )
    else:
        logging.error("Message not sent to the processed SQS.")


def entry_predict_dlq_msgs_handler(event, context):
    records = event['Records']

    for record in records:
        entry_id = record['body']
        entry = record['messageAttributes']['entry']['stringValue']
        pred_tags = record['messageAttributes']['pred_tags']['stringValue']
        pred_thresholds = record['messageAttributes']['pred_thresholds']['stringValue']
        tags_selected = record['messageAttributes']['tags_selected']['stringValue']
        callback_url = record['messageAttributes']['callback_url']['stringValue']
        prediction_status = record['messageAttributes']['prediction_status']['stringValue']
        geolocations = record['messageAttributes']['geolocations']['stringValue']
        reliability_score = record['messageAttributes']['reliability_score']['stringValue']

        logging.info(f"Sending the entry id {entry_id} message to Processing Queue")

        sqs_message = {
            'entry_id': entry_id,
            'entry': entry,
            'pred_tags': pred_tags,
            'pred_thresholds': pred_thresholds,
            'tags_selected': tags_selected,
            'callback_url': callback_url,
            'prediction_status': prediction_status,
            'geolocations': geolocations,
            'reliability_score': reliability_score
        }
        send_message2sqs(**sqs_message)

    return {
        'statusCode': 200
    }
