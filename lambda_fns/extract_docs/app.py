import os
import requests
import uuid
import json
import base64
import logging
import re
import pathlib
from datetime import datetime
from enum import Enum
import boto3
from botocore.exceptions import ClientError
import tempfile

import sentry_sdk

from deep_parser import TextFromFile
from deep_parser import TextFromWeb

try:
    from content_types import ExtractContentType, UrlTypes
except ImportError:
    from .content_types import ExtractContentType, UrlTypes

logging.getLogger().setLevel(logging.INFO)

EXTRACTED_FILE_NAME = "extract_text.txt"
DEFAULT_AWS_REGION = "us-east-1"

AWS_REGION = os.environ.get("AWS_REGION", DEFAULT_AWS_REGION)
DEST_BUCKET_NAME = os.environ.get("DEST_S3_BUCKET")
PROCESSED_QUEUE_NAME = os.environ.get("PROCESSED_QUEUE")
DOCS_CONVERT_LAMBDA_FN_NAME = os.environ.get("DOCS_CONVERT_LAMBDA_FN_NAME")
DOCS_CONVERSION_BUCKET_NAME = os.environ.get("DOCS_CONVERSION_BUCKET_NAME")

DOMAIN_NAME = os.environ.get("EXTRACTOR_DOMAIN_NAME", "http://extractor:8001")

SENTRY_URL = os.environ.get("SENTRY_URL")
ENVIRONMENT = os.environ.get("ENVIRONMENT")

s3_client = boto3.client('s3', region_name=AWS_REGION)
sqs_client = boto3.client('sqs', region_name=AWS_REGION)
lambda_client = boto3.client('lambda', region_name=AWS_REGION)

extract_content_type = ExtractContentType()

sentry_sdk.init(SENTRY_URL, environment=ENVIRONMENT, attach_stacktrace=True, traces_sample_rate=1.0)

REQ_HEADERS = {
    'user-agent': ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1')
}


class ExtractionStatus(Enum):
    FAILED = 0
    SUCCESS = 1


def extract_path(filepath):
    """
    Extracts bucket and key names from the s3 URI
    """
    if filepath is not None:
        filepath_split = pathlib.Path(filepath).parts
        bucket_name = filepath_split[1]
        file_key_path = str(pathlib.Path(*filepath_split[2:]))
        file_name = filepath_split[-1]
        return bucket_name, file_key_path, file_name
    return None, None, None


def store_text_s3(data, bucket_name, key):
    s3_client.put_object(
        Body=data,
        Bucket=bucket_name,
        Key=key
    )

def upload_file_to_s3(
    url,
    key="temporaryfile.pdf",
    bucketname="deep-large-docs-conversion"
):
    try:
        session = boto3.Session()
        s3_resource = session.resource("s3")

        r = requests.get(url, stream=True)
        if r.status_code == 200:
            bucket = s3_resource.Bucket(bucketname)
            bucket.upload_fileobj(r.raw, key)
            logging.info(f"The file is uploaded to the S3 bucket {bucketname}")
        else:
            return False
    except Exception as e:
        logging.error(str(e))
        return False
    return True

def download_file(filename_s3, bucketname, filename_local):
    try:
        s3_client.download_file(
            bucketname,
            filename_s3,
            filename_local
        )
        logging.info("The file is downloaded in the lambda /tmp directory.")
    except ClientError as e:
        return False
    return True


def get_words_count(text):
    if text:
        w = re.sub(r'[^\w\s]', '', text)
        w = re.sub(r'_', '', w)
        return len(w.split())
    return 0


