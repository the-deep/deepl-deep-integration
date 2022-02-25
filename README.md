# deepl-deep-integration


## Endpoints:
### Document Extract
Extract the contents from the documents

##### Request: POST `/extract_docs` [Req from DEEP to DEEPL]
```json
{
  "urls": [
    {
      "url": "url_of_pdf_or_html",
      "client_id": "client_id_value"
    }
  ],
  "callback_url": "callback url where the result should be sent"
}
```

##### Response: **POST** on `callback_url` for each url (individual request) [After the extraction]
```json
{
  "client_id": "client_id_value",
  "url": "url of the pdf or html",
  "text_path": "text path: presigned url from s3 for prod env, local link for dev env",
  "images_path": [
    "array of presigned urls from s3 for prod env",
    "local links for dev env"
  ],
  "total_pages": "total pages count",
  "total_words_count": "total_words count",
  "extraction_status": 1
}
```
NOTE: **extraction status** -> 0 = Falied, 1 = Success



### Entry Prediction
##### Request: POST `/entry_predict` [Req from DEEP to DEEPL]
```json
{
  "entries": [
    {
      "entry_id": "entry id value",
      "entry": "entry text ..."
    }
  ],
  "publishing_organization": "name of publishing org",
  "authoring_organization": "names of authoring org (list)",
  "callback_url": "callback url where the result should be sent"
}
```

