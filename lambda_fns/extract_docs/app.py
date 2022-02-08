import os
import requests
import uuid
import base64
from datetime import datetime
from enum import Enum
import boto3
import logging

from deep_parser.parser.base import TextFromFile
from deep_parser import TextFromWeb

try:
    from content_types import ExtractContentType, UrlTypes
except ImportError:
    from .content_types import ExtractContentType, UrlTypes

logging.getLogger().setLevel(logging.INFO)

DEFAULT_AWS_REGION = "us-east-1"

aws_region = os.environ.get("AWS_REGION", DEFAULT_AWS_REGION)
dest_bucket_name = os.environ.get("DEST_S3_BUCKET")
processed_queue_name = os.environ.get("PROCESSED_QUEUE")

domain_name = os.environ.get("EXTRACTOR_DOMAIN_NAME", "http://extractor:8001")

s3_client = boto3.client('s3', region_name=aws_region)
sqs_client = boto3.client('sqs', region_name=aws_region)

extract_content_type = ExtractContentType()


class ExtractionStatus(Enum):
    FAILED = 0
    SUCCESS = 1


def extract_path(filepath):
    """
    Extracts bucket and key names from the s3 URI
    """
    if filepath is not None:
        bucket_and_key = filepath.split("//")[-1]
        bucket_key_split = bucket_and_key.split("/")
        bucket_name = bucket_key_split[0]
        file_path = '/'.join(bucket_key_split[1:])
        file_name = bucket_key_split[-1]
        return bucket_name, file_path, file_name
    return None, None, None


def store_text_s3(data, bucket_name, key):
    s3_client.put_object(
        Body=data,
        Bucket=bucket_name,
        Key=key
    )


def get_words_count(text):
    return len(text.split()) if text else 0


