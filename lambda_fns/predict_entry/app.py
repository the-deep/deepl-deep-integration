import os
import json
import boto3

DEFAULT_AWS_REGION = "us-east-1"

AWS_REGION = os.environ.get("AWS_REGION", DEFAULT_AWS_REGION)
runtime = boto3.client("runtime.sagemaker", region_name="us-east-1")  # todo: update the region later.

ENDPOINT_NAME_MODEL = os.environ.get("EP_NAME_MODEL")

fake_data = [{
    'column_present': [{
        'age': 0.027165943756699562, 'gender': 0.008588225580751896, 'sectors': 0.8696880340576172,
        'severity': 0.1440506875514984, 'specific_needs_groups': 0.003556417301297188,
        'subpillars_1d': 0.211192786693573, 'subpillars_2d': 0.6162739992141724
    }],
    'sectors': [{
        'Agriculture': 0.0003300844691693783, 'Education': 0.0046178982593119144, 'Food Security': 0.008884105831384659,
        'Health': 0.7998205423355103, 'Livelihoods': 0.014437100850045681, 'Logistics': 0.0007252205978147686,
        'Nutrition': 0.023609966039657593, 'Protection': 0.097443588078022, 'Shelter': 0.00541486032307148,
        'WASH': 0.021994158625602722
    }],
    'severity': [{
        'Critical': 0.323945552110672, 'Major': 0.2642754316329956, 'Minor Problem': 0.00012541725300252438,
        'No problem': 0.022020939737558365, 'Of Concern': 0.25321635603904724
    }],
    'age': [{
        'Adult (18 to 59 years old)': 0.37543609738349915, 'Children/Youth (5 to 17 years old)': 0.790147066116333,
        'Infants/Toddlers (<5 years old)': 0.06683919578790665, 'Older Persons (60+ years old)': 0.11112841963768005
    }],
    'gender': [{
        'Female': 0.9447542428970337, 'Male': 0.32883399724960327
    }],
    'subpillars_1d': [{
        'Casualties->Dead': 0.04435533285140991, 'Casualties->Injured': 0.006503191776573658,
        'Casualties->Missing': 0.0011395137989893556, 'Context->Demography': 0.04126974567770958,
        'Context->Economy': 0.0757586881518364, 'Context->Environment': 0.011730965226888657,
        'Context->Legal & Policy': 0.03758103772997856, 'Context->Politics': 0.02613712102174759,
        'Context->Security & Stability': 0.11285246163606644, 'Context->Socio Cultural': 0.014916954562067986,
        'Covid-19->Cases': 0.1081336960196495, 'Covid-19->Contact Tracing': 0.00917692482471466,
        'Covid-19->Deaths': 0.05601067095994949, 'Covid-19->Hospitalization & Care': 0.0038976152427494526,
        'Covid-19->Restriction Measures': 0.07902296632528305, 'Covid-19->Testing': 0.026262041181325912,
        'Covid-19->Vaccination': 0.043814320117235184, 'Displacement->Intentions': 0.004670116119086742,
        'Displacement->Local Integration': 0.022074149921536446, 'Displacement->Pull Factors': 0.0017036062199622393,
        'Displacement->Push Factors': 0.022912347689270973, 'Displacement->Type/Numbers/Movements': 0.1375022679567337,
        'Humanitarian Access->Number Of People Facing Humanitarian Access Constraints/Humanitarian Access Gaps': 0.005927749909460545,
        'Humanitarian Access->Physical Constraints': 0.014906663447618484,
        'Humanitarian Access->Population To Relief': 0.0002910180191975087,
        'Humanitarian Access->Relief To Population': 0.007220406550914049,
        'Information And Communication->Communication Means And Preferences': 0.0008181931916624308,
        'Information And Communication->Information Challenges And Barriers': 0.00026705829077400267,
        'Information And Communication->Knowledge And Info Gaps (Hum)': 0.003694553393870592,
        'Information And Communication->Knowledge And Info Gaps (Pop)': 0.0014655488776043057,
        'Shock/Event->Hazard & Threats': 0.060984861105680466, 'Shock/Event->Type And Characteristics': 0.01441953144967556,
        'Shock/Event->Underlying/Aggravating Factors': 0.02055468037724495
    }],
    'specific_needs_groups': [{
        'Child Head of Household': 0.0017206069314852357, 'Chronically Ill': 0.0870874673128128,
        'Elderly Head of Household': 0.003888340201228857, 'Female Head of Household': 0.04594024643301964,
        'GBV survivors': 0.09000838547945023, 'Indigenous people': 0.23285317420959473, 'LGBTQI+': 0.04832516983151436,
        'Minorities': 0.12234015762805939, 'Persons with Disability': 0.1481849104166031,
        'Pregnant or Lactating Women': 0.2539842426776886, 'Single Women (including Widows)': 0.011717932298779488,
        'Unaccompanied or Separated Children': 0.07986424118280411
    }],
    'subpillars_2d': [{
        'At Risk->Number Of People At Risk': 0.00026445105322636664, 'At Risk->Risk And Vulnerabilities': 0.1167299821972847,
        'Capacities & Response->International Response': 0.16384711861610413,
        'Capacities & Response->Local Response': 0.00019643644918687642,
        'Capacities & Response->National Response': 0.06674249470233917,
        'Capacities & Response->Number Of People Reached/Response Gaps': 0.017031589522957802,
        'Humanitarian Conditions->Coping Mechanisms': 0.04063984751701355,
        'Humanitarian Conditions->Living Standards': 0.2574504315853119,
        'Humanitarian Conditions->Number Of People In Need': 0.003051605774089694,
        'Humanitarian Conditions->Physical And Mental Well Being': 0.12444109469652176,
        'Impact->Driver/Aggravating Factors': 0.12277168035507202,
        'Impact->Impact On People': 0.11150680482387543,
        'Impact->Impact On Systems, Services And Networks': 0.1322088986635208,
        'Impact->Number Of People Affected': 0.009056051261723042,
        'Priority Interventions->Expressed By Humanitarian Staff': 0.09123516082763672,
        'Priority Interventions->Expressed By Population': 0.00010119302896782756,
        'Priority Needs->Expressed By Humanitarian Staff': 0.011230959556996822,
        'Priority Needs->Expressed By Population': 0.012422597967088223
    }]},
    {'column_present': {
        'age': 0.4, 'gender': 0.41000000000000003, 'sectors': 0.5700000000000001, 'severity': 0.33,
        'specific_needs_groups': 0.27, 'subpillars_1d': 0.44, 'subpillars_2d': 0.64
    },
    'sectors': {
        'Agriculture': 0.12, 'Education': 0.15, 'Food Security': 0.41000000000000003, 'Health': 0.54, 'Livelihoods': 0.24,
        'Logistics': 0.16, 'Nutrition': 0.17, 'Protection': 0.51, 'Shelter': 0.17, 'WASH': 0.42
    },
    'severity': {
        'Critical': 0.48, 'Major': 0.21, 'Minor Problem': 0.03, 'No problem': 0.58, 'Of Concern': 0.24
    },
    'age': {
        'Adult (18 to 59 years old)': 0.36, 'Children/Youth (5 to 17 years old)': 0.74,
        'Infants/Toddlers (<5 years old)': 0.7000000000000001, 'Older Persons (60+ years old)': 0.2
    },
    'gender': {'Female': 0.92, 'Male': 0.42},
    'subpillars_1d': {
        'Casualties->Dead': 0.07, 'Casualties->Injured': 0.03, 'Casualties->Missing': 0.02,
        'Context->Demography': 0.07, 'Context->Economy': 0.09, 'Context->Environment': 0.04, 'Context->Legal & Policy': 0.07,
        'Context->Politics': 0.05, 'Context->Security & Stability': 0.14, 'Context->Socio Cultural': 0.05,
        'Covid-19->Cases': 0.12, 'Covid-19->Contact Tracing': 0.03, 'Covid-19->Deaths': 0.07,
        'Covid-19->Hospitalization & Care': 0.02, 'Covid-19->Restriction Measures': 0.11, 'Covid-19->Testing': 0.05,
        'Covid-19->Vaccination': 0.07, 'Displacement->Intentions': 0.03, 'Displacement->Local Integration': 0.05,
        'Displacement->Pull Factors': 0.02, 'Displacement->Push Factors': 0.04, 'Displacement->Type/Numbers/Movements': 0.15,
        'Humanitarian Access->Number Of People Facing Humanitarian Access Constraints/Humanitarian Access Gaps': 0.03,
        'Humanitarian Access->Physical Constraints': 0.03, 'Humanitarian Access->Population To Relief': 0.02,
        'Humanitarian Access->Relief To Population': 0.03,
        'Information And Communication->Communication Means And Preferences': 0.02,
        'Information And Communication->Information Challenges And Barriers': 0.02,
        'Information And Communication->Knowledge And Info Gaps (Hum)': 0.02,
        'Information And Communication->Knowledge And Info Gaps (Pop)': 0.02,
        'Shock/Event->Hazard & Threats': 0.09, 'Shock/Event->Type And Characteristics': 0.03,
        'Shock/Event->Underlying/Aggravating Factors': 0.04
    },
    'specific_needs_groups': {
        'Child Head of Household': 0.02, 'Chronically Ill': 0.09, 'Elderly Head of Household': 0.02,
        'Female Head of Household': 0.06, 'GBV survivors': 0.11, 'Indigenous people': 0.23, 'LGBTQI+': 0.05,
        'Minorities': 0.13, 'Persons with Disability': 0.17, 'Pregnant or Lactating Women': 0.26,
        'Single Women (including Widows)': 0.03, 'Unaccompanied or Separated Children': 0.1
    },
    'subpillars_2d': {
        'At Risk->Number Of People At Risk': 0.02, 'At Risk->Risk And Vulnerabilities': 0.1,
        'Capacities & Response->International Response': 0.17, 'Capacities & Response->Local Response': 0.02,
        'Capacities & Response->National Response': 0.07,
        'Capacities & Response->Number Of People Reached/Response Gaps': 0.05,
        'Humanitarian Conditions->Coping Mechanisms': 0.06, 'Humanitarian Conditions->Living Standards': 0.28,
        'Humanitarian Conditions->Number Of People In Need': 0.03,
        'Humanitarian Conditions->Physical And Mental Well Being': 0.19,
        'Impact->Driver/Aggravating Factors': 0.11, 'Impact->Impact On People': 0.14,
        'Impact->Impact On Systems, Services And Networks': 0.15, 'Impact->Number Of People Affected': 0.04,
        'Priority Interventions->Expressed By Humanitarian Staff': 0.12,
        'Priority Interventions->Expressed By Population': 0.02,
        'Priority Needs->Expressed By Humanitarian Staff': 0.03,
        'Priority Needs->Expressed By Population': 0.03
    }}]


