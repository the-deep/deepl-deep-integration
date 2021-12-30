from celery import Celery
from .app import process_docs
import requests

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

cel_app = Celery(__name__, broker='redis://redis:6379/3')

cel_app.config_from_object(__name__)


@cel_app.task()
def extract_contents(args):
    extraction_response = process_docs(args, None)
    logger.info(extraction_response)
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
