import os
import json
import requests
import boto3
from botocore.exceptions import ClientError

REQUEST_TIMEOUT = 60
SQS_MSG_DELAY_SECS = 600

aws_region = os.environ.get("AWS_REGION")
processed_queue_name = os.environ.get("PROCESSED_QUEUE")
signed_url_expiry_secs = os.environ.get("SIGNED_URL_EXPIRY_SECS")

s3_client = boto3.client('s3', region_name=aws_region)
sqs_client = boto3.client('sqs', region_name=aws_region)


def extract_path(filepath):
    """
    Extracts bucket and key names from the s3 URI
    """
    if filepath is not None:
        bucket_and_key = filepath.split("//")[-1]
        bucket_key_split = bucket_and_key.split("/")
        bucket_name = bucket_key_split[0]
        key_name = '/'.join(bucket_key_split[1:])
        return bucket_name, key_name
    return None, None


def generate_signed_url(bucket_name, key_name):
    url = None
    try:
        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': bucket_name,
                'Key': key_name
            },
            ExpiresIn=signed_url_expiry_secs
        )
    except ClientError as e:
        print(f"ClientError: {e}")
        return None
    return url


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


def output_request(event, context):
    records = event['Records']

    for record in records:
        request_body = {}
        image_urls = []

        client_id = record['body']
        message_attributes = record['messageAttributes']
        s3_file_path = message_attributes['s3_file_path']['stringValue'] if 's3_file_path' in message_attributes else None
        s3_images_path = message_attributes['s3_images_path']['stringValue'] if 's3_images_path' in message_attributes else None
        url = message_attributes['url']['stringValue']
        callback_url = message_attributes['callback_url']['stringValue']

        request_body['client_id'] = client_id
        request_body['url'] = url

        doc_bucket_name, doc_key_name = extract_path(s3_file_path)
        if doc_bucket_name and doc_key_name:
            s3_file_signed_url = generate_signed_url(
                doc_bucket_name, doc_key_name
            )
            if s3_file_signed_url:
                request_body['s3_file_signed_url'] = s3_file_signed_url

        images_bucket_name, images_key_name = extract_path(s3_images_path)
        if images_bucket_name and images_key_name:
            response = s3_client.list_objects(
                Bucket=images_bucket_name, Prefix=images_key_name
            )
            for content in response.get('Contents', []):
                image_key_name = content.get('Key')
                s3_image_signed_url = generate_signed_url(
                    images_bucket_name, image_key_name
                )
                if s3_image_signed_url:
                    image_urls.append(s3_image_signed_url)
            if image_urls:
                request_body['s3_images_signed_urls'] = image_urls

        # Sending the request towards Deep
        try:
            response = requests.post(
                callback_url,
                data=request_body,
                timeout=60
            )
            if response.status_code == 200:
                print(f'Successfully sent the request with client_id: {client_id}')
            else:
                print('Request not sent successfully.')
                print(f'Message added back in the queue with client_id: {client_id}')
                sqs_message = {
                    'client_id': client_id,
                    'url': url,
                    'callback_url': callback_url,
                    's3_file_path': s3_file_path,
                    's3_images_path': s3_images_path
                }
                send_message2sqs(**sqs_message)    
        except requests.exceptions.RequestException as e:
            print(f"Exception occurred while sending request - {e}")
            print(f'Message added back in the queue with client_id: {client_id}')
            sqs_message = {
                'client_id': client_id,
                'url': url,
                'callback_url': callback_url,
                's3_file_path': s3_file_path,
                's3_images_path': s3_images_path
            }
            send_message2sqs(**sqs_message)

    return {
        'statusCode': 200,
        'body': None
    }
