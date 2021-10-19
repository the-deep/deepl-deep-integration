import os
import json
import uuid
import boto3
from botocore.exceptions import ClientError

aws_region = os.environ.get("AWS_REGION")
queue_url = os.environ.get("INPUT_QUEUE")

sqs_client = boto3.client("sqs", region_name=aws_region)


def send_msg_sqs(event, context):
    errormsg = None

    request_body = json.loads(event['body'])
    urls = request_body['urls']

    if queue_url:
        try:
            entries = [{
                'Id': str(uuid.uuid4()),
                'MessageBody': item['id'],
                'DelaySeconds': 0,
                'MessageAttributes': {
                    'link': {
                        'DataType': 'String',
                        'StringValue': item['url']
                    }
                }
            } for item in urls]
            sqs_client.send_message_batch(
                QueueUrl=queue_url,
                Entries=entries
            )
            return {
                'statusCode': 200,
                'body': "returned"
            }
        except Exception as err:
            print(err)
            errormsg = err

    return {
        'statusCode': 500,
        'body': errormsg
    }
