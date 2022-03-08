import requests
import json
import logging
from mappings.tags_mapping import get_all_mappings, get_categories

logging.getLogger().setLevel(logging.INFO)

mappings = get_all_mappings()
categories = get_categories()

fake_data = {
    'primary_tags': {
        'sectors': [{
            'Agriculture': 0.0013131533306455466, 'Education': 0.003010824160731357,
            'Food Security': 0.002566287973119567, 'Health': 2.677955230077108,
            'Livelihoods': 0.01722483797685096, 'Logistics': 0.003670748323202133,
            'Nutrition': 0.0041013412481668045, 'Protection': 0.028100471686700296,
            'Shelter': 0.0035644680749447573, 'WASH': 0.00885658950175879
        }],
        'subpillars_2d': [{
            'At Risk->Number Of People At Risk': 0.00023104241032948875,
            'At Risk->Risk And Vulnerabilities': 0.006840221311261014,
            'Capacities & Response->International Response': 1.51390548675291,
            'Capacities & Response->Local Response': 0.0024619154282845557,
            'Capacities & Response->National Response': 0.19748103480006374,
            'Capacities & Response->Number Of People Reached/Response Gaps': 0.1326687938096572,
            'Humanitarian Conditions->Coping Mechanisms': 0.008473951473004289,
            'Humanitarian Conditions->Living Standards': 0.014394345796770519,
            'Humanitarian Conditions->Number Of People In Need': 0.002753498941479671,
            'Humanitarian Conditions->Physical And Mental Well Being': 0.02261752535293742,
            'Impact->Driver/Aggravating Factors': 0.0028069927602222093,
            'Impact->Impact On People': 0.0035386373796923594,
            'Impact->Impact On Systems, Services And Networks': 0.00474455507679118,
            'Impact->Number Of People Affected': 0.002435182492869596,
            'Priority Interventions->Expressed By Humanitarian Staff': 0.004984116689725355,
            'Priority Interventions->Expressed By Population': 0.0034277827944606543,
            'Priority Needs->Expressed By Humanitarian Staff': 0.0018360981872926156,
            'Priority Needs->Expressed By Population': 0.007651697378605604
        }],
        'subpillars_1d': [{
            'Casualties->Dead': 0.0018779816205746359,
            'Casualties->Injured': 0.0009131004424908987,
            'Casualties->Missing': 0.0010629182305330266,
            'Context->Demography': 0.01951472795739466,
            'Context->Economy': 0.002760568168014288,
            'Context->Environment': 0.001610475469772753,
            'Context->Legal & Policy': 0.0028414463984870143,
            'Context->Politics': 0.0030019306965793175,
            'Context->Security & Stability': 0.0028423364380035887,
            'Context->Socio Cultural': 0.0024926103993921592,
            'Covid-19->Cases': 0.004972799797542393,
            'Covid-19->Contact Tracing': 0.00032880847216941987,
            'Covid-19->Deaths': 0.001167356436152333,
            'Covid-19->Hospitalization & Care': 0.0024493522487762497,
            'Covid-19->Restriction Measures': 0.005428578056718992,
            'Covid-19->Testing': 0.0018874364551392537,
            'Covid-19->Vaccination': 0.0011778841898949057,
            'Displacement->Intentions': 0.0004781786533146116,
            'Displacement->Local Integration': 0.006963967811316252,
            'Displacement->Pull Factors': 0.0003674881209635401,
            'Displacement->Push Factors': 0.0002446720680234501,
            'Displacement->Type/Numbers/Movements': 0.012378716890357043,
            'Humanitarian Access->Number Of People Facing Humanitarian Access Constraints/Humanitarian Access Gaps': 0.001155513591390658,
            'Humanitarian Access->Physical Constraints': 0.0014652756362920627,
            'Humanitarian Access->Population To Relief': 0.001666667767016119,
            'Humanitarian Access->Relief To Population': 0.011259256380385366,
            'Information And Communication->Communication Means And Preferences': 0.007581055563475405,
            'Information And Communication->Information Challenges And Barriers': 0.0003372832482758289,
            'Information And Communication->Knowledge And Info Gaps (Hum)': 0.0009009759297542688,
            'Information And Communication->Knowledge And Info Gaps (Pop)': 0.0007702910806983709,
            'Shock/Event->Hazard & Threats': 0.006979638609387304,
            'Shock/Event->Type And Characteristics': 0.00357941840775311,
            'Shock/Event->Underlying/Aggravating Factors': 0.006321697112391976
        }]
    },
    'secondary_tags': {
        'age': [{
            'Adult (18 to 59 years old)': 0.04068703080217044,
            'Children/Youth (5 to 17 years old)': 0.024587836709212173,
            'Infants/Toddlers (<5 years old)': 0.04259871318936348,
            'Older Persons (60+ years old)': 0.006414494919972342
        }],
        'gender': [{
            'Female': 1.403369450233352,
            'Male': 0.007781315997073596
        }],
        'affected_groups': [{
            'Asylum Seekers': 0.0002758237987769487, 'Host': 0.00997524285181002,
            'IDP': 0.004761773787105261, 'Migrants': 0.000846206055333217,
            'Refugees': 0.0007048035968182376, 'Returnees': 0.007033202674169585
        }],
        'specific_needs_groups': [{
            'Child Head of Household': 0.0002081420534523204,
            'Chronically Ill': 0.0029977605726312978,
            'Elderly Head of Household': 0.0029921820636705627,
            'Female Head of Household': 0.002415977602746959,
            'GBV survivors': 0.020530499899998687,
            'Indigenous people': 0.0028101496774559985,
            'LGBTQI+': 0.00022843408415366598,
            'Minorities': 0.009432899118480036,
            'Persons with Disability': 0.000918924031014155,
            'Pregnant or Lactating Women': 2.0397998848739936,
            'Single Women (including Widows)': 0.007506779511459172,
            'Unaccompanied or Separated Children': 0.00019092757914525768
        }]
    }
}

