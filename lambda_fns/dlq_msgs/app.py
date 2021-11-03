import os
import boto3

SQS_MSG_DELAY_SECS = 600

DEFAULT_AWS_REGION = "us-east-1"

aws_region = os.environ.get("AWS_REGION", DEFAULT_AWS_REGION)
processed_queue_name = os.environ.get("PROCESSED_QUEUE")

sqs_client = boto3.client('sqs', region_name=aws_region)


def send_message2sqs(client_id, url, callback_url, s3_file_path, s3_images_path):
    message_attributes = {}
    message_attributes['url'] = {
            'DataType': 'String',
            'StringValue': url
    }
    if s3_file_path:
        message_attributes['s3_file_path'] = {
            'DataType': 'String',
            'StringValue': s3_file_path
        }
    if s3_images_path:
        message_attributes['s3_images_path'] = {
            'DataType': 'String',
            'StringValue': s3_images_path
        }
    if callback_url:
        message_attributes['callback_url'] = {
            'DataType': 'String',
            'StringValue': callback_url
        }
    if processed_queue_name and s3_file_path:
        sqs_client.send_message(
            QueueUrl=processed_queue_name,
            MessageBody=client_id,
            DelaySeconds=SQS_MSG_DELAY_SECS,
            MessageAttributes=message_attributes
        )
    else:
        print("Message not sent to the processed SQS.")


def dlq_msgs_handler(event, context):
    records = event['Records']

    for record in records:
        client_id = record['body']
        message_attributes = record['messageAttributes']
        s3_file_path = message_attributes['s3_file_path']['stringValue'] if 's3_file_path' in message_attributes else None
        s3_images_path = message_attributes['s3_images_path']['stringValue'] if 's3_images_path' in message_attributes else None
        url = message_attributes['url']['stringValue']
        callback_url = message_attributes['callback_url']['stringValue']

        print(f'Storing message from dlq to processed queue with client id {client_id}')

        sqs_message = {
            'client_id': client_id,
            'url': url,
            'callback_url': callback_url,
            's3_file_path': s3_file_path,
            's3_images_path': s3_images_path
        }
        send_message2sqs(**sqs_message)

    return {
        'statusCode': 200
    }