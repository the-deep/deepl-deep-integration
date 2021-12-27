import requests
import json

from mappings.tags_mapping import get_all_mappings, map_categories_subpillars

subpillars_mapping = map_categories_subpillars()
mappings = get_all_mappings()


def get_subpillars_mapping(data):
    processed_predictions = {}
    processed_thresholds = {}
    for k1, v1 in data[0].items():  # predictions
        if k1 in subpillars_mapping.keys():
            if subpillars_mapping[k1] not in processed_predictions:
                processed_predictions[subpillars_mapping[k1]] = v1
            else:
                for i, kv in enumerate(processed_predictions[subpillars_mapping[k1]]):
                    processed_predictions[subpillars_mapping[k1]][i].update(v1[i])

    for k1, v1 in data[1].items():  # thresholds
        if k1 in subpillars_mapping.keys():
            if subpillars_mapping[k1] not in processed_thresholds:
                processed_thresholds[subpillars_mapping[k1]] = v1
            else:
                processed_thresholds[subpillars_mapping[k1]].update(v1)

    return processed_predictions, processed_thresholds


def mapping_name_enum(entry_id, predictions, thresholds):
    data = {
        'predictions': {},
        'thresholds': {},
        'versions': {}
    }

    data['entry_id'] = entry_id
    for k1, v1 in predictions.items():
        category = mappings[k1][0]
        tags = {}
        versions = {}
        for k2, v2 in v1[0].items():
            if k2 in mappings:
                tags[mappings[k2][0]] = v2
                versions[mappings[k2][0]] = mappings[k2][1]
        data['predictions'][category] = tags
        data['versions'][category] = versions

    for k1, v1 in thresholds.items():
        category = mappings[k1][0]
        tags = {}
        for k2, v2 in v1.items():
            if k2 in mappings:
                tags[mappings[k2][0]] = v2
        data['thresholds'][category] = tags

    return data


def entry_predict_output_handler(event, context):
    records = event['Records']

    headers = {
        'Content-Type': 'application/json'
    }

    for record in records:
        entry_id = record['body']
        # entry = record['messageAttributes']['entry']['stringValue']
        predictions = record['messageAttributes']['predictions']['stringValue']
        callback_url = record['messageAttributes']['callback_url']['stringValue']

        preds_lst = json.loads(predictions)

        pp, pt = get_subpillars_mapping(preds_lst)

        final_output = mapping_name_enum(entry_id, pp, pt)

        try:
            response = requests.post(
                callback_url,
                headers=headers,
                data=json.dumps(final_output),
                timeout=60
            )
            if response.status_code == 200:
                print(f"Successfully sent the request on callback url with entry id {entry_id}")
            else:
                print("Request not sent successfully.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Exception occurred while sending request - {e}")

    return {
        'statusCode': 200
    }
