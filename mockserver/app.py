import json
import logging
from flask.helpers import send_from_directory

import requests
from flask import Flask, request

from lambda_fns.entry_predict_output_request.app import entry_predict_output_handler
from lambda_fns.extract_docs.celery_task import extract_contents
from lambda_fns.model_info.app import lambda_handler

from mappings.tags_mapping import get_vf_list

logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)


@app.route('/')
def homepage():
    return json.dumps({
        "status": "Welcome to mock server"
    })


@app.route('/extract_docs', methods=['POST'])
def extract_documents():
    body = request.get_json()

    for item in body['urls']:
        extract_contents.delay({
            'mock': True,
            'url': item['url'],
            'client_id': item['client_id'],
            'callback_url': body['callback_url']
        })

    return json.dumps({
        "status": "Requests are enqueued successfully"
    })


@app.route('/tmp/<path:filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory("/tmp/", filename, as_attachment=True)


@app.route('/vf_tags', methods=['GET'])
def get_vf_tags():
    return json.dumps(get_vf_list())


@app.route('/entry_predict', methods=['POST'])
def predict_entry():
    body = request.get_json()

    event = {}
    event['mock'] = True
    event['entries'] = body['entries']
    event['publishing_organization'] = body['publishing_organization']
    event['authoring_organization'] = body['authoring_organization']\
        if 'authoring_organization' in body else None

    callback_url = body['callback_url']

    responses = entry_predict_output_handler(event, None)

    headers = {
        'Content-Type': 'application/json'
    }

    for response_body in responses:
        try:
            response = requests.post(
                callback_url,
                headers=headers,
                data=json.dumps(response_body),
                timeout=60
            )
            if response.status_code == 200:
                logging.info(f"Successfully sent the request on callback url with entry id {response_body['entry_id']}")
            else:
                logging.error("Request not sent successfully.")
                raise Exception(f"Exception occurred while sending request: StatusCode {response.status_code}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Exception occurred while sending request - {e}")

    return json.dumps({
        "status": "Response handled successfully"
    })


@app.route('/model_info', methods=['GET'])
def model_info():
    event = {}
    event["mock"] = True
    return json.dumps(json.loads(lambda_handler(event, None)["body"]))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8001", debug=True)
