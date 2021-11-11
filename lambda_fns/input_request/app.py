import os
import json
import uuid
import boto3

DEFAULT_AWS_REGION = "us-east-1"

aws_region = os.environ.get("AWS_REGION", DEFAULT_AWS_REGION)
queue_url = os.environ.get("INPUT_QUEUE")

sqs_client = boto3.client("sqs", region_name=aws_region)


def send_msg_sqs(event, context):
    errormsg = None

    request_body = json.loads(event['body'])
    urls = request_body['urls']
    callback_url = request_body['callback_url']

    if queue_url:
        try:
            entries = [{
                'Id': str(uuid.uuid4()),
                'MessageBody': item['client_id'],
                'DelaySeconds': 0,
                'MessageAttributes': {
                    'url': {
                        'DataType': 'String',
                        'StringValue': item['url']
                    },
                    'url_content_type': {
                        'DataType': 'String',
                        'StringValue': item['url_content_type']
                    },
                    'callback_url': {
                        'DataType': 'String',
                        'StringValue': callback_url
                    }
                }
            } for item in urls]
            sqs_client.send_message_batch(
                QueueUrl=queue_url,
                Entries=entries
            )
            return {
                'statusCode': 200,
                'body': 'Message Enqueued Successfully'
            }
        except Exception as err:
            print(err)
            errormsg = err

    return {
        'statusCode': 500,
        'body': errormsg
    }