fake_data_thresholds = {
    'primary_tags': {
        'sectors': {
            'Agriculture': 0.41000000000000003, 'Education': 0.46,
            'Food Security': 0.48, 'Health': 0.36, 'Livelihoods': 0.38,
            'Logistics': 0.5, 'Nutrition': 0.49, 'Protection': 0.58,
            'Shelter': 0.42, 'WASH': 0.53
        },
        'subpillars_2d': {
            'At Risk->Number Of People At Risk': 0.12,
            'At Risk->Risk And Vulnerabilities': 0.41000000000000003,
            'Capacities & Response->International Response': 0.62,
            'Capacities & Response->Local Response': 0.1,
            'Capacities & Response->National Response': 0.43,
            'Capacities & Response->Number Of People Reached/Response Gaps': 0.49,
            'Humanitarian Conditions->Coping Mechanisms': 0.36,
            'Humanitarian Conditions->Living Standards': 0.45,
            'Humanitarian Conditions->Number Of People In Need': 0.31,
            'Humanitarian Conditions->Physical And Mental Well Being': 0.41000000000000003,
            'Impact->Driver/Aggravating Factors': 0.38, 'Impact->Impact On People': 0.33,
            'Impact->Impact On Systems, Services And Networks': 0.45,
            'Impact->Number Of People Affected': 0.24,
            'Priority Interventions->Expressed By Humanitarian Staff': 0.55,
            'Priority Interventions->Expressed By Population': 0.15,
            'Priority Needs->Expressed By Humanitarian Staff': 0.3,
            'Priority Needs->Expressed By Population': 0.25
        },
        'subpillars_1d': {
            'Casualties->Dead': 0.28,
            'Casualties->Injured': 0.13,
            'Casualties->Missing': 0.13, 'Context->Demography': 0.49,
            'Context->Economy': 0.41000000000000003, 'Context->Environment': 0.38,
            'Context->Legal & Policy': 0.31, 'Context->Politics': 0.3,
            'Context->Security & Stability': 0.44, 'Context->Socio Cultural': 0.17,
            'Covid-19->Cases': 0.8, 'Covid-19->Contact Tracing': 0.39,
            'Covid-19->Deaths': 0.81, 'Covid-19->Hospitalization & Care': 0.41000000000000003,
            'Covid-19->Restriction Measures': 0.46, 'Covid-19->Testing': 0.79,
            'Covid-19->Vaccination': 0.54, 'Displacement->Intentions': 0.38,
            'Displacement->Local Integration': 0.25, 'Displacement->Pull Factors': 0.29,
            'Displacement->Push Factors': 0.37, 'Displacement->Type/Numbers/Movements': 0.38,
            'Humanitarian Access->Number Of People Facing Humanitarian Access Constraints/Humanitarian Access Gaps': 0.47000000000000003,
            'Humanitarian Access->Physical Constraints': 0.48,
            'Humanitarian Access->Population To Relief': 0.19,
            'Humanitarian Access->Relief To Population': 0.29,
            'Information And Communication->Communication Means And Preferences': 0.21,
            'Information And Communication->Information Challenges And Barriers': 0.15,
            'Information And Communication->Knowledge And Info Gaps (Hum)': 0.18,
            'Information And Communication->Knowledge And Info Gaps (Pop)': 0.18,
            'Shock/Event->Hazard & Threats': 0.23, 'Shock/Event->Type And Characteristics': 0.2,
            'Shock/Event->Underlying/Aggravating Factors': 0.17
        }
    },
    'secondary_tags': {
        'age': {
            'Adult (18 to 59 years old)': 0.48, 'Children/Youth (5 to 17 years old)': 0.44,
            'Infants/Toddlers (<5 years old)': 0.4, 'Older Persons (60+ years old)': 0.61
        },
        'gender': {
            'Female': 0.71, 'Male': 0.44
        },
        'affected_groups': {
            'Asylum Seekers': 0.73, 'Host': 0.55, 'IDP': 0.67, 'Migrants': 0.75,
            'Refugees': 0.64, 'Returnees': 0.53
        },
        'specific_needs_groups': {
            'Child Head of Household': 0.25, 'Chronically Ill': 0.58, 'Elderly Head of Household': 0.14,
            'Female Head of Household': 0.48, 'GBV survivors': 0.78, 'Indigenous people': 0.13,
            'LGBTQI+': 0.41000000000000003, 'Minorities': 0.59, 'Persons with Disability': 0.56,
            'Pregnant or Lactating Women': 0.49, 'Single Women (including Widows)': 0.2,
            'Unaccompanied or Separated Children': 0.6
        }
    }
}

