import json
from mappings.tags_mapping import get_vf_list


def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps(get_vf_list())
    }