def prepare_response(entry, preds, thresholds):
    return {
        "entry_id": entry["entry_id"],
        "predictions": {
            "sectors": preds["sectors"][0],
            "subpillars_1d": preds["subpillars_1d"][0],
            "subpillars_2d": preds["subpillars_2d"][0],
            "gender": preds["gender"][0],
            "age": preds["age"][0],
            "specific_needs_groups": preds["specific_needs_groups"][0],
            "severity": preds["severity"][0]
        },
        "thresholds": {
            "sectors": thresholds["sectors"],
            "subpillars_1d": thresholds["subpillars_1d"],
            "subpillars_2d": thresholds["subpillars_2d"],
            "gender": thresholds["gender"],
            "age": thresholds["age"],
            "specific_needs_groups": thresholds["specific_needs_groups"],
            "severity": thresholds["severity"]
        }
    }


def predict_entry_handler(event, context):
    preds = {}
    thresholds = {}
    if event.get('mock', False):
        entries = event["entries"]

        preds = fake_data[0]
        thresholds = fake_data[1]
        # del preds["column_present"]
        # del thresholds["column_present"]

        fake_response = []
        for entry in entries:
            fake_response.append(
                prepare_response(entry, preds, thresholds)
            )
        return fake_response
    else:
        body = json.loads(event["body"])
        entries = body["entries"]
        data = {
            "columns": ["excerpt"],
            "index": list(range(len(entries))),
            "data": [[entry["entry"]] for entry in entries],
        }

        response = runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME_MODEL,
            ContentType="application/json; format=pandas-split",
            Body=json.dumps(data),
        )
        response_body = json.loads(response["Body"].read().decode("ascii"))

        preds = response_body[0]
        thresholds = response_body[1]
        del preds["column_present"]
        del thresholds["column_present"]

        responses = []
        for entry in entries:
            responses.append(
                prepare_response(entry, preds, thresholds)
            )

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": str(responses),
        }