def send_message2sqs(
    client_id,
    url,
    callback_url,
    s3_text_path,
    s3_images_path,
    total_pages,
    total_words_count,
    extraction_status
):
    message_attributes = {}
    message_attributes['url'] = {
        'DataType': 'String',
        'StringValue': url
    }
    message_attributes['extraction_status'] = {
        'DataType': 'Number',
        'StringValue': extraction_status
    }
    if s3_text_path:
        message_attributes['s3_text_path'] = {
            'DataType': 'String',
            'StringValue': s3_text_path
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
    message_attributes['total_pages'] = {
        'DataType': 'Number',
        'StringValue': total_pages
    }
    message_attributes['total_words_count'] = {
        'DataType': 'Number',
        'StringValue': total_words_count
    }
    if processed_queue_name and s3_text_path:
        sqs_client.send_message(
            QueueUrl=processed_queue_name,
            MessageBody=client_id,
            DelaySeconds=0,
            MessageAttributes=message_attributes
        )
    else:
        logging.error("Message not sent to the processed SQS.")


def get_extracted_content_links(file_name, mock):
    with open(os.path.join("/tmp", file_name), "rb") as f:
        binary = base64.b64encode(f.read())

    document = TextFromFile(stream=binary, ext="pdf")
    entries, images = document.extract_text(output_format="list")

    entries_list = [item for sublist in entries for item in sublist]
    extracted_text = "\n".join(entries_list)

    total_pages = len(entries)
    total_words_count = get_words_count(extracted_text)

    date_today = str(datetime.now().date())

    processed_file_name = ''.join(file_name.split('.')[:-1])
    dir_name = "-".join(processed_file_name.split())

    s3_path_prefix = f"{date_today}/{dir_name}"
    if mock:
        dir_path = f'/tmp/{s3_path_prefix}'
        os.makedirs(f'{dir_path}/images')
        with open(f'{dir_path}/{processed_file_name}.txt', 'w') as f:
            f.write(extracted_text)

        images.save_images(directory_path=f'{dir_path}/images')

        s3_file_path = f'{domain_name}{dir_path}/{processed_file_name}.txt'
        s3_images_path_prefix = f'{dir_path}/images'
        s3_images_path = []
        for subdir, dirs, files in os.walk(s3_images_path_prefix):
            for f in files:
                full_path = os.path.join(subdir, f)
                with open(full_path, 'rb') as data:
                    s3_images_path.append(f"{domain_name}{s3_images_path_prefix}/{f}")
        return s3_file_path, s3_images_path, total_pages, total_words_count
    else:
        store_text_s3(
            extracted_text,
            dest_bucket_name,
            f"{s3_path_prefix}/{processed_file_name}.txt"
        )

        local_temp_directory = f"/tmp/{processed_file_name}"
        os.mkdir(local_temp_directory)
        images.save_images(directory_path=local_temp_directory)

        for subdir, dirs, files in os.walk(local_temp_directory):
            for f in files:
                full_path = os.path.join(subdir, f)
                with open(full_path, 'rb') as data:
                    store_text_s3(
                        data,
                        dest_bucket_name,
                        f"{s3_path_prefix}/images/{f}"
                    )

        s3_file_path = f"s3://{dest_bucket_name}/{s3_path_prefix}/{processed_file_name}.txt"
        s3_images_path = f"s3://{dest_bucket_name}/{s3_path_prefix}/images"

    return s3_file_path, s3_images_path, total_pages, total_words_count


def get_extracted_text_web_links(link, mock=False):
    try:
        web_text = TextFromWeb(url=link)
        entries = web_text.extract_text(output_format="list")

        entries_list = [item for sublist in entries for item in sublist]
        extracted_text = "\n".join(entries_list)

        total_pages = -1
        total_words_count = get_words_count(extracted_text)

        date_today = str(datetime.now().date())

        processed_file_name = uuid.uuid4().hex
        dir_name = uuid.uuid4().hex

        s3_path_prefix = f"{date_today}/{dir_name}"
        if mock:
            dir_path = f'/tmp/{s3_path_prefix}'
            os.makedirs(f'{dir_path}/images')
            with open(f'{dir_path}/{processed_file_name}.txt', 'w') as f:
                f.write(extracted_text)
            s3_file_path = f'{domain_name}{dir_path}/{processed_file_name}.txt'
        else:
            store_text_s3(
                extracted_text,
                dest_bucket_name,
                f"{s3_path_prefix}/{processed_file_name}.txt"
            )
            s3_file_path = f"s3://{dest_bucket_name}/{s3_path_prefix}/{processed_file_name}.txt"

        return s3_file_path, None, total_pages, total_words_count  # No images extraction (lib doesn't support?)
    except Exception as e:
        logging.error(f"Extraction from website failed {e}")
        return None, None, -1, -1


def handle_urls(url, mock=False):
    file_name = None

    content_type = extract_content_type.get_content_type(url)

    if url.startswith("s3"):
        bucket_name, file_path, file_name = extract_path(url)
        s3_client.download_file(
            bucket_name,
            file_path,
            f"/tmp/{file_name}"
        )
        try:
            s3_file_path, s3_images_path, total_pages, total_words_count = get_extracted_content_links(
                file_name, mock
            )
            extraction_status = ExtractionStatus.SUCCESS.value
        except Exception:
            s3_file_path, s3_images_path, total_pages, total_words_count = None, None, -1, -1
            extraction_status = ExtractionStatus.FAILED.value

    elif content_type == UrlTypes.PDF.value:  # assume it is http/https pdf weblink
        response = requests.get(url, stream=True)
        file_name = f"{str(uuid.uuid4())}.pdf"
        with open(f"/tmp/{file_name}", 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)
        try:
            s3_file_path, s3_images_path, total_pages, total_words_count = get_extracted_content_links(
                file_name, mock
            )
            extraction_status = ExtractionStatus.SUCCESS.value
        except Exception:
            s3_file_path, s3_images_path, total_pages, total_words_count = None, None, -1, -1
            extraction_status = ExtractionStatus.FAILED.value
    elif content_type == UrlTypes.HTML.value:  # assume it is a static webpage
        try:
            s3_file_path, s3_images_path, total_pages, total_words_count = get_extracted_text_web_links(url, mock)
            extraction_status = ExtractionStatus.SUCCESS.value
        except Exception:
            s3_file_path, s3_images_path, total_pages, total_words_count = None, None, -1, -1
            extraction_status = ExtractionStatus.FAILED.value
    else:
        raise NotImplementedError

    logging.info(f"The extracted file path is {s3_file_path}")
    logging.info(f"The extracted image path is {s3_images_path}")

    return s3_file_path, s3_images_path, str(total_pages), str(total_words_count), str(extraction_status)


def process_docs(event, context):
    logging.debug(f"The event output is {event}")

    if event.get('mock', False):
        url = event['url']
        text_path, images_path, total_pages, total_words_count, extraction_status = handle_urls(url, mock=True)
        return {
            'client_id': event['client_id'],
            'url': url,
            'text_path': text_path,
            'images_path': images_path,
            'total_pages': total_pages,
            'total_words_count': total_words_count,
            'extraction_status': extraction_status
        }
    else:
        records = event['Records']

        for record in records:
            client_id = record['body']
            url = record['messageAttributes']['url']['stringValue']
            callback_url = record['messageAttributes']['callback_url']['stringValue']
            logging.info(f"Processing {url}")

            s3_text_path, s3_images_path, total_pages, total_words_count, extraction_status = handle_urls(url)

            sqs_message = {
                'client_id': client_id,
                'url': url,
                'callback_url': callback_url,
                's3_text_path': s3_text_path,
                's3_images_path': s3_images_path,
                'total_pages': total_pages,
                'total_words_count': total_words_count,
                'extraction_status': extraction_status
            }
            send_message2sqs(**sqs_message)

    return {
        'StatusCode': 200,
        'Body': 'Message processed successfully.'
    }
