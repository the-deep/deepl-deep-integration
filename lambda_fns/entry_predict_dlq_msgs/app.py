import os
import boto3

SQS_MSG_DELAY_SECS = 600

DEFAULT_AWS_REGION = "us-east-1"

AWS_REGION = os.environ.get("AWS_REGION", DEFAULT_AWS_REGION)
PREDICTION_QUEUE_NAME = os.environ.get("PREDICTION_QUEUE")

sqs_client = boto3.client('sqs', region_name=AWS_REGION)


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
    if predictions:
        message_attributes['predictions'] = {
            'DataType': 'String',
            'StringValue': predictions  # already serialized.
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
    if PREDICTION_QUEUE_NAME:
        sqs_client.send_message(
            QueueUrl=PREDICTION_QUEUE_NAME,
            MessageBody=entry_id,
            DelaySeconds=SQS_MSG_DELAY_SECS,
            MessageAttributes=message_attributes
        )
    else:
        print("Message not sent to the processed SQS.")


def entry_predict_dlq_msgs_handler(event, context):
    records = event['Records']

    for record in records:
        entry_id = record['body']
        entry = record['messageAttributes']['entry']['stringValue']
        predictions = record['messageAttributes']['predictions']['stringValue']
        callback_url = record['messageAttributes']['callback_url']['stringValue']
        prediction_status = record['messageAttributes']['prediction_status']['stringValue']
        geolocations = record['messageAttributes']['geolocations']['stringValue']

        print(f"Sending the entry id {entry_id} message to Processing Queue")

        sqs_message = {
            'entry_id': entry_id,
            'entry': entry,
            'predictions': predictions,
            'callback_url': callback_url,
            'prediction_status': prediction_status,
            'geolocations': geolocations
        }
        send_message2sqs(**sqs_message)

    return {
        'statusCode': 200
    }
