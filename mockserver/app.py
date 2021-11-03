import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from flask import Flask, request
from lambda_fns.extract_docs.app import process_docs

app = Flask(__name__)


@app.route('/')
def homepage():
    return 'Welcome to mock server'


@app.route('/extract_docs', methods=['POST'])
def extract_documents():
    body = request.get_json()

    event = {}

    event['mock'] = True
    event['urls'] = body['urls']

    response = process_docs(event, None)

    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)