def get_extracted_content_links(file_path, file_name, mock):
    try:
        with open(pathlib.Path(file_path), "rb") as f:
            binary = base64.b64encode(f.read())

        document = TextFromFile(stream=binary, ext="pdf")
        entries, images = document.serial_extract_text(output_format="list")
    except Exception as e:
        logging.error(f"Extraction failed: {str(e)}")
        return None, None, -1, -1

    entries_list = [item for sublist in entries for item in sublist]
    extracted_text = "\n".join(entries_list)
    
    extracted_text = extracted_text.replace("\x00", "")  # remove null chars
    extracted_text = extracted_text.encode('utf-8', 'ignore').decode('utf-8')
    total_pages = len(entries)
    total_words_count = get_words_count(extracted_text)

    date_today = str(datetime.now().date())

    dir_name = str(uuid.uuid4())

    s3_path_prefix = pathlib.Path(date_today, dir_name)
    if mock:
        dir_path = pathlib.Path('/tmp') / s3_path_prefix
        dir_path.mkdir(parents=True) if not dir_path.exists() else None
        with open(dir_path / file_name, 'w') as f:
            f.write(extracted_text)

        dir_images_path = dir_path / 'images'
        dir_images_path.mkdir() if not dir_images_path.exists() else None
        images.save_images(directory_path=dir_images_path)

        s3_file_path = f'{DOMAIN_NAME}{str(dir_path)}/{file_name}'

        s3_images_path = []
        # Note: commented for now
        # for subdir, dirs, files in os.walk(dir_images_path):
        #     for f in files:
        #         full_path = os.path.join(subdir, f)
        #         with open(full_path, 'rb') as data:
        #             s3_images_path.append(f"{DOMAIN_NAME}{str(dir_images_path)}/{f}")
        return s3_file_path, s3_images_path, total_pages, total_words_count
    else:
        store_text_s3(
            extracted_text,
            DEST_BUCKET_NAME,
            f"{str(s3_path_prefix)}/{file_name}"
        )

        local_temp_directory = pathlib.Path('/tmp', file_name)
        local_temp_directory.mkdir(parents=True) if not local_temp_directory.exists() else None
        # Note: commented for now
        # images.save_images(directory_path=local_temp_directory)

        # for subdir, dirs, files in os.walk(local_temp_directory):
        #     for f in files:
        #         full_path = os.path.join(subdir, f)
        #         with open(full_path, 'rb') as data:
        #             store_text_s3(
        #                 data,
        #                 DEST_BUCKET_NAME,
        #                 f"{str(s3_path_prefix)}/images/{f}"
        #             )

        s3_file_path = f"s3://{DEST_BUCKET_NAME}/{str(s3_path_prefix)}/{file_name}"
        s3_images_path = f"s3://{DEST_BUCKET_NAME}/{str(s3_path_prefix)}/images"

    return s3_file_path, s3_images_path, total_pages, total_words_count


def get_extracted_text_web_links(link, file_name, mock=False):
    try:
        web_text = TextFromWeb(url=link)
        entries = web_text.extract_text(output_format="list")
    except Exception as e:
        logging.error(f"Extraction from website failed {e}")
        return None, None, -1, -1

    entries_list = [item for sublist in entries for item in sublist]
    extracted_text = "\n".join(entries_list)

    extracted_text = extracted_text.replace("\x00", "")  # remove null chars

    total_pages = 1
    total_words_count = get_words_count(extracted_text)

    date_today = str(datetime.now().date())

    dir_name = uuid.uuid4().hex

    s3_path_prefix = pathlib.Path(date_today, dir_name)
    if mock:
        dir_path = pathlib.Path('/tmp') / s3_path_prefix
        dir_path.mkdir(parents=True) if not dir_path.exists() else None
        # os.makedirs(f'{dir_path}/images')
        with open(dir_path / file_name, 'w') as f:
            f.write(extracted_text)
        s3_file_path = f'{DOMAIN_NAME}{str(dir_path)}/{file_name}'
    else:
        store_text_s3(
            extracted_text,
            DEST_BUCKET_NAME,
            f"{str(s3_path_prefix)}/{file_name}"
        )
        s3_file_path = f"s3://{DEST_BUCKET_NAME}/{str(s3_path_prefix)}/{file_name}"
    return s3_file_path, None, total_pages, total_words_count  # No images extraction (lib doesn't support?)


