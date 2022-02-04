import requests
import json

from mappings.tags_mapping import get_all_mappings, get_categories, map_categories_subpillars

subpillars_mapping = map_categories_subpillars()
mappings = get_all_mappings()
categories = get_categories()

fake_data = {
    'raw_predictions': {
        'subpillars': [{
            'At Risk->Number Of People At Risk': 0.004270137287676334,
            'At Risk->Risk And Vulnerabilities': 0.07127775529096293,
            'Capacities & Response->International Response': 1.331607320091941,
            'Capacities & Response->Local Response': 0.020646801414458377,
            'Capacities & Response->National Response': 0.4925251007080078,
            'Capacities & Response->Number Of People Reached/Response Gaps': 0.7790635240838882,
            'Casualties->Dead': 0.01773698255419731,
            'Casualties->Injured': 0.005923864185152685,
            'Casualties->Missing': 0.027860794216394424,
            'Context->Demography': 0.19150988721266024,
            'Context->Economy': 0.03239802516451696,
            'Context->Environment': 0.0266275278502895,
            'Context->Legal & Policy': 0.02023347094655037,
            'Context->Politics': 0.025336206068887427,
            'Context->Security & Stability': 0.03668013150277345,
            'Context->Socio Cultural': 0.025737904669607386,
            'Covid-19->Cases': 0.038027222035452724,
            'Covid-19->Contact Tracing': 0.019042426720261574,
            'Covid-19->Deaths': 0.024089267527734912,
            'Covid-19->Hospitalization & Care': 0.055941250608410945,
            'Covid-19->Restriction Measures': 0.03760255640372634,
            'Covid-19->Testing': 0.04087602895385814,
            'Covid-19->Vaccination': 0.03429351405042117,
            'Displacement->Intentions': 0.0036236922309364913,
            'Displacement->Local Integration': 0.026188229980028194,
            'Displacement->Pull Factors': 0.007194649272908768,
            'Displacement->Push Factors': 0.011826851942504827,
            'Displacement->Type/Numbers/Movements': 0.09764697816636828,
            'Humanitarian Access->Number Of People Facing Humanitarian Access Constraints/Humanitarian Access Gaps': 0.04048,
            'Humanitarian Access->Physical Constraints': 0.020004283370716233,
            'Humanitarian Access->Population To Relief': 0.02886151778511703,
            'Humanitarian Access->Relief To Population': 0.08136125979945064,
            'Humanitarian Conditions->Coping Mechanisms': 0.07366700826779655,
            'Humanitarian Conditions->Living Standards': 0.08120508459599121,
            'Humanitarian Conditions->Number Of People In Need': 0.049229882853595835,
            'Humanitarian Conditions->Physical And Mental Well Being': 0.1497238576412201,
            'Impact->Driver/Aggravating Factors': 0.05259623184152271,
            'Impact->Impact On People': 0.048762670856841064,
            'Impact->Impact On Systems, Services And Networks': 0.07096444411824147,
            'Impact->Number Of People Affected': 0.0289971218444407,
            'Information And Communication->Communication Means And Preferences': 0.03272266437609991,
            'Information And Communication->Information Challenges And Barriers': 0.003942607768944331,
            'Information And Communication->Knowledge And Info Gaps (Hum)': 0.013623181730508804,
            'Information And Communication->Knowledge And Info Gaps (Pop)': 0.009105289204707068,
            'Priority Interventions->Expressed By Humanitarian Staff': 0.04735273108178494,
            'Priority Interventions->Expressed By Population': 0.022244140313103282,
            'Priority Needs->Expressed By Humanitarian Staff': 0.02912785443994734,
            'Priority Needs->Expressed By Population': 0.06317001368318285,
            'Shock/Event->Hazard & Threats': 0.05274482899241977,
            'Shock/Event->Type And Characteristics': 0.019818637520074844,
            'Shock/Event->Underlying/Aggravating Factors': 0.07190693702016557}],
        'sectors': [{
            'Agriculture': 0.05120900645852089,
            'Education': 0.05305534398013895,
            'Food Security': 0.0618496835231781,
            'Health': 1.618701742406477,
            'Livelihoods': 0.1329706003100185,
            'Logistics': 0.06410405039787292,
            'Nutrition': 0.07127126057942708,
            'Protection': 0.14047556157623017,
            'Shelter': 0.07421194504086788,
            'WASH': 0.0428224541246891}],
        'secondary_tags': [{
            'affected_groups_level_3_kw->Asylum Seekers': 0.0209003354289702,
            'affected_groups_level_3_kw->Host': 0.024959675612903777,
            'affected_groups_level_3_kw->IDP': 0.05839878862554376,
            'affected_groups_level_3_kw->Migrants': 0.01291824979180435,
            'affected_groups_level_3_kw->Refugees': 0.025602160179513996,
            'affected_groups_level_3_kw->Returnees': 0.09169663601326491,
            'age_kw_pred->Adult (18 to 59 years old)': 1.4639190652153709,
            'age_kw_pred->Children/Youth (5 to 17 years old)': 0.13173515834505595,
            'age_kw_pred->Infants/Toddlers (<5 years old)': 0.09468458019770108,
            'age_kw_pred->Older Persons (60+ years old)': 0.04525523943205675,
            'gender_kw_pred->Female': 1.5787005424499512,
            'gender_kw_pred->Male': 0.09616524109552647,
            'severity->Critical': 0.1511390060186386,
            'severity->Major': 0.15994030982255936,
            'severity->Minor Problem': 0.10206978768110275,
            'severity->No problem': 0.2135063045554691,
            'severity->Of Concern': 0.20366763696074486,
            'specific_needs_groups->Child Head of Household': 0.08046364630846416,
            'specific_needs_groups->Chronically Ill': 0.18402323352568076,
            'specific_needs_groups->Elderly Head of Household': 0.11073422928651175,
            'specific_needs_groups->Female Head of Household': 0.15970195733731793,
            'specific_needs_groups->GBV survivors': 0.29262131452560425,
            'specific_needs_groups->Indigenous people': 0.0469617903805696,
            'specific_needs_groups->LGBTQI+': 0.020378202933705212,
            'specific_needs_groups->Minorities': 0.07438406348228455,
            'specific_needs_groups->Persons with Disability': 0.07348087383434176,
            'specific_needs_groups->Pregnant or Lactating Women': 1.7958825542813257,
            'specific_needs_groups->Single Women (including Widows)': 0.3080255351960659,
            'specific_needs_groups->Unaccompanied or Separated Children': 0.06830143697914623}]},
    'thresholds': {
        'subpillars': {
            'At Risk->Number Of People At Risk': 0.24,
            'At Risk->Risk And Vulnerabilities': 0.43,
            'Capacities & Response->International Response': 0.55,
            'Capacities & Response->Local Response': 0.19,
            'Capacities & Response->National Response': 0.44,
            'Capacities & Response->Number Of People Reached/Response Gaps': 0.47000000000000003,
            'Casualties->Dead': 0.55, 'Casualties->Injured': 0.34,
            'Casualties->Missing': 0.31,
            'Context->Demography': 0.41000000000000003,
            'Context->Economy': 0.41000000000000003,
            'Context->Environment': 0.31,
            'Context->Legal & Policy': 0.5,
            'Context->Politics': 0.34,
            'Context->Security & Stability': 0.46,
            'Context->Socio Cultural': 0.34,
            'Covid-19->Cases': 0.64,
            'Covid-19->Contact Tracing': 0.46,
            'Covid-19->Deaths': 0.74,
            'Covid-19->Hospitalization & Care': 0.43,
            'Covid-19->Restriction Measures': 0.48,
            'Covid-19->Testing': 0.53, 'Covid-19->Vaccination': 0.61,
            'Displacement->Intentions': 0.53, 'Displacement->Local Integration': 0.46,
            'Displacement->Pull Factors': 0.42, 'Displacement->Push Factors': 0.52,
            'Displacement->Type/Numbers/Movements': 0.45,
            'Humanitarian Access->Number Of People Facing Humanitarian Access Constraints/Humanitarian Access Gaps': 0.33,
            'Humanitarian Access->Physical Constraints': 0.42, 'Humanitarian Access->Population To Relief': 0.24,
            'Humanitarian Access->Relief To Population': 0.32,
            'Humanitarian Conditions->Coping Mechanisms': 0.46,
            'Humanitarian Conditions->Living Standards': 0.46, 'Humanitarian Conditions->Number Of People In Need': 0.38,
            'Humanitarian Conditions->Physical And Mental Well Being': 0.5,
            'Impact->Driver/Aggravating Factors': 0.46,
            'Impact->Impact On People': 0.47000000000000003,
            'Impact->Impact On Systems, Services And Networks': 0.48,
            'Impact->Number Of People Affected': 0.4,
            'Information And Communication->Communication Means And Preferences': 0.3,
            'Information And Communication->Information Challenges And Barriers': 0.28,
            'Information And Communication->Knowledge And Info Gaps (Hum)': 0.45,
            'Information And Communication->Knowledge And Info Gaps (Pop)': 0.31,
            'Priority Interventions->Expressed By Humanitarian Staff': 0.51,
            'Priority Interventions->Expressed By Population': 0.29,
            'Priority Needs->Expressed By Humanitarian Staff': 0.45,
            'Priority Needs->Expressed By Population': 0.42,
            'Shock/Event->Hazard & Threats': 0.45, 'Shock/Event->Type And Characteristics': 0.42,
            'Shock/Event->Underlying/Aggravating Factors': 0.28},
        'sectors': {
            'Agriculture': 0.5,
            'Education': 0.55,
            'Food Security': 0.5,
            'Health': 0.5700000000000001,
            'Livelihoods': 0.59, 'Logistics': 0.58,
            'Nutrition': 0.51, 'Protection': 0.56,
            'Shelter': 0.52, 'WASH': 0.6},
        'secondary_tags': {
            'affected_groups_level_3_kw->Asylum Seekers': 0.28,
            'affected_groups_level_3_kw->Host': 0.63,
            'affected_groups_level_3_kw->IDP': 0.55,
            'affected_groups_level_3_kw->Migrants': 0.53,
            'affected_groups_level_3_kw->Refugees': 0.59,
            'affected_groups_level_3_kw->Returnees': 0.53,
            'age_kw_pred->Adult (18 to 59 years old)': 0.66,
            'age_kw_pred->Children/Youth (5 to 17 years old)': 0.63,
            'age_kw_pred->Infants/Toddlers (<5 years old)': 0.65,
            'age_kw_pred->Older Persons (60+ years old)': 0.6,
            'gender_kw_pred->Female': 0.6,
            'gender_kw_pred->Male': 0.58,
            'severity->Critical': 0.5, 'severity->Major': 0.44,
            'severity->Minor Problem': 0.18, 'severity->No problem': 0.45,
            'severity->Of Concern': 0.4, 'specific_needs_groups->Child Head of Household': 0.17,
            'specific_needs_groups->Chronically Ill': 0.33, 'specific_needs_groups->Elderly Head of Household': 0.15,
            'specific_needs_groups->Female Head of Household': 0.31,
            'specific_needs_groups->GBV survivors': 0.5,
            'specific_needs_groups->Indigenous people': 0.52, 'specific_needs_groups->LGBTQI+': 0.33,
            'specific_needs_groups->Minorities': 0.45, 'specific_needs_groups->Persons with Disability': 0.32,
            'specific_needs_groups->Pregnant or Lactating Women': 0.42,
            'specific_needs_groups->Single Women (including Widows)': 0.12,
            'specific_needs_groups->Unaccompanied or Separated Children': 0.42}}}


