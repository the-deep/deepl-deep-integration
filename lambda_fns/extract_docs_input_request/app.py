import os
import json
import uuid
import logging
import boto3
from math import ceil

logging.getLogger().setLevel(logging.INFO)

MSG_GROUP_SIZE = 10
DEFAULT_AWS_REGION = "us-east-1"

aws_region = os.environ.get("AWS_REGION", DEFAULT_AWS_REGION)
queue_url = os.environ.get("INPUT_QUEUE")
reserved_queue_url = os.environ.get("RESERVED_INPUT_QUEUE")

sqs_client = boto3.client("sqs", region_name=aws_region)


class RequestType:
    TYPE_SYSTEM = "system"
    TYPE_USER = "user"


def send_msg_sqs(event, context):
    request_body = json.loads(event['body'])
    urls = request_body['urls']
    callback_url = request_body['callback_url']
    request_type = request_body.get('type', RequestType.TYPE_SYSTEM)

    entries = [{
        'Id': str(uuid.uuid4()),
        'MessageBody': item['client_id'],
        'DelaySeconds': 0,
        'MessageAttributes': {
            'url': {
                'DataType': 'String',
                'StringValue': item['url']
            },
            'callback_url': {
                'DataType': 'String',
                'StringValue': callback_url
            }
        }
    } for item in urls]
    try:
        i = 0
        if request_type == RequestType.TYPE_SYSTEM:
            logging.info("System generated requests are enqueued.")
            for _ in range(ceil(len(entries) / MSG_GROUP_SIZE)):
                sqs_client.send_message_batch(
                    QueueUrl=queue_url,
                    Entries=entries[i: i + MSG_GROUP_SIZE]
                )
                i += MSG_GROUP_SIZE
        else:
            logging.info("User generated requests are enqueued.")
            for _ in range(ceil(len(entries) / MSG_GROUP_SIZE)):
                sqs_client.send_message_batch(
                    QueueUrl=reserved_queue_url,
                    Entries=entries[i: i + MSG_GROUP_SIZE]
                )
                i += MSG_GROUP_SIZE
        return {
            'statusCode': 200,
            'body': 'Message Enqueued Successfully'
        }
    except Exception as err:
        logging.error(err)
        return {
            'statusCode': 500,
            'body': err
        }
