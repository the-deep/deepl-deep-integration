import json
import os
import requests
import logging
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config

import sentry_sdk

logging.getLogger().setLevel(logging.INFO)

REQUEST_TIMEOUT = 60
DEFAULT_AWS_REGION = "us-east-1"

aws_region = os.environ.get("AWS_REGION", DEFAULT_AWS_REGION)
signed_url_expiry_secs = os.environ.get("SIGNED_URL_EXPIRY_SECS")

SENTRY_URL = os.environ.get("SENTRY_URL")
ENVIRONMENT = os.environ.get("ENVIRONMENT")

sentry_sdk.init(SENTRY_URL, environment=ENVIRONMENT, traces_sample_rate=1.0)

s3_client = boto3.client(
    's3',
    region_name=aws_region,
    config=Config(
        signature_version='s3v4',
        s3={'addressing_style': 'path'}
    )
)
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
        logging.error(f"ClientError: {e}")
        return None
    logging.info(f'The generated signed url is {url}')
    return url


def output_request(event, context):
    records = event['Records']

    for record in records:
        request_body = {}
        image_urls = []

        client_id = record['body']
        message_attributes = record['messageAttributes']
        s3_text_path = message_attributes['s3_text_path']['stringValue'] \
            if 's3_text_path' in message_attributes else None
        s3_images_path = message_attributes['s3_images_path']['stringValue'] \
            if 's3_images_path' in message_attributes else None
        url = message_attributes['url']['stringValue']
        callback_url = message_attributes['callback_url']['stringValue']
        total_pages = message_attributes['total_pages']['stringValue']
        total_words_count = message_attributes['total_words_count']['stringValue']
        extraction_status = message_attributes['extraction_status']['stringValue']

        # Preparing the request body on callback url.

        request_body['client_id'] = client_id
        request_body['url'] = url

        doc_bucket_name, doc_key_name = extract_path(s3_text_path)
        if doc_bucket_name and doc_key_name:
            s3_file_signed_url = generate_signed_url(
                doc_bucket_name, doc_key_name
            )
            if s3_file_signed_url:
                request_body['text_path'] = s3_file_signed_url
        else:
            request_body['text_path'] = None
        # Note: enable if images are required to be sent to deep.
        # images_bucket_name, images_key_name = extract_path(s3_images_path)
        # if images_bucket_name and images_key_name:
        #     response = s3_client.list_objects(
        #         Bucket=images_bucket_name, Prefix=images_key_name
        #     )
        #     for content in response.get('Contents', []):
        #         image_key_name = content.get('Key')
        #         s3_image_signed_url = generate_signed_url(
        #             images_bucket_name, image_key_name
        #         )
        #         if s3_image_signed_url:
        #             image_urls.append(s3_image_signed_url)
        #     if image_urls:
        #         request_body['images_path'] = image_urlss
        request_body['images_path'] = []  # if s3_images_path else None

        request_body['total_pages'] = total_pages
        request_body['total_words_count'] = total_words_count
        request_body['extraction_status'] = extraction_status

        # Sending the request towards Deep
        logging.info(f"The request body is {json.dumps(request_body)}")
        try:
            response = requests.post(
                callback_url,
                data=request_body,
                timeout=60
            )
            if response.status_code == 200:
                logging.info(f"Successfully sent the request on {callback_url} with client_id: {client_id}")
            else:
                logging.error(f"Request not sent successfully on {callback_url} with {response.content}")
                err_resp = response.json()
                if "errors" in err_resp and "clientId" not in err_resp["errors"]:
                    raise Exception(f"Exception occurred while sending request with StatusCode {response.status_code}")
                else:
                    logging.info('ClientId is invalid. Not sending the request anymore.')
                    return {
                        "statusCode": 200,
                        "body": "ClientId is invalid. Not sending the request anymore."
                    }
        except requests.exceptions.RequestException as e:
            raise Exception(f"Exception occurred while sending request - {e}")

    return {
        "statusCode": 200,
        "body": "Successfully sent on the callback url"
    }