##### Response: POST on callback url for each entry result
```json
{
    "entry_id": "entry id value",
    "model_preds": {
        "predictions": {
            "1": {
                "101": 0.0011651739818839036,
                "103": 0.015535588254747183,
                "104": 0.005824137285041313,
                "105": 1.793482568528917,
                "106": 0.01099251798893276,
                "107": 0.0032105192076414824,
                "108": 0.0124868813293929,
                "109": 0.02668164670467377,
                "110": 0.005009377353070748,
                "111": 0.009972890311816952
            },
            "2": {
                "201": 0.0012622659836013458,
                "202": 0.02306136576568379,
                "203": 0.005644642770653817,
                "204": 0.0034247187669483982,
                "205": 0.012004651850269686,
                "206": 0.003777112314392897,
                "207": 0.006988294577846925,
                "208": 0.004434663860592991,
                "209": 0.010090794496457365,
                "210": 0.03726671490332355,
                "212": 0.0032292920973544057,
                "213": 0.0006074654536221076,
                "214": 0.0003304164395025321,
                "215": 0.00018383467058332537,
                "216": 0.0055785649456083775,
                "217": 0.0007600567746871653,
                "218": 0.001205129620547478,
                "219": 0.0014695160124184828,
                "220": 0.002951633008518096,
                "221": 0.0035551005949903476,
                "222": 0.0012103682820452377,
                "223": 0.0019022544717138751,
                "224": 0.08337817021778653,
                "225": 0.03830634678403537,
                "226": 0.034376099291774966,
                "227": 0.07387536784840955,
                "228": 0.0012126606452511624,
                "229": 0.004611896852461191,
                "230": 0.0009712083322674403,
                "231": 0.010670439862623447,
                "232": 0.01832416443073231,
                "233": 0.11516693460790417,
                "234": 0.0053614584936036
            },
            "3": {
                "301": 0.0002837441267426281,
                "302": 0.009622176109654147,
                "303": 0.04561438916190978,
                "304": 0.005028768791817129,
                "305": 0.9964677483536476,
                "306": 0.06108326571328299,
                "307": 0.010084001890694102,
                "308": 0.2781538168589274,
                "309": 0.0020901766425419238,
                "310": 0.01726081572109606,
                "311": 0.012977353885377707,
                "312": 0.009677161914155338,
                "313": 0.070230257180002,
                "314": 0.0016847220346486818,
                "315": 0.00868615863675421,
                "316": 0.00596371750968198,
                "317": 0.00492362305521965,
                "318": 0.012582738883793354
            },
            "4": {
                "401": 0.0037905480712652206,
                "402": 0.0007412575008668776,
                "403": 0.0057904648461512154,
                "404": 0.0025663503038231283,
                "405": 0.0010304296245941748,
                "406": 0.0020969748640289674,
                "407": 0.018655198694365778,
                "408": 0.023670646093659483,
                "409": 0.003865474718622863,
                "410": 0.001413615691304511,
                "411": 0.004206338198855519,
                "412": 0.0004054372160074612
            },
            "5": {
                "501": 0.002500954949834817,
                "502": 0.005071992795406418
            },
            "6": {
                "601": 0.0047307801044856514,
                "602": 0.009723861744119362,
                "603": 0.02891216892749071,
                "604": 0.002321415412865701
            },
            "8": {
                "801": 0.00033179544827786005,
                "802": 0.002489823805676265,
                "803": 0.004687755535454002,
                "804": 0.000245133259644111,
                "805": 0.0010722849765443243,
                "806": 0.09103546024493452
            },
            "9": {
                "902": 0.5,
                "903": 0.5,
                "904": 0.5,
                "905": 0.5,
                "906": 0.5,
                "907": 0.5
            }
        },
        "thresholds": {
            "1": {
                "101": 0.41000000000000003,
                "103": 0.46,
                "104": 0.48,
                "105": 0.36,
                "106": 0.38,
                "107": 0.5,
                "108": 0.49,
                "109": 0.58,
                "110": 0.42,
                "111": 0.53
            },
            "2": {
                "201": 0.38,
                "202": 0.17,
                "203": 0.41000000000000003,
                "204": 0.49,
                "205": 0.31,
                "206": 0.44,
                "207": 0.3,
                "208": 0.2,
                "209": 0.17,
                "210": 0.23,
                "212": 0.38,
                "213": 0.37,
                "214": 0.29,
                "215": 0.38,
                "216": 0.25,
                "217": 0.13,
                "218": 0.13,
                "219": 0.28,
                "220": 0.29,
                "221": 0.19,
                "222": 0.48,
                "223": 0.47000000000000003,
                "224": 0.21,
                "225": 0.15,
                "226": 0.18,
                "227": 0.18,
                "228": 0.8,
                "229": 0.39,
                "230": 0.81,
                "231": 0.41000000000000003,
                "232": 0.46,
                "233": 0.79,
                "234": 0.54
            },
            "3": {
                "301": 0.12,
                "302": 0.41000000000000003,
                "303": 0.62,
                "304": 0.1,
                "305": 0.43,
                "306": 0.49,
                "307": 0.36,
                "308": 0.45,
                "309": 0.31,
                "310": 0.41000000000000003,
                "311": 0.38,
                "312": 0.33,
                "313": 0.45,
                "314": 0.24,
                "315": 0.55,
                "316": 0.15,
                "317": 0.3,
                "318": 0.25
            },
            "4": {
                "401": 0.25,
                "402": 0.58,
                "403": 0.14,
                "404": 0.48,
                "405": 0.78,
                "406": 0.13,
                "407": 0.41000000000000003,
                "408": 0.59,
                "409": 0.56,
                "410": 0.49,
                "411": 0.2,
                "412": 0.6
            },
            "5": {
                "501": 0.71,
                "502": 0.44
            },
            "6": {
                "601": 0.48,
                "602": 0.44,
                "603": 0.4,
                "604": 0.61
            },
            "8": {
                "801": 0.73,
                "802": 0.55,
                "803": 0.67,
                "804": 0.75,
                "805": 0.64,
                "806": 0.53
            },
            "9": {
                "902": 0.5,
                "903": 0.5,
                "904": 0.5,
                "905": 0.5,
                "906": 0.5,
                "907": 0.5
            }
        },
        "selected_tags": {
            "1": [
                "105"
            ],
            "2": [],
            "3": [
                "305"
            ],
            "4": [],
            "5": [],
            "6": [],
            "7": [],
            "8": [],
            "9": []
        },
        "prediction_status": "1"
    },
    "geolocations_preds": [],
    "reliability_pred": "Usually reliable",
    "main_model": {
        "name": "all_tags_model",
        "version": "1.0.0"
    },
    "geolocation": {
        "name": "geolocation",
        "version": "1.0.0"
    },
    "reliability": {
        "name": "reliability",
        "version": "1.0.0"
    }
}
```