def get_enum_mappings(preds_data):
    main_model_preds = {
        'predictions': {},
        'thresholds': {},
        'versions': {}
    }
    for key, val in preds_data['raw_predictions'].items():
        first_item = val[0]
        for tag, pred in first_item.items():
            if key in categories:
                key_id = categories[key][0]
            if tag in mappings.keys():
                tag_id = mappings[tag][0]
                if key_id not in main_model_preds['predictions']:
                    main_model_preds['predictions'][key_id] = {}
                main_model_preds['predictions'][key_id][tag_id] = pred
            else:
                print(f"The Tag {tag} is missing.")

    for key, tag_threshold in preds_data['thresholds'].items():
        for tag, threshold in tag_threshold.items():
            if key in categories:
                key_id = categories[key][0]
            if tag in mappings.keys():
                tag_id = mappings[tag][0]
                if key_id not in main_model_preds['thresholds']:
                    main_model_preds['thresholds'][key_id] = {}
                if key_id not in main_model_preds['versions']:
                    main_model_preds['versions'][key_id] = {}
                main_model_preds['thresholds'][key_id][tag_id] = threshold
                main_model_preds['versions'][key_id][tag_id] = mappings[tag][1]

    return main_model_preds


def entry_predict_output_handler(event, context):
    if 'mock' in event and event['mock']:
        all_predictions = []
        entries = event['entries']
        prediction_status = 1
        geolocations_mock = ['Nepal', 'Paris']
        for entry in entries:
            main_model_preds = get_enum_mappings(fake_data)
            main_model_preds['prediction_status'] = prediction_status

            all_predictions.append({
                'main_model_preds': main_model_preds,
                'geolocations_preds': geolocations_mock
            })
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
            geolocations = json.loads(record['messageAttributes']['geolocations']['stringValue'])

            preds_lst = json.loads(predictions)

            main_model_preds = get_enum_mappings(preds_lst)
            main_model_preds['prediction_status'] = prediction_status

            try:
                response = requests.post(
                    callback_url,
                    headers=headers,
                    data=json.dumps({'main_model_preds': main_model_preds, 'geolocations_preds': geolocations}),
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