def handle_urls(url, mock=False):
    content_type = extract_content_type.get_content_type(url, REQ_HEADERS)

    file_name = EXTRACTED_FILE_NAME

    if url.startswith("s3"):
        bucket_name, file_path, file_name = extract_path(url)
        local_file_path = f"/tmp/{file_name}"
        s3_client.download_file(
            bucket_name,
            file_path,
            local_file_path
        )
        try:
            s3_file_path, s3_images_path, total_pages, total_words_count = get_extracted_content_links(
                local_file_path, file_name, mock
            )
            extraction_status = ExtractionStatus.SUCCESS.value
        except Exception:
            s3_file_path, s3_images_path, total_pages, total_words_count = None, None, -1, -1
            extraction_status = ExtractionStatus.FAILED.value

    elif content_type == UrlTypes.PDF.value:  # assume it is http/https pdf weblink
        s3_file_path = None
        s3_images_path = None

        response = requests.get(url, headers=REQ_HEADERS, stream=True)
        with tempfile.NamedTemporaryFile(mode='w+b') as temp:
            for chunk in response.iter_content(chunk_size=128):
                temp.write(chunk)
            temp.seek(0)

            try:
                s3_file_path, s3_images_path, total_pages, total_words_count = get_extracted_content_links(
                    temp.name, file_name, mock
                )
                if s3_file_path:
                    extraction_status = ExtractionStatus.SUCCESS.value
                else:
                    extraction_status = ExtractionStatus.FAILED.value
            except Exception:
                s3_file_path, s3_images_path, total_pages, total_words_count = None, None, -1, -1
                extraction_status = ExtractionStatus.FAILED.value
    elif content_type == UrlTypes.HTML.value:  # assume it is a static webpage
        try:
            s3_file_path, s3_images_path, total_pages, total_words_count = get_extracted_text_web_links(
                url, file_name, mock
            )
            if s3_file_path:
                extraction_status = ExtractionStatus.SUCCESS.value
            else:
                extraction_status = ExtractionStatus.FAILED.value
        except Exception:
            s3_file_path, s3_images_path, total_pages, total_words_count = None, None, -1, -1
            extraction_status = ExtractionStatus.FAILED.value
    elif content_type == UrlTypes.DOCX.value or content_type == UrlTypes.MSWORD.value or \
            content_type == UrlTypes.XLSX.value or content_type == UrlTypes.XLS.value or \
            content_type == UrlTypes.PPTX.value or content_type == UrlTypes.PPT.value:

        ext_type = content_type
        tmp_filename = f"{uuid.uuid4().hex}.{ext_type}"
        flag = False
        if upload_file_to_s3(url, key=tmp_filename, bucketname=DOCS_CONVERSION_BUCKET_NAME):
            payload = json.dumps({
                "file": tmp_filename,
                "bucket": DOCS_CONVERSION_BUCKET_NAME,
                "ext": ext_type,
                "fromS3": 1
            })

            docs_conversion_lambda_response = lambda_client.invoke(
                FunctionName=DOCS_CONVERT_LAMBDA_FN_NAME,
                InvocationType="RequestResponse",
                Payload=payload
            )
            docs_conversion_lambda_response_json = json.loads(
                docs_conversion_lambda_response["Payload"].read().decode("utf-8")
            )

            if "statusCode" in docs_conversion_lambda_response_json and \
                docs_conversion_lambda_response_json["statusCode"] == 200:
                bucket_name = docs_conversion_lambda_response_json["bucket"]
                file_path = docs_conversion_lambda_response_json["file"]
                filename = file_path.split("/")[-1]

                if download_file(file_path, bucket_name, f"/tmp/{filename}"):
                    s3_file_path, s3_images_path, total_pages, total_words_count = get_extracted_content_links(
                        f"/tmp/{filename}", file_name, mock
                    )
                    if s3_file_path:
                        extraction_status = ExtractionStatus.SUCCESS.value
                    else:
                        extraction_status = ExtractionStatus.FAILED.value
                else:
                    flag = True
            else:
                logging.error(f"Error occurred during file conversion. {docs_conversion_lambda_response_json['error']}")
                flag = True
        else:
            logging.warn("Could not upload the file to s3.")
            flag = True
        
        if flag:
            s3_file_path, s3_images_path, total_pages, total_words_count = None, None, -1, -1
            extraction_status = ExtractionStatus.FAILED.value
    elif content_type == UrlTypes.IMG.value:
        logging.warn("Text extraction from Images is not available.")
        s3_file_path, s3_images_path, total_pages, total_words_count = None, None, -1, -1
        extraction_status = ExtractionStatus.FAILED.value
    else:
        raise NotImplementedError

    logging.info(f"The extracted file path is {s3_file_path}")
    logging.info(f"The extracted image path is {s3_images_path}")
    logging.info(f"The status of the extraction is {str(extraction_status)}")

    return s3_file_path, s3_images_path, str(total_pages), str(total_words_count), str(extraction_status)