### Entry Prediction Tag Info
##### Response: GET `/vf_tags`
```json
{
  "sectors": ["1", "1.0.0"],
  "subpillars_1d": ["2", "1.0.0"],
  "subpillars_2d": ["3", "1.0.0"],
  "age": ["6", "1.0.0"], "gender": ["5", "1.0.0"],
  "demographic_group": ["9", "1.0.0"],
  "affected_groups": ["8", "1.0.0"],
  "specific_needs_groups": ["4", "1.0.0"],
  "severity": ["7", "1.0.0"],
  "Agriculture": ["101", "1.0.0"],
  "Cross": ["102", "1.0.0"],
  "Education": ["103", "1.0.0"],
  "Food Security": ["104", "1.0.0"],
  "Health": ["105", "1.0.0"],
  "Livelihoods": ["106", "1.0.0"],
  "Logistics": ["107", "1.0.0"],
  "Nutrition": ["108", "1.0.0"],
  "Protection": ["109", "1.0.0"],
  "Shelter": ["110", "1.0.0"],
  "WASH": ["111", "1.0.0"],
  "Context->Environment": ["201", "1.0.0"],
  "Context->Socio Cultural": ["202", "1.0.0"],
  "Context->Economy": ["203", "1.0.0"],
  "Context->Demography": ["204", "1.0.0"],
  "Context->Legal & Policy": ["205", "1.0.0"],
  "Context->Security & Stability": ["206", "1.0.0"],
  "Context->Politics": ["207", "1.0.0"],
  "Shock/Event->Type And Characteristics": ["208", "1.0.0"],
  "Shock/Event->Underlying/Aggravating Factors": ["209", "1.0.0"],
  "Shock/Event->Hazard & Threats": ["210", "1.0.0"],
  "Displacement->Type/Numbers/Movements": ["212", "1.0.0"],
  "Displacement->Push Factors": ["213", "1.0.0"],
  "Displacement->Pull Factors": ["214", "1.0.0"],
  "Displacement->Intentions": ["215", "1.0.0"],
  "Displacement->Local Integration": ["216", "1.0.0"],
  "Casualties->Injured": ["217", "1.0.0"],
  "Casualties->Missing": ["218", "1.0.0"],
  "Casualties->Dead": ["219", "1.0.0"],
  "Humanitarian Access->Relief To Population": ["220", "1.0.0"],
  "Humanitarian Access->Population To Relief": ["221", "1.0.0"],
  "Humanitarian Access->Physical Constraints": ["222", "1.0.0"],
  "Humanitarian Access->Number Of People Facing Humanitarian Access Constraints/Humanitarian Access Gaps": ["223", "1.0.0"],
  "Information And Communication->Communication Means And Preferences": ["224", "1.0.0"],
  "Information And Communication->Information Challenges And Barriers": ["225", "1.0.0"],
  "Information And Communication->Knowledge And Info Gaps (Pop)": ["226", "1.0.0"],
  "Information And Communication->Knowledge And Info Gaps (Hum)": ["227", "1.0.0"],
  "Covid-19->Cases": ["228", "1.0.0"],
  "Covid-19->Contact Tracing": ["229", "1.0.0"],
  "Covid-19->Deaths": ["230", "1.0.0"],
  "Covid-19->Hospitalization & Care": ["231", "1.0.0"],
  "Covid-19->Restriction Measures": ["232", "1.0.0"],
  "Covid-19->Testing": ["233", "1.0.0"],
  "Covid-19->Vaccination": ["234", "1.0.0"],
  "At Risk->Number Of People At Risk": ["301", "1.0.0"],
  "At Risk->Risk And Vulnerabilities": ["302", "1.0.0"],
  "Capacities & Response->International Response": ["303", "1.0.0"],
  "Capacities & Response->Local Response": ["304", "1.0.0"],
  "Capacities & Response->National Response": ["305", "1.0.0"],
  "Capacities & Response->Number Of People Reached/Response Gaps": ["306", "1.0.0"],
  "Humanitarian Conditions->Coping Mechanisms": ["307", "1.0.0"],
  "Humanitarian Conditions->Living Standards": ["308", "1.0.0"],
  "Humanitarian Conditions->Number Of People In Need": ["309", "1.0.0"],
  "Humanitarian Conditions->Physical And Mental Well Being": ["310", "1.0.0"],
  "Impact->Driver/Aggravating Factors": ["311", "1.0.0"], "Impact->Impact On People": ["312", "1.0.0"],
  "Impact->Impact On Systems, Services And Networks": ["313", "1.0.0"],
  "Impact->Number Of People Affected": ["314", "1.0.0"],
  "Priority Interventions->Expressed By Humanitarian Staff": ["315", "1.0.0"],
  "Priority Interventions->Expressed By Population": ["316", "1.0.0"],
  "Priority Needs->Expressed By Humanitarian Staff": ["317", "1.0.0"],
  "Priority Needs->Expressed By Population": ["318", "1.0.0"],
  "Child Head of Household": ["401", "1.0.0"],
  "Chronically Ill": ["402", "1.0.0"],
  "Elderly Head of Household": ["403", "1.0.0"],
  "Female Head of Household": ["404", "1.0.0"],
  "GBV survivors": ["405", "1.0.0"],
  "Indigenous people": ["406", "1.0.0"],
  "LGBTQI+": ["407", "1.0.0"],
  "Minorities": ["408", "1.0.0"],
  "Persons with Disability": ["409", "1.0.0"],
  "Pregnant or Lactating Women": ["410", "1.0.0"],
  "Single Women (including Widows)": ["411", "1.0.0"],
  "Unaccompanied or Separated Children": ["412", "1.0.0"],
  "Female": ["501", "1.0.0"],
  "Male": ["502", "1.0.0"],
  "Adult (18 to 59 years old)": ["601", "1.0.0"],
  "Children/Youth (5 to 17 years old)": ["602", "1.0.0"],
  "Infants/Toddlers (<5 years old)": ["603", "1.0.0"],
  "Older Persons (60+ years old)" : ["604", "1.0.0"],
  "Infants/Toddlers (<5 years old) " : ["901", "1.0.0"],
  "Female Children/Youth (5 to 17 years old)" : ["902", "1.0.0"],
  "Male Children/Youth (5 to 17 years old)" : ["903", "1.0.0"],
  "Female Adult (18 to 59 years old)" : ["904", "1.0.0"],
  "Male Adult (18 to 59 years old)" : ["905", "1.0.0" ],
  "Female Older Persons (60+ years old)" : ["906", "1.0.0"],
  "Male Older Persons (60+ years old)" : ["907", "1.0.0"],
  "Critical" : ["701", "1.0.0"],
  "Major" : ["702", "1.0.0"],
  "Minor Problem" : ["703", "1.0.0"],
  "No problem" : ["704", "1.0.0" ],
  "Of Concern" : ["705", "1.0.0"],
  "Asylum Seekers" : ["801", "1.0.0"],
  "Host" : ["802", "1.0.0"],
  "IDP" : ["803", "1.0.0" ],
  "Migrants" : ["804", "1.0.0"],
  "Refugees" : ["805", "1.0.0"],
  "Returnees" : ["806", "1.0.0"]
}
```
