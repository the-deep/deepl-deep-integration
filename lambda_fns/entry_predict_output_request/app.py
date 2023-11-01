import os
import requests
import json
import logging
import sentry_sdk
from mappings.tags_mapping import get_all_mappings, get_categories
try:
    from lambda_fns.model_info.app import lambda_handler
    model_info_mock_data = json.loads(lambda_handler({"mock": True}, None)["body"])
except ImportError:
    pass

SENTRY_URL = os.environ.get("SENTRY_URL")
ENVIRONMENT = os.environ.get("ENVIRONMENT")

sentry_sdk.init(SENTRY_URL, environment=ENVIRONMENT, attach_stacktrace=True, traces_sample_rate=1.0)

logging.getLogger().setLevel(logging.INFO)

mappings = get_all_mappings()
categories = get_categories()

fake_data = [
   {
      "primary_tags":{
         "sectors":{
            "Agriculture":0.0015192615267421517,
            "Cross":2.266681720228756,
            "Education":0.02295325743034482,
            "Food Security":0.061531245176281245,
            "Health":0.140668327609698,
            "Livelihoods":0.040182591016803465,
            "Logistics":0.005464191199280322,
            "Nutrition":9.93173974469149e-05,
            "Protection":5.455834865570068,
            "Shelter":0.01595675065699551,
            "WASH":0.0018369699578865296
         },
         "subpillars_2d":{
            "At Risk->Number Of People At Risk":7.958003038766037e-05,
            "At Risk->Risk And Vulnerabilities":0.14909714121710171,
            "Capacities & Response->International Response":0.0005300973977060302,
            "Capacities & Response->Local Response":3.6785016277463e-05,
            "Capacities & Response->National Response":0.002878893385915195,
            "Capacities & Response->Number Of People Reached/Response Gaps":0.0015827980435763798,
            "Humanitarian Conditions->Coping Mechanisms":0.006730915305929052,
            "Humanitarian Conditions->Living Standards":0.13377755307234251,
            "Humanitarian Conditions->Number Of People In Need":0.00030424525903072203,
            "Humanitarian Conditions->Physical And Mental Well Being":3.557107225060463,
            "Impact->Driver/Aggravating Factors":0.30262467761834466,
            "Impact->Impact On People":0.1379885245114565,
            "Impact->Impact On Systems, Services And Networks":0.05514782969839871,
            "Impact->Number Of People Affected":0.006860913126729429,
            "Priority Interventions->Expressed By Humanitarian Staff":7.764241470593131e-05,
            "Priority Interventions->Expressed By Population":1.9618319887134326e-05,
            "Priority Needs->Expressed By Humanitarian Staff":1.2330993318495788e-05,
            "Priority Needs->Expressed By Population":0.0005511248533506519
         },
         "subpillars_1d":{
            "Casualties->Dead":0.5277328766309298,
            "Casualties->Injured":0.5389928352087736,
            "Casualties->Missing":0.0024325139949926073,
            "Context->Demography":0.03165506558226687,
            "Context->Economy":0.010170067738120755,
            "Context->Environment":0.010367161731290465,
            "Context->Legal & Policy":0.001767287377585122,
            "Context->Politics":0.012721888593990694,
            "Context->Security & Stability":5.508916079998016,
            "Context->Socio Cultural":0.003907638601958752,
            "Covid-19->Cases":3.329320053227194e-05,
            "Covid-19->Contact Tracing":1.0524275430932241e-07,
            "Covid-19->Deaths":5.623477904248189e-05,
            "Covid-19->Hospitalization & Care":9.923554292375533e-06,
            "Covid-19->Restriction Measures":0.0002665956107312408,
            "Covid-19->Testing":7.267150184845613e-05,
            "Covid-19->Vaccination":7.220470042039569e-05,
            "Displacement->Intentions":2.8656749388270937e-06,
            "Displacement->Local Integration":7.402830026246823e-05,
            "Displacement->Pull Factors":8.282385503359062e-06,
            "Displacement->Push Factors":0.0006505369898290015,
            "Displacement->Type/Numbers/Movements":0.011573675569267042,
            "Humanitarian Access->Number Of People Facing Humanitarian Access Constraints/Humanitarian Access Gaps":0.0016117644716157683,
            "Humanitarian Access->Physical Constraints":0.001055635675584199,
            "Humanitarian Access->Population To Relief":3.701728701344109e-06,
            "Humanitarian Access->Relief To Population":2.0293501537790608e-05,
            "Information And Communication->Communication Means And Preferences":9.698896974441595e-06,
            "Information And Communication->Information Challenges And Barriers":0.00012904413324577035,
            "Information And Communication->Knowledge And Info Gaps (Hum)":0.002071594852688057,
            "Information And Communication->Knowledge And Info Gaps (Pop)":0.008236645306977961,
            "Shock/Event->Hazard & Threats":0.04653984991212686,
            "Shock/Event->Type And Characteristics":0.005213278234891949,
            "Shock/Event->Underlying/Aggravating Factors":0.08061402477324009
         }
      },
      "secondary_tags":{
         "age":{
            "Adult (18 to 59 years old)":9.536670404486358e-05,
            "Children/Youth (5 to 17 years old)":0.0010865677419739466,
            "Infants/Toddlers (<5 years old)":5.143924949259278e-05,
            "Older Persons (60+ years old)":0.00022308759071165696
         },
         "gender":{
            "Female":0.007455993650688065,
            "Male":0.02926515298895538
         },
         "affected_groups":{
            "Asylum Seekers":2.1205758226835425e-07,
            "Host":5.6676799431443214e-05,
            "IDP":0.0016466826006459694,
            "Migrants":4.5306819629331585e-06,
            "Refugees":0.0003480630202202833,
            "Returnees":0.0010307924821972847
         },
         "specific_needs_groups":{
            "Child Head of Household":1.5001008864209293e-07,
            "Chronically Ill":8.45890200354107e-06,
            "Elderly Head of Household":2.563743350947334e-06,
            "Female Head of Household":2.0595144726886407e-06,
            "GBV survivors":4.9045229388866574e-05,
            "Indigenous people":7.791085408825893e-06,
            "LGBTQI+":1.3531972748686322e-06,
            "Minorities":0.0001522377880808728,
            "Persons with Disability":1.2454439340302108e-06,
            "Pregnant or Lactating Women":7.379314550719399e-08,
            "Single Women (including Widows)":2.3683933629096527e-06,
            "Unaccompanied or Separated Children":9.06970538178737e-07
         },
         "severity":{
            "Critical":0.45211867049888327,
            "Major":0.028029342435977676,
            "Minor Problem":0.0002331270297872834,
            "No problem":0.006089172772287081,
            "Of Concern":0.0023042623070068657
         }
      }
   }
]

