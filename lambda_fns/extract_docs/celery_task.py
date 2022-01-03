import os
import requests
from celery import Celery
from celery.utils.log import get_task_logger

from .app import process_docs

logger = get_task_logger(__name__)

EXTRACTOR_REDIS_URL = os.environ.get("EXTRACTOR_REDIS_URL", 'redis://redis:6379/3')

cel_app = Celery(__name__, broker=EXTRACTOR_REDIS_URL)

cel_app.config_from_object(__name__)


@cel_app.task()
def extract_contents(args):
    extraction_response = process_docs(args, None)
    try:
        response = requests.post(
            args['callback_url'],
            data=extraction_response,
            timeout=60
        )
        if response.status_code == 200:
            logger.info("Successfully sent the request on call")
        else:
            logger.info("Request not sent successfully.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Exception occurred while sending requests. {e}")
    finally:
        logger.info("The task is complete.")
