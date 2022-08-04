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

SENTRY_URL = os.environ.get("SENTRY_URL")
ENVIRONMENT = os.environ.get("ENVIRONMENT")

CLIENT_ID = os.environ.get("CLIENT_ID")
URL = os.environ.get("URL")
CALLBACK_URL = os.environ.get("CALLBACK_URL")

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
        logging.error(f"Client error occurred. {str(e)}")
        return False
    return True


def get_words_count(text):
    if text:
        w = re.sub(r'[^\w\s]', '', text)
        w = re.sub(r'_', '', w)
        return len(w.split())
    return 0


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
        'StringValue': extraction_status if s3_text_path else "0"
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
    if PROCESSED_QUEUE_NAME:
        sqs_client.send_message(
            QueueUrl=PROCESSED_QUEUE_NAME,
            MessageBody=client_id,
            DelaySeconds=0,
            MessageAttributes=message_attributes
        )
    else:
        logging.error("Message not sent to the processed SQS.")


def get_extracted_content_links(file_path, file_name):
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


def get_extracted_text_web_links(link, file_name):
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

    store_text_s3(
        extracted_text,
        DEST_BUCKET_NAME,
        f"{str(s3_path_prefix)}/{file_name}"
    )
    s3_file_path = f"s3://{DEST_BUCKET_NAME}/{str(s3_path_prefix)}/{file_name}"
    return s3_file_path, None, total_pages, total_words_count  # No images extraction (lib doesn't support?)


def handle_urls(url):
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
                local_file_path, file_name
            )
            extraction_status = ExtractionStatus.SUCCESS.value
        except Exception as e:
            logging.error(e, exc_info=True)
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
                    temp.name, file_name
                )
                if s3_file_path:
                    extraction_status = ExtractionStatus.SUCCESS.value
                else:
                    extraction_status = ExtractionStatus.FAILED.value
            except Exception as e:
                logging.error(f"Error occurred during text extraction. {str(e)}", exc_info=True)
                s3_file_path, s3_images_path, total_pages, total_words_count = None, None, -1, -1
                extraction_status = ExtractionStatus.FAILED.value
    elif content_type == UrlTypes.HTML.value:  # assume it is a static webpage
        try:
            s3_file_path, s3_images_path, total_pages, total_words_count = get_extracted_text_web_links(
                url, file_name
            )
            if s3_file_path:
                extraction_status = ExtractionStatus.SUCCESS.value
            else:
                extraction_status = ExtractionStatus.FAILED.value
        except Exception:
            logging.error(f"Error occurred during text extraction. {str(e)}", exc_info=True)
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
                        f"/tmp/{filename}", file_name
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
        logging.error("Text extraction is not available for this datatype.")
        s3_file_path, s3_images_path, total_pages, total_words_count = None, None, -1, -1
        extraction_status = ExtractionStatus.FAILED.value

    logging.info(f"The extracted file path is {s3_file_path}")
    logging.info(f"The extracted image path is {s3_images_path}")
    logging.info(f"The status of the extraction is {str(extraction_status)}")

    return s3_file_path, s3_images_path, str(total_pages), str(total_words_count), str(extraction_status)


def process_docs():
    logging.info(f"Processing the {URL}")
    s3_text_path, s3_images_path, total_pages, total_words_count, extraction_status = handle_urls(URL)

    sqs_message = {
        "client_id": CLIENT_ID,
        "url": URL,
        "callback_url": CALLBACK_URL,
        "s3_text_path": s3_text_path,
        "s3_images_path": s3_images_path,
        "total_pages": total_pages,
        "total_words_count": total_words_count,
        "extraction_status": extraction_status
    }
    logging.info(sqs_message)
    send_message2sqs(**sqs_message)


process_docs()
