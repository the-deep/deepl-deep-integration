import os
import json
import boto3

AWS_REGION = os.environ.get("AWS_REGION")
runtime = boto3.client("runtime.sagemaker", region_name="us-east-1")  # todo: update the region later.

ENDPOINT_NAME_1D_MODEL = os.environ.get("EP_NAME_1D_MODEL")


def predict_entry_handler(event, context):
    body = json.loads(event["body"])
    print(body)
    entries = body["entries"]
    data = {
        "columns": ["excerpt"],
        "index": list(range(len(entries))),
        "data": [[entry] for entry in entries],
    }

    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT_NAME_1D_MODEL,
        ContentType="application/json; format=pandas-split",
        Body=json.dumps(data),
    )
    response_body = response["Body"].read()
    print (response_body)

    return_body = {
        "results": response_body,
        "input": event,
    }
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": str(return_body),
    }