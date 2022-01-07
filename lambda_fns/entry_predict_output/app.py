import requests
import json

from mappings.tags_mapping import get_all_mappings, map_categories_subpillars

subpillars_mapping = map_categories_subpillars()
mappings = get_all_mappings()

fake_data = [{
    'sectors': [{
        'Agriculture': 4.4552652980200946e-05,
        'Education': 0.0006393258552313507,
        'Food Security': 0.0007695988866454754,
        'Health': 2.0288994117658965,
        'Livelihoods': 0.0027210856585398965,
        'Logistics': 0.00011781198059287952,
        'NOT_MAPPED': 0.0001796700113724607,
        'Nutrition': 0.0012666034308495,
        'Protection': 0.001404099185169945,
        'Shelter': 0.000824810834681808,
        'WASH': 0.0025559339502995663
    }],
    'present_prim_tags': [
        {'sectors': 1.7443921078335156, 'subpillars_1d': 0.27051111062367755, 'subpillars_2d': 1.125618815422058}], 
    'pillars_2d': [
        {
            'At Risk': 0.014071312866040638, 'Capacities & Response': 0.9037117747699512,
            'Humanitarian Conditions': 0.6109961349031199, 'Impact': 0.08877085832258066, 'NOT_MAPPED': 0.18958856189061724,
            'Priority Interventions': 0.0019680088813844566, 'Priority Needs': 0.0031425298657268286
        },
        {
            'At Risk': 0.0139712356030941, 'Capacities & Response': 0.5527079981916091,
            'Humanitarian Conditions': 1.1584259893583215, 'Impact': 0.12869075872004032, 'NOT_MAPPED': 0.1346996615803431,
            'Priority Interventions': 0.001594731175164516, 'Priority Needs': 0.0026255864650011063
        }
    ],
    'pillars_1d': [
        {
            'Casualties': 0.003412537625990808, 'Context': 0.02325245295651257, 'Covid-19': 0.44976268241654577,
            'Displacement': 0.009790685855680041, 'Humanitarian Access': 0.002306541621995469,
            'Information And Communication': 0.036622151466352594, 'NOT_MAPPED': 1.0777293394009273,
            'Shock/Event': 0.16493414613333615
        },
        {
            'Casualties': 0.003208380439900793, 'Context': 0.02115225652232766, 'Covid-19': 0.43925273774275136,
            'Displacement': 0.022146134740776487, 'Humanitarian Access': 0.0014709733659401536,
            'Information And Communication': 0.017782342287578752, 'NOT_MAPPED': 0.7329113781452179,
            'Shock/Event': 0.3287952731956135
        }
    ],
    'impact_capresp_humcond': [
        {
            'Capacities & Response->International Response': 0.07528654485940933,
            'Capacities & Response->Local Response': 0.00020584032297067873,
            'Capacities & Response->National Response': 2.33131421578897,
            'Capacities & Response->Number Of People Reached/Response Gaps': 0.03508530895818363,
            'Humanitarian Conditions->Coping Mechanisms': 0.003846486166973288,
            'Humanitarian Conditions->Living Standards': 0.25096290358682954,
            'Humanitarian Conditions->Number Of People In Need': 0.0005299710028339177,
            'Humanitarian Conditions->Physical And Mental Well Being': 0.08303534984588623,
            'Impact->Driver/Aggravating Factors': 0.005122622112847037,
            'Impact->Impact On People': 0.027884856205094944,
            'Impact->Impact On Systems, Services And Networks': 0.06305176851361297,
            'Impact->Number Of People Affected': 0.0006419112145926596
        }
    ],
    'need_intervention_risk': [
        {
            'At Risk->Number Of People At Risk': 0.00029756879368319345,
            'At Risk->Risk And Vulnerabilities': 0.09423873963810149,
            'Priority Interventions->Expressed By Humanitarian Staff': 1.4020784033669365,
            'Priority Interventions->Expressed By Population': 0.0954590504989028,
            'Priority Needs->Expressed By Humanitarian Staff': 0.4301432626588004,
            'Priority Needs->Expressed By Population': 0.08459019785126051
        },
        {
            'At Risk->Number Of People At Risk': 0.00010954293732841809,
            'At Risk->Risk And Vulnerabilities': 0.04522786253974551,
            'Priority Interventions->Expressed By Humanitarian Staff': 1.5009298368736548,
            'Priority Interventions->Expressed By Population': 0.03515536276002725,
            'Priority Needs->Expressed By Humanitarian Staff': 0.18193615334374563,
            'Priority Needs->Expressed By Population': 0.13003668282181025
        }
    ],
    'context_covid': [
        {
            'Context->Demography': 0.001032184361695097, 'Context->Economy': 0.00699733341620727,
            'Context->Environment': 0.00041005110168563467, 'Context->Legal & Policy': 0.007072312938463357,
            'Context->Politics': 0.07354221394601858, 'Context->Security & Stability': 0.008455046022740694,
            'Context->Socio Cultural': 0.0014313508290797472, 'Covid-19->Cases': 0.011693374677137894,
            'Covid-19->Contact Tracing': 0.0002544779730769359, 'Covid-19->Deaths': 6.76133053135485e-05,
            'Covid-19->Hospitalization & Care': 0.00012371650276084742, 'Covid-19->Restriction Measures': 0.07524518917004268,
            'Covid-19->Testing': 0.9760316075949834, 'Covid-19->Vaccination': 0.000740400601869389
        }
    ],
    'displacement_shockevent': [
        {
            'Displacement->Intentions': 0.0004663542919540002, 'Displacement->Local Integration': 0.002901282456076267,
            'Displacement->Pull Factors': 0.0010130269066920797, 'Displacement->Push Factors': 0.021304991096258163,
            'Displacement->Type/Numbers/Movements': 0.20951724104713973, 'Shock/Event->Hazard & Threats': 1.2634064312334412,
            'Shock/Event->Type And Characteristics': 0.01677578275508069,
            'Shock/Event->Underlying/Aggravating Factors': 0.35870664698236127
        },
        {
            'Displacement->Intentions': 0.0005456410993550284, 'Displacement->Local Integration': 0.004696231145335704,
            'Displacement->Pull Factors': 0.0011058724148346013, 'Displacement->Push Factors': 0.01964313288529714,
            'Displacement->Type/Numbers/Movements': 0.593930587433932, 'Shock/Event->Hazard & Threats': 0.7747167790377582,
            'Shock/Event->Type And Characteristics': 0.013671035660391158,
            'Shock/Event->Underlying/Aggravating Factors': 0.2826770219732733
        }],
    'access_infcom_casualities': [
        {
            'Casualties->Dead': 0.25634305442080774, 'Casualties->Injured': 0.051686998146275684,
            'Casualties->Missing': 0.015421428463675758,
            'Humanitarian Access->Number Of People Facing Humanitarian Access Constraints/Humanitarian Access Gaps': 0.021052659105728653,
            'Humanitarian Access->Physical Constraints': 0.28977797112681647, 'Humanitarian Access->Population To Relief': 0.0033493785215823937,
            'Humanitarian Access->Relief To Population': 0.29718720100142737,
            'Information And Communication->Communication Means And Preferences': 21.184255679448448,
            'Information And Communication->Information Challenges And Barriers': 0.0047589408826421604,
            'Information And Communication->Knowledge And Info Gaps (Hum)': 0.10249406403424789,
            'Information And Communication->Knowledge And Info Gaps (Pop)': 0.023119417684418813
        }
    ]},
    {
        'sectors': {
            'Agriculture': 0.3, 'Education': 0.68, 'Food Security': 0.61, 'Health': 0.49, 'Livelihoods': 0.46,
            'Logistics': 0.47000000000000003, 'NOT_MAPPED': 0.09, 'Nutrition': 0.48, 'Protection': 0.62,
            'Shelter': 0.58, 'WASH': 0.55
        },
        'present_prim_tags': {
            'sectors': 0.44, 'subpillars_1d': 0.45, 'subpillars_2d': 0.56},
        'pillars_2d': {
            'At Risk': 0.35000000000000003, 'Capacities & Response': 0.68, 'Humanitarian Conditions': 0.46, 'Impact': 0.48,
            'NOT_MAPPED': 0.63, 'Priority Interventions': 0.74, 'Priority Needs': 0.5
        },
        'pillars_1d': {
            'Casualties': 0.64, 'Context': 0.48, 'Covid-19': 0.67, 'Displacement': 0.45, 'Humanitarian Access': 0.6,
            'Information And Communication': 0.07, 'NOT_MAPPED': 0.48, 'Shock/Event': 0.44
        },
        'impact_capresp_humcond': {
            'Capacities & Response->International Response': 0.5, 'Capacities & Response->Local Response': 0.07,
            'Capacities & Response->National Response': 0.37,
            'Capacities & Response->Number Of People Reached/Response Gaps': 0.22,
            'Humanitarian Conditions->Coping Mechanisms': 0.48,
            'Humanitarian Conditions->Living Standards': 0.41000000000000003,
            'Humanitarian Conditions->Number Of People In Need': 0.6,
            'Humanitarian Conditions->Physical And Mental Well Being': 0.5,
            'Impact->Driver/Aggravating Factors': 0.36, 'Impact->Impact On People': 0.33,
            'Impact->Impact On Systems, Services And Networks': 0.43, 'Impact->Number Of People Affected': 0.18
        },
        'need_intervention_risk': {
            'At Risk->Number Of People At Risk': 0.78, 'At Risk->Risk And Vulnerabilities': 0.42,
            'Priority Interventions->Expressed By Humanitarian Staff': 0.54,
            'Priority Interventions->Expressed By Population': 0.03,
            'Priority Needs->Expressed By Humanitarian Staff': 0.35000000000000003,
            'Priority Needs->Expressed By Population': 0.48
        },
        'context_covid': {
            'Context->Demography': 0.52, 'Context->Economy': 0.66, 'Context->Environment': 0.35000000000000003,
            'Context->Legal & Policy': 0.72, 'Context->Politics': 0.53, 'Context->Security & Stability': 0.52,
            'Context->Socio Cultural': 0.45, 'Covid-19->Cases': 0.55, 'Covid-19->Contact Tracing': 0.73,
            'Covid-19->Deaths': 0.52, 'Covid-19->Hospitalization & Care': 0.6, 'Covid-19->Restriction Measures': 0.6,
            'Covid-19->Testing': 0.58, 'Covid-19->Vaccination': 0.62
        },
        'displacement_shockevent': {
            'Displacement->Intentions': 0.48, 'Displacement->Local Integration': 0.49, 'Displacement->Pull Factors': 0.19,
            'Displacement->Push Factors': 0.45, 'Displacement->Type/Numbers/Movements': 0.5700000000000001,
            'Shock/Event->Hazard & Threats': 0.54, 'Shock/Event->Type And Characteristics': 0.47000000000000003,
            'Shock/Event->Underlying/Aggravating Factors': 0.34
        },
        'access_infcom_casualities': {
            'Casualties->Dead': 0.68, 'Casualties->Injured': 0.48, 'Casualties->Missing': 0.55,
            'Humanitarian Access->Number Of People Facing Humanitarian Access Constraints/Humanitarian Access Gaps': 0.34,
            'Humanitarian Access->Physical Constraints': 0.44, 'Humanitarian Access->Population To Relief': 0.33,
            'Humanitarian Access->Relief To Population': 0.22,
            'Information And Communication->Communication Means And Preferences': 0.03,
            'Information And Communication->Information Challenges And Barriers': 0.44,
            'Information And Communication->Knowledge And Info Gaps (Hum)': 0.49,
            'Information And Communication->Knowledge And Info Gaps (Pop)': 0.28
        }
    }
]


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