fake_data_thresholds = {
   "primary_tags":{
      "sectors":{
         "Agriculture":0.14,
         "Cross":0.17,
         "Education":0.1,
         "Food Security":0.14,
         "Health":0.18,
         "Livelihoods":0.14,
         "Logistics":0.1,
         "Nutrition":0.12,
         "Protection":0.15,
         "Shelter":0.18,
         "WASH":0.14
      },
      "subpillars_2d":{
         "At Risk->Number Of People At Risk":0.01,
         "At Risk->Risk And Vulnerabilities":0.11,
         "Capacities & Response->International Response":0.38,
         "Capacities & Response->Local Response":0.01,
         "Capacities & Response->National Response":0.17,
         "Capacities & Response->Number Of People Reached/Response Gaps":0.15,
         "Humanitarian Conditions->Coping Mechanisms":0.09,
         "Humanitarian Conditions->Living Standards":0.13,
         "Humanitarian Conditions->Number Of People In Need":0.07,
         "Humanitarian Conditions->Physical And Mental Well Being":0.16,
         "Impact->Driver/Aggravating Factors":0.15,
         "Impact->Impact On People":0.2,
         "Impact->Impact On Systems, Services And Networks":0.16,
         "Impact->Number Of People Affected":0.05,
         "Priority Interventions->Expressed By Humanitarian Staff":0.45,
         "Priority Interventions->Expressed By Population":0.06,
         "Priority Needs->Expressed By Humanitarian Staff":0.28,
         "Priority Needs->Expressed By Population":0.13
      },
      "subpillars_1d":{
         "Casualties->Dead":0.13,
         "Casualties->Injured":0.04,
         "Casualties->Missing":0.09,
         "Context->Demography":0.14,
         "Context->Economy":0.24,
         "Context->Environment":0.17,
         "Context->Legal & Policy":0.47,
         "Context->Politics":0.22,
         "Context->Security & Stability":0.16,
         "Context->Socio Cultural":0.15,
         "Covid-19->Cases":0.72,
         "Covid-19->Contact Tracing":0.55,
         "Covid-19->Deaths":0.61,
         "Covid-19->Hospitalization & Care":0.3,
         "Covid-19->Restriction Measures":0.23,
         "Covid-19->Testing":0.31,
         "Covid-19->Vaccination":0.39,
         "Displacement->Intentions":0.15,
         "Displacement->Local Integration":0.13,
         "Displacement->Pull Factors":0.09,
         "Displacement->Push Factors":0.26,
         "Displacement->Type/Numbers/Movements":0.31,
         "Humanitarian Access->Number Of People Facing Humanitarian Access Constraints/Humanitarian Access Gaps":0.09,
         "Humanitarian Access->Physical Constraints":0.16,
         "Humanitarian Access->Population To Relief":0.16,
         "Humanitarian Access->Relief To Population":0.22,
         "Information And Communication->Communication Means And Preferences":0.21,
         "Information And Communication->Information Challenges And Barriers":0.04,
         "Information And Communication->Knowledge And Info Gaps (Hum)":0.07,
         "Information And Communication->Knowledge And Info Gaps (Pop)":0.09,
         "Shock/Event->Hazard & Threats":0.24,
         "Shock/Event->Type And Characteristics":0.21,
         "Shock/Event->Underlying/Aggravating Factors":0.05
      }
   },
   "secondary_tags":{
      "age":{
         "Adult (18 to 59 years old)":0.06,
         "Children/Youth (5 to 17 years old)":0.48,
         "Infants/Toddlers (<5 years old)":0.34,
         "Older Persons (60+ years old)":0.16
      },
      "gender":{
         "Female":0.45,
         "Male":0.48
      },
      "affected_groups":{
         "Asylum Seekers":0.66,
         "Host":0.3,
         "IDP":0.36,
         "Migrants":0.23,
         "Refugees":0.58,
         "Returnees":0.3
      },
      "specific_needs_groups":{
         "Child Head of Household":0.29,
         "Chronically Ill":0.45,
         "Elderly Head of Household":0.03,
         "Female Head of Household":0.34,
         "GBV survivors":0.37,
         "Indigenous people":0.25,
         "LGBTQI+":0.07,
         "Minorities":0.11,
         "Persons with Disability":0.43,
         "Pregnant or Lactating Women":0.23,
         "Single Women (including Widows)":0.06,
         "Unaccompanied or Separated Children":0.36
      },
      "severity":{
         "Critical":0.27,
         "Major":0.11,
         "Minor Problem":0.05,
         "No problem":0.24,
         "Of Concern":0.12
      }
   }
}

