import os
import boto3
import json

DEFAULT_AWS_REGION = "us-east-1"

AWS_REGION = os.environ.get("AWS_REGION", DEFAULT_AWS_REGION)
PREDICTION_QUEUE_NAME = os.environ.get("PREDICTION_QUEUE")
ENDPOINT_NAME_MODEL = os.environ.get("EP_NAME_MODEL")

sqs_client = boto3.client('sqs', region_name=AWS_REGION)

sagemaker_rt = boto3.client("runtime.sagemaker", region_name="us-east-1")  # todo: update the region later.


def send_message2sqs(
    entry_id,
    entry,
    predictions,
    callback_url
):
    message_attributes = {}
    message_attributes['entry'] = {
        'DataType': 'String',
        'StringValue': entry
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
    response = sagemaker_rt.invoke_endpoint(
        EndpointName=ENDPOINT_NAME_MODEL,
        ContentType="application/json; format=pandas-split",
        Body=json.dumps(data)
    )
    pred_response = json.loads(response["Body"].read().decode("ascii"))

    return pred_response


def predict_entry_handler(event, context):
    records = event['Records']

    for record in records:
        entry_id = record['body']
        entry = record['messageAttributes']['entry']['stringValue']
        callback_url = record['messageAttributes']['callback_url']['stringValue']
        print(f"Processing entry id {entry_id}")

        predictions = get_predictions(entry)

        sqs_message = {
            'entry_id': entry_id,
            'entry': entry,
            'predictions': predictions,
            'callback_url': callback_url
        }
        send_message2sqs(**sqs_message)