fake_selected_tags = {
    'sectors': [
        ['Health']
    ],
    'subpillars_2d': [
        ['Capacities & Response->International Response']
    ],
    'subpillars_1d': [
        []
    ],
    'gender': [
        ['Female']
    ],
    'age': [
        ['Adult (18 to 59 years old)']
    ],
    'severity': [
        []
    ],
    'specific_needs_groups': [
        ['Pregnant or Lactating Women']
    ],
    'affected_groups': [
        []
    ]
}

model_info_mock = {
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
}


def get_model_enum_mappings(pred_data, thresholds, selected_tags):
    def get_threshold_primary_value(pt_key, t_key):
        return thresholds['primary_tags'][pt_key][t_key]

    def get_threshold_secondary_value(st_key, t_key):
        return thresholds['secondary_tags'][st_key][t_key]

    def check_selected_tag(category, tag):
        return True if tag in selected_tags[category][0] else False

    def check_demo_grp_selected_tag(gender, age):
        return True if gender in selected_tags["gender"][0] and age in selected_tags["age"][0] else False

    all_tags_pred = {}
    for prim_tags_key, prim_key_val in pred_data["primary_tags"].items():
        tags = {}
        if prim_tags_key in categories:
            category = categories[prim_tags_key][0]
            tags[category] = {}

            for tag_key, tag_val in prim_key_val[0].items():
                tag = mappings[tag_key][0]
                tags[category][tag] = {}
                tags[category][tag]["prediction"] = tag_val
                tags[category][tag]["threshold"] = get_threshold_primary_value(prim_tags_key, tag_key)
                tags[category][tag]["is_selected"] = check_selected_tag(prim_tags_key, tag_key)
        all_tags_pred.update(tags)

    for sec_tags_key, sec_tags_val in pred_data["secondary_tags"].items():
        tags = {}
        if sec_tags_key in categories:
            category = categories[sec_tags_key][0]
            tags[category] = {}

            for tag_key, tag_val in sec_tags_val[0].items():
                tag = mappings[tag_key][0]
                tags[category][tag] = {}
                tags[category][tag]["prediction"] = tag_val
                tags[category][tag]["threshold"] = get_threshold_secondary_value(sec_tags_key, tag_key)
                tags[category][tag]["is_selected"] = check_selected_tag(sec_tags_key, tag_key)
        all_tags_pred.update(tags)

    demographic_grp_id = categories['demographic_group'][0]
    tags = {}
    tags[demographic_grp_id] = {}
    for age_key, age_val in pred_data["secondary_tags"]["age"][0].items():
        for gender_key, gender_val in pred_data["secondary_tags"]["gender"][0].items():
            demographic_key = f"{gender_key} {age_key}"

            if demographic_key in mappings:
                tag = mappings[demographic_key][0]
                tags[demographic_grp_id][tag] = {}
                tags[demographic_grp_id][tag]["prediction"] = 0.5
                tags[demographic_grp_id][tag]["threshold"] = 0.5
                tags[demographic_grp_id][tag]["is_selected"] = check_demo_grp_selected_tag(gender_key, age_key)
    all_tags_pred.update(tags)

    return all_tags_pred