def run_fargate_task(
    client_id,
    url,
    callback_url
):
    VPC_PRIVATE_SUBNET = os.environ.get("VPC_PRIVATE_SUBNET")
    ECS_CLUSTER_ID = os.environ.get("ECS_CLUSTER_ID")
    ECS_TASK_DEFINITION = os.environ.get("ECS_TASK_DEFINITION")
    ECS_CONTAINER_NAME = os.environ.get("ECS_CONTAINER_NAME")
    
    ecs_client = boto3.client('ecs', region_name=AWS_REGION)
    
    response = ecs_client.run_task(
        cluster=ECS_CLUSTER_ID,
        launchType='FARGATE',
        taskDefinition=ECS_TASK_DEFINITION,
        count = 1,
        platformVersion='LATEST',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [
                    VPC_PRIVATE_SUBNET
                ],
                'assignPublicIp': 'DISABLED'
            }
        },
        overrides={
            'containerOverrides': [
                {
                    'name': f"{ECS_CONTAINER_NAME}-{ENVIRONMENT}",
                    'command': [
                            'python',
                            'app.py'
                        ],
                    "environment": [
                        {
                            "name": "CLIENT_ID",
                            "value": client_id
                        },
                        {
                            "name": "URL",
                            "value":  url
                        },
                        {
                            "name": "CALLBACK_URL",
                            "value": callback_url
                        },
                        {
                            "name": "AWS_REGION",
                            "value": AWS_REGION
                        },
                        {
                            "name": "ENVIRONMENT",
                            "value": ENVIRONMENT
                        },
                        {
                            "name": "DEST_S3_BUCKET",
                            "value": DEST_BUCKET_NAME
                        },
                        {
                            "name": "DOCS_CONVERSION_BUCKET_NAME",
                            "value": DOCS_CONVERSION_BUCKET_NAME
                        },
                        {
                            "name": "DOCS_CONVERT_LAMBDA_FN_NAME",
                            "value": DOCS_CONVERT_LAMBDA_FN_NAME
                        },
                        {
                            "name": "PROCESSED_QUEUE",
                            "value": PROCESSED_QUEUE_NAME
                        },
                        {
                            "name": "SENTRY_URL",
                            "value": SENTRY_URL
                        }
                    ]
                },
            ],
        },
    )

    return str(response) #handle the response status


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
        try:
            records = event['Records']

            for record in records:
                client_id = record['body']
                url = record['messageAttributes']['url']['stringValue']
                callback_url = record['messageAttributes']['callback_url']['stringValue']

                logging.info(f"Processing {url} in the ecs fargate.")

                run_fargate_task(client_id, url, callback_url)
        except Exception as e:
            logging.error(e, exc_info=True)
            return {
                "statusCode": 500,
                "body": f"Error occurred: {str(e)}"
            }
    return {
        "statusCode": 200,
        "body": "Message processed successfully."
    }
