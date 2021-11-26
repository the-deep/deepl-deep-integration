import sys
import json
import os.path
from flask.helpers import send_from_directory

import requests
from flask import Flask, request

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from lambda_fns.extract_docs.app import process_docs
from lambda_fns.predict_entry.app import predict_entry_handler

from mappings.tags_mapping import Categories, Tags, get_all_mappings


app = Flask(__name__)


@app.route('/')
def homepage():
    return "Welcome to mock server"


@app.route('/extract_docs', methods=['POST'])
def extract_documents():
    body = request.get_json()

    event = {}
    event['mock'] = True
    event['urls'] = body['urls']

    callback_url = body['callback_url']

    responses = process_docs(event, None)

    for response_body in responses:
        try:
            response = requests.post(
                callback_url,
                data=response_body,
                timeout=60
            )
            if response.status_code == 200:
                print(f"Successfully sent the request on callback url with client id {response_body['client_id']}")
            else:
                print("Request not sent successfully.")
                raise Exception(f"Exception occurred while sending request: StatusCode {response.status_code}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Exception occurred while sending request - {e}")

    return "Requests handled successfully"


@app.route('/tmp/<path:filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory("/tmp/", filename, as_attachment=True)


@app.route('/vf_tags', methods=['GET'])
def get_vf_tags():
    response = Categories.all_models() + Tags.sector_list() + Tags.subpillars_1d_list() + \
        Tags.subpillars_2d_list() + Tags.specific_needs_group_list() + Tags.gender_list() + \
        Tags.age_list() + Tags.severity_list()

    return json.dumps(response)


@app.route('/entry_predict', methods=['POST'])
def predict_entry():
    body = request.get_json()

    event = {}
    event['mock'] = True
    event['entries'] = body['entries']

    callback_url = body['callback_url']

    responses = predict_entry_handler(event, None)

    headers = {
        'Content-Type': 'application/json'
    }

    mappings = get_all_mappings()

    for response_body in responses:
        data = {
            'predictions': {},
            'thresholds': {},
            'versions': {}
        }
        data['entry_id'] = response_body['entry_id']
        for k1, v1 in response_body['predictions'].items():
            category = mappings[k1][0]
            tags = {}
            versions = {}
            for k2, v2 in v1.items():
                tags[mappings[k2][0]] = v2
                versions[mappings[k2][0]] = mappings[k2][1]
            data['predictions'][category] = tags
            data['versions'][category] = versions

        for k1, v1 in response_body['thresholds'].items():
            category = mappings[k1][0]
            tags = {}
            for k2, v2 in v1.items():
                tags[mappings[k2][0]] = v2
            data['thresholds'][category] = tags

        try:
            response = requests.post(
                callback_url,
                headers=headers,
                data=json.dumps(data),
                timeout=60
            )
            if response.status_code == 200:
                print(f"Successfully sent the request on callback url with entry id {response_body['entry_id']}")
            else:
                print("Request not sent successfully.")
                raise Exception(f"Exception occurred while sending request: StatusCode {response.status_code}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Exception occurred while sending request - {e}")

    return "Response handled successfully"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8001", debug=True)