def get_reliability_enum_mappings(reliability_score):
    reliability_tag = {}
    if reliability_score and reliability_score.strip():
        reliability_tag[categories["reliability"][0]] = {
            mappings[reliability_score][0]: {
                "is_selected": True
            }
        }
    return reliability_tag


def entry_predict_output_handler(event, context):
    if 'mock' in event and event['mock']:
        all_predictions = []
        entries = event['entries']
        prediction_status = 1
        geolocations_mock = ['Nepal', 'Paris']
        reliability_mock = "Usually reliable"

        for entry in entries:
            all_models = []
            main_model_preds = {}
            main_model_preds["tags"] = get_model_enum_mappings(fake_data, fake_data_thresholds, fake_selected_tags)
            main_model_preds["prediction_status"] = prediction_status
            main_model_preds["model_info"] = model_info_mock["main_model"]

            geolocation_preds = {}
            geolocation_preds["model_info"] = model_info_mock["geolocation"]
            geolocation_preds["values"] = geolocations_mock
            geolocation_preds["prediction_status"] = 1

            reliability_preds = {}
            reliability_preds["model_info"] = model_info_mock["reliability"]
            reliability_preds["tags"] = get_reliability_enum_mappings(reliability_mock)
            reliability_preds["prediction_status"] = 1

            all_models.append(main_model_preds)
            all_models.append(geolocation_preds)
            all_models.append(reliability_preds)

            all_predictions.append({
                "entry_id": entry["entry_id"],
                "model_preds": all_models
            })
        return all_predictions

    records = event['Records']

    headers = {
        'Content-Type': 'application/json'
    }

    for record in records:
        entry_id = record['body']
        # entry = record['messageAttributes']['entry']['stringValue']
        pred_tags = json.loads(record['messageAttributes']['pred_tags']['stringValue'])
        pred_thresholds = json.loads(record['messageAttributes']['pred_thresholds']['stringValue'])
        tags_selected = json.loads(record['messageAttributes']['tags_selected']['stringValue'])
        callback_url = record['messageAttributes']['callback_url']['stringValue']
        prediction_status = record['messageAttributes']['prediction_status']['stringValue']
        geolocations = json.loads(record['messageAttributes']['geolocations']['stringValue'])
        reliability_score = record['messageAttributes']['reliability_score']['stringValue']

        all_models = []
        main_model_preds = {}
        main_model_preds["tags"] = get_model_enum_mappings(pred_tags, pred_thresholds, tags_selected)
        main_model_preds["prediction_status"] = prediction_status
        main_model_preds["model_info"] = model_info_mock["main_model"]

        geolocation_preds = {}
        geolocation_preds["model_info"] = model_info_mock["geolocation"]
        geolocation_preds["values"] = geolocations
        geolocation_preds["prediction_status"] = 1

        reliability_preds = {}
        reliability_preds["model_info"] = model_info_mock["reliability"]
        reliability_preds["tags"] = get_reliability_enum_mappings(reliability_score)
        reliability_preds["prediction_status"] = 1 if reliability_score.strip() else 0

        all_models.append(main_model_preds)
        all_models.append(geolocation_preds)
        all_models.append(reliability_preds)

        try:
            logging.info(json.dumps({
                'entry_id': entry_id,
                'model_preds': all_models
            }))
            response = requests.post(
                callback_url,
                headers=headers,
                data=json.dumps({
                    'entry_id': entry_id,
                    'model_preds': all_models
                }),
                timeout=60
            )
            if response.status_code == 200:
                logging.info(f"Successfully sent the request on callback url with entry id {entry_id}")
            else:
                logging.error("Request not sent successfully.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Exception occurred while sending request - {e}")

    return {
        'statusCode': 200
    }
