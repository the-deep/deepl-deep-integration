#!/bin/bash -x
celery -A lambda_fns.extract_docs.celery_task.cel_app  worker --pool=solo --loglevel=INFO &
python -m mockserver.app
