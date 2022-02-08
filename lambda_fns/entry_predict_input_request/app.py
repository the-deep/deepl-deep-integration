import os
import json
import uuid
import boto3
import logging

logging.getLogger().setLevel(logging.INFO)

DEFAULT_AWS_REGION = "us-east-1"

aws_region = os.environ.get("AWS_REGION", DEFAULT_AWS_REGION)
queue_url = os.environ.get("ENTRY_PREDICT_INPUT_QUEUE")

sqs_client = boto3.client("sqs", region_name=aws_region)


def entry_msg_sqs_handler(event, context):
    request_body = json.loads(event['body'])
    entries_lst = request_body['entries']
    callback_url = request_body['callback_url']

    entries = [{
        'Id': str(uuid.uuid4()),
        'MessageBody': item['entry_id'],
        'DelaySeconds': 0,
        'MessageAttributes': {
            'entry': {
                'DataType': 'String',
                'StringValue': item['entry']
            },
            'callback_url': {
                'DataType': 'String',
                'StringValue': callback_url
            }
        }
    } for item in entries_lst]
    try:
        sqs_client.send_message_batch(
            QueueUrl=queue_url,
            Entries=entries
        )
        return {
            'statusCode': 200,
            'body': 'Entries Enqueued Successfully'
        }
    except Exception as err:
        logging.error(err)
        return {
            'statusCode': 500,
            'body': err
        }
