import os
import requests
import uuid
import base64
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

from deep_parser.parser.base import TextFromFile
from deep_parser import TextFromWeb

aws_region = os.environ.get("AWS_REGION")
dest_bucket_name = os.environ.get("DEST_S3_BUCKET")
processed_queue_name = os.environ.get("PROCESSED_QUEUE")

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


def get_extracted_content_links(file_name):
    with open(os.path.join("/tmp", file_name), "rb") as f:
        binary = base64.b64encode(f.read())

    document = TextFromFile(stream=binary, ext="pdf")
    entries, images = document.extract_text(output_format="list")

    entries_list = [item for sublist in entries for item in sublist]
    extracted_text = "\n".join(entries_list)

    date_today = str(datetime.now().date())

    processed_file_name = ''.join(file_name.split('.')[:-1])
    dir_name = "-".join(processed_file_name.split())

    s3_path_prefix = f"{date_today}/{dir_name}"
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

    return s3_file_path, s3_images_path


def send_filepath_sqs(url_id, url, s3_file_path, s3_images_path):
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
    if processed_queue_name and s3_file_path:
        sqs_client.send_message(
            QueueUrl=processed_queue_name,
            MessageBody=url_id,
            DelaySeconds=0,
            MessageAttributes=message_attributes
        )
    else:
        print("Message not sent to the processed SQS.")


def get_extracted_text_web_links(link):
    try:
        web_text = TextFromWeb(url=link)
        entries = web_text.extract_text(output_format="list")

        entries_list = [item for sublist in entries for item in sublist]
        extracted_text = "\n".join(entries_list)

        date_today = str(datetime.now().date())

        processed_file_name = uuid.uuid4().hex
        dir_name = uuid.uuid4().hex

        s3_path_prefix = f"{date_today}/{dir_name}"
        store_text_s3(
            extracted_text,
            dest_bucket_name,
            f"{s3_path_prefix}/{processed_file_name}.txt"
        )
        s3_file_path = f"s3://{dest_bucket_name}/{s3_path_prefix}/{processed_file_name}.txt"

        return s3_file_path, None  # No images extraction (lib doesn't support?)
    except Exception as e:
        print(f"Extraction from website failed {e}")
        return None, None


def process_docs(event, context):
    print(f"The event output is {event}")

    records = event['Records']

    for record in records:
        url_id = record['body']
        url = record['messageAttributes']['link']['stringValue']
        print(f"Processing {url}")

        file_name = None
        if url.startswith("s3"):
            bucket_name, file_path, file_name = extract_path(url)
            s3_client.download_file(
                bucket_name,
                file_path,
                f"/tmp/{file_name}"
            )
            s3_file_path, s3_images_path = get_extracted_content_links(file_name)
        elif url.endswith(".pdf"):  # assume it is http/https pdf weblink
            response = requests.get(url, stream=True)
            file_name = f"{str(uuid.uuid4())}.pdf"
            with open(f"/tmp/{file_name}", 'wb') as fd:
                for chunk in response.iter_content(chunk_size=128):
                    fd.write(chunk)
            s3_file_path, s3_images_path = get_extracted_content_links(file_name)
        else:  # assume it is a webpage
            s3_file_path, s3_images_path = get_extracted_text_web_links(url)

        print(f"The extracted file path is {s3_file_path}")
        print(f"The extracted image path is {s3_images_path}")
        send_filepath_sqs(url_id, url, s3_file_path, s3_images_path)