fake_selected_tags = {
   "sectors":[
      [
         "Cross",
         "Protection"
      ]
   ],
   "subpillars_2d":[
      [
         "Humanitarian Conditions->Physical And Mental Well Being"
      ]
   ],
   "subpillars_1d":[
      [
         "Context->Security & Stability"
      ]
   ],
   "age":[
      [
         
      ]
   ],
   "gender":[
      [
         
      ]
   ],
   "affected_groups":[
      [
         
      ]
   ],
   "specific_needs_groups":[
      [
         
      ]
   ],
   "severity":[
      [
         "Critical"
      ]
   ]
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
    for prim_tags_key, prim_key_val in pred_data[0]["primary_tags"].items():
        tags = {}
        if prim_tags_key in categories:
            category = categories[prim_tags_key][0]
            tags[category] = {}

            for tag_key, tag_val in prim_key_val.items():
                tag = mappings[tag_key][0]
                tags[category][tag] = {}
                tags[category][tag]["prediction"] = round(tag_val, 15)
                tags[category][tag]["threshold"] = round(get_threshold_primary_value(prim_tags_key, tag_key), 15)
                tags[category][tag]["is_selected"] = check_selected_tag(prim_tags_key, tag_key)
        all_tags_pred.update(tags)

    for sec_tags_key, sec_tags_val in pred_data[0]["secondary_tags"].items():
        tags = {}
        if sec_tags_key in categories:
            category = categories[sec_tags_key][0]
            tags[category] = {}

            for tag_key, tag_val in sec_tags_val.items():
                tag = mappings[tag_key][0]
                tags[category][tag] = {}
                tags[category][tag]["prediction"] = round(tag_val, 15)
                tags[category][tag]["threshold"] = round(get_threshold_secondary_value(sec_tags_key, tag_key), 15)
                tags[category][tag]["is_selected"] = check_selected_tag(sec_tags_key, tag_key)
        all_tags_pred.update(tags)

    demographic_grp_id = categories['demographic_group'][0]
    tags = {}
    tags[demographic_grp_id] = {}
    for age_key, age_val in pred_data[0]["secondary_tags"]["age"].items():
        for gender_key, gender_val in pred_data[0]["secondary_tags"]["gender"].items():
            demographic_key = f"{gender_key} {age_key}"

            if demographic_key in mappings:
                tag = mappings[demographic_key][0]
                tags[demographic_grp_id][tag] = {}
                tags[demographic_grp_id][tag]["prediction"] = -1  # ignore the prediction value
                tags[demographic_grp_id][tag]["threshold"] = -1   # ignore the threshold value
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
            main_model_preds["model_info"] = model_info_mock_data["main_model"]

            geolocation_preds = {}
            geolocation_preds["model_info"] = model_info_mock_data["geolocation"]
            geolocation_preds["values"] = geolocations_mock
            geolocation_preds["prediction_status"] = 1

            reliability_preds = {}
            reliability_preds["model_info"] = model_info_mock_data["reliability"]
            reliability_preds["tags"] = get_reliability_enum_mappings(reliability_mock)
            reliability_preds["prediction_status"] = 1

            all_models.append(main_model_preds)
            all_models.append(geolocation_preds)
            all_models.append(reliability_preds)

            all_predictions.append({
                "client_id": entry["client_id"],
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
        model_info = json.loads(record['messageAttributes']['model_info']['stringValue'])

        all_models = []
        main_model_preds = {}
        main_model_preds["tags"] = get_model_enum_mappings(pred_tags, pred_thresholds, tags_selected)
        main_model_preds["prediction_status"] = prediction_status
        main_model_preds["model_info"] = model_info["main_model"]

        geolocation_preds = {}
        geolocation_preds["model_info"] = model_info["geolocation"]
        geolocation_preds["values"] = geolocations
        geolocation_preds["prediction_status"] = 1

        reliability_preds = {}
        reliability_preds["model_info"] = model_info["reliability"]
        reliability_preds["tags"] = get_reliability_enum_mappings(reliability_score)
        reliability_preds["prediction_status"] = 1 if reliability_score.strip() else 0

        all_models.append(main_model_preds)
        all_models.append(geolocation_preds)
        all_models.append(reliability_preds)

        try:
            logging.info(json.dumps({
                'client_id': entry_id,
                'model_preds': all_models
            }))
            response = requests.post(
                callback_url,
                headers=headers,
                data=json.dumps({
                    'client_id': entry_id,
                    'model_preds': all_models
                }),
                timeout=60
            )
            if response.status_code == 200:
                logging.info(f"Successfully sent the request on callback url {callback_url} with client id {entry_id}")
            else:
                logging.error(f"Request not sent successfully on {callback_url} with {response.content}")
                err_resp = response.json()
                if "errors" in err_resp and "clientId" not in err_resp["errors"]:
                    raise Exception(f"Exception occurred while sending request with StatusCode {response.status_code}")
                else:
                    logging.info('ClientId is invalid. Not sending the request anymore.')
                    return {
                        "statusCode": 200,
                        "body": "ClientId is invalid. Not sending the request anymore."
                    }
        except requests.exceptions.RequestException as e:
            raise Exception(f"Exception occurred while sending request - {e}")

    return {
        "statusCode": 200,
        "body": "Successfully sent on the callback url"
    }
