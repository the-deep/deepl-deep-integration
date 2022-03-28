import os
from math import ceil
import json
import uuid
import boto3
import logging

logging.getLogger().setLevel(logging.INFO)

DEFAULT_AWS_REGION = "us-east-1"
MSG_GROUP_SIZE = 10

aws_region = os.environ.get("AWS_REGION", DEFAULT_AWS_REGION)
queue_url = os.environ.get("ENTRY_PREDICT_INPUT_QUEUE")
reserved_queue_url = os.environ.get("RESERVED_ENTRY_PREDICT_INPUT_QUEUE")

sqs_client = boto3.client("sqs", region_name=aws_region)


class RequestType:
    TYPE_SYSTEM = "system"
    TYPE_USER = "user"


def entry_msg_sqs_handler(event, context):
    request_body = json.loads(event['body'])
    entries_lst = request_body['entries']
    publishing_organization = request_body['publishing_organization']
    authoring_organization = request_body['authoring_organization']
    callback_url = request_body['callback_url']
    request_type = request_body.get('type', RequestType.TYPE_USER)

    entries = [{
        'Id': str(uuid.uuid4()),
        'MessageBody': item['client_id'],
        'DelaySeconds': 0,
        'MessageAttributes': {
            'entry': {
                'DataType': 'String',
                'StringValue': item['entry']
            },
            'publishing_organization': {
                'DataType': 'String',
                'StringValue': publishing_organization
            },
            'authoring_organization': {
                'DataType': 'String',
                'StringValue': json.dumps(authoring_organization) if authoring_organization else json.dumps([])
            },
            'callback_url': {
                'DataType': 'String',
                'StringValue': callback_url
            }
        }
    } for item in entries_lst]
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
            'body': 'Entries Enqueued Successfully'
        }
    except Exception as err:
        logging.error(err)
        return {
            'statusCode': 500,
            'body': err
        }