def mapping_name_enum(entry_id, predictions, thresholds, prediction_status):
    data = {
        'predictions': {},
        'thresholds': {},
        'versions': {}
    }

    data['entry_id'] = entry_id
    data['prediction_status'] = prediction_status
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
    if 'mock' in event and event['mock']:
        all_predictions = []
        entries = event['entries']
        prediction_status = 1
        geolocations_mock = ['Nepal', 'Paris']
        for entry in entries:
            pp, pt = get_subpillars_mapping(fake_data)

            pillars_output = mapping_name_enum(entry['entry_id'], pp, pt, prediction_status)
            all_predictions.append({'pillars_output': pillars_output, 'geolocations': geolocations_mock})
        return all_predictions

    else:
        records = event['Records']

        headers = {
            'Content-Type': 'application/json'
        }

        for record in records:
            entry_id = record['body']
            # entry = record['messageAttributes']['entry']['stringValue']
            predictions = record['messageAttributes']['predictions']['stringValue']
            callback_url = record['messageAttributes']['callback_url']['stringValue']
            prediction_status = record['messageAttributes']['prediction_status']['stringValue']
            geolocations = record['messageAttributes']['geolocations']['stringValue']

            preds_lst = json.loads(predictions)

            pp, pt = get_subpillars_mapping(preds_lst)

            pillars_output = mapping_name_enum(entry_id, pp, pt, prediction_status)

            try:
                response = requests.post(
                    callback_url,
                    headers=headers,
                    data=json.dumps({'pillars_output': pillars_output, 'geolocations': geolocations}),
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
