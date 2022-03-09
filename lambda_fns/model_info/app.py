import json


def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps({
            "main_model": {
                "id": "all_tags_model",
                "version": "1.0.0"
            },
            "geolocation": {
                "id": "geolocation",
                "version": "1.0.0"
            },
            "reliability": {
                "id": "reliability",
                "version": "1.0.0"
            }
        })
    }
