import requests
import tempfile
import uuid
import base64
import logging
import re
import pathlib
import sentry_sdk
from enum import Enum
from datetime import datetime

try:
    from content_types import ExtractContentType, UrlTypes
    from config import (
        EXTRACTED_FILE_NAME,
        AWS_REGION,
        DEST_BUCKET_NAME,
        PROCESSED_QUEUE_NAME,
        DOCS_CONVERT_LAMBDA_FN_NAME,
        DOCS_CONVERSION_BUCKET_NAME,
        DOMAIN_NAME,
        SENTRY_URL,
        ENVIRONMENT,
        VPC_PRIVATE_SUBNET,
        ECS_CLUSTER_ID,
        ECS_TASK_DEFINITION,
        ECS_CONTAINER_NAME
    )
except ImportError:
    from deep_parser import TextFromFile, TextFromWeb
    from .content_types import ExtractContentType, UrlTypes
    from .config import (
        EXTRACTED_FILE_NAME,
        AWS_REGION,
        DEST_BUCKET_NAME,
        PROCESSED_QUEUE_NAME,
        DOCS_CONVERT_LAMBDA_FN_NAME,
        DOCS_CONVERSION_BUCKET_NAME,
        DOMAIN_NAME,
        SENTRY_URL,
        ENVIRONMENT,
        VPC_PRIVATE_SUBNET,
        ECS_CLUSTER_ID,
        ECS_TASK_DEFINITION,
        ECS_CONTAINER_NAME
    )

logging.getLogger().setLevel(logging.INFO)

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
        entries, images = document.extract_text(output_format="list")
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


def get_extracted_text_web_links(link, file_name, mock=False):
    try:
        web_text = TextFromWeb(url=link)
        entries = web_text.extract_text(output_format="list", url=link)
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
    return s3_file_path, None, total_pages, total_words_count  # No images extraction (lib doesn't support?)


def handle_urls(url, mock=False):
    content_type = extract_content_type.get_content_type(url, REQ_HEADERS)

    file_name = EXTRACTED_FILE_NAME

    if content_type == UrlTypes.PDF.value:  # assume it is http/https pdf weblink
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
        logging.warn("Text extraction from docx, xlsx, pptx, doc, xls, ppt is not available in local setup.")
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
    import boto3
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
