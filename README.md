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
  "callback_url": "callback url where the result should be sent"
}
```

##### Response: POST on callback url for each entry result
```json
{
  "main_model_preds": {
    "predictions": {
      "1": {
        "101": 0.05120900645852089,
        "103": 0.05305534398013895,
        "104": 0.0618496835231781,
        "105": 1.618701742406477,
        "106": 0.1329706003100185,
        "107": 0.06410405039787292,
        "108": 0.07127126057942708,
        "109": 0.14047556157623017,
        "110": 0.07421194504086788,
        "111": 0.0428224541246891
      },
      "2": {
        "201": 0.0266275278502895,
        "202": 0.025737904669607386,
        "203": 0.03239802516451696,
        "204": 0.19150988721266024,
        "205": 0.02023347094655037,
        "206": 0.03668013150277345,
        "207": 0.025336206068887427,
        "208": 0.019818637520074844,
        "209": 0.07190693702016557,
        "210": 0.05274482899241977,
        "212": 0.09764697816636828,
        "213": 0.011826851942504827,
        "214": 0.007194649272908768,
        "215": 0.0036236922309364913,
        "216": 0.026188229980028194,
        "217": 0.005923864185152685,
        "218": 0.027860794216394424,
        "219": 0.01773698255419731,
        "220": 0.08136125979945064,
        "221": 0.02886151778511703,
        "222": 0.020004283370716233,
        "223": 0.04048,
        "224": 0.03272266437609991,
        "225": 0.003942607768944331,
        "226": 0.009105289204707068,
        "227": 0.013623181730508804,
        "228": 0.038027222035452724,
        "229": 0.019042426720261574,
        "230": 0.024089267527734912,
        "231": 0.055941250608410945,
        "232": 0.03760255640372634,
        "233": 0.04087602895385814,
        "234": 0.03429351405042117,
        "301": 0.004270137287676334,
        "302": 0.07127775529096293,
        "303": 1.331607320091941,
        "304": 0.020646801414458377,
        "305": 0.4925251007080078,
        "306": 0.7790635240838882,
        "307": 0.07366700826779655,
        "308": 0.08120508459599121,
        "309": 0.049229882853595835,
        "310": 0.1497238576412201,
        "311": 0.05259623184152271,
        "312": 0.048762670856841064,
        "313": 0.07096444411824147,
        "314": 0.0289971218444407,
        "315": 0.04735273108178494,
        "316": 0.022244140313103282,
        "317": 0.02912785443994734,
        "318": 0.06317001368318285
      },
      "3": {
        "401": 0.08046364630846416,
        "402": 0.18402323352568076,
        "403": 0.11073422928651175,
        "404": 0.15970195733731793,
        "405": 0.29262131452560425,
        "406": 0.0469617903805696,
        "407": 0.020378202933705212,
        "408": 0.07438406348228455,
        "409": 0.07348087383434176,
        "410": 1.7958825542813257,
        "411": 0.3080255351960659,
        "412": 0.06830143697914623,
        "501": 1.5787005424499512,
        "502": 0.09616524109552647,
        "601": 0.1511390060186386,
        "602": 0.15994030982255936,
        "603": 0.10206978768110275,
        "604": 0.2135063045554691,
        "605": 0.20366763696074486,
        "701": 1.4639190652153709,
        "702": 0.13173515834505595,
        "703": 0.09468458019770108,
        "704": 0.04525523943205675,
        "801": 0.0209003354289702,
        "802": 0.024959675612903777,
        "803": 0.05839878862554376,
        "804": 0.01291824979180435,
        "805": 0.025602160179513996,
        "806": 0.09169663601326491
      }
    },
    "thresholds": {
      "1": {
        "101": 0.5,
        "103": 0.55,
        "104": 0.5,
        "105": 0.5700000000000001,
        "106": 0.59,
        "107": 0.58,
        "108": 0.51,
        "109": 0.56,
        "110": 0.52,
        "111": 0.6
      },
      "2": {
        "201": 0.31,
        "202": 0.34,
        "203": 0.41000000000000003,
        "204": 0.41000000000000003,
        "205": 0.5,
        "206": 0.46,
        "207": 0.34,
        "208": 0.42,
        "209": 0.28,
        "210": 0.45,
        "212": 0.45,
        "213": 0.52,
        "214": 0.42,
        "215": 0.53,
        "216": 0.46,
        "217": 0.34,
        "218": 0.31,
        "219": 0.55,
        "220": 0.32,
        "221": 0.24,
        "222": 0.42,
        "223": 0.33,
        "224": 0.3,
        "225": 0.28,
        "226": 0.31,
        "227": 0.45,
        "228": 0.64,
        "229": 0.46,
        "230": 0.74,
        "231": 0.43,
        "232": 0.48,
        "233": 0.53,
        "234": 0.61,
        "301": 0.24,
        "302": 0.43,
        "303": 0.55,
        "304": 0.19,
        "305": 0.44,
        "306": 0.47000000000000003,
        "307": 0.46,
        "308": 0.46,
        "309": 0.38,
        "310": 0.5,
        "311": 0.46,
        "312": 0.47000000000000003,
        "313": 0.48,
        "314": 0.4,
        "315": 0.51,
        "316": 0.29,
        "317": 0.45,
        "318": 0.42
      },
      "3": {
        "401": 0.17,
        "402": 0.33,
        "403": 0.15,
        "404": 0.31,
        "405": 0.5,
        "406": 0.52,
        "407": 0.33,
        "408": 0.45,
        "409": 0.32,
        "410": 0.42,
        "411": 0.12,
        "412": 0.42,
        "501": 0.6,
        "502": 0.58,
        "601": 0.5,
        "602": 0.44,
        "603": 0.18,
        "604": 0.45,
        "605": 0.4,
        "701": 0.66,
        "702": 0.63,
        "703": 0.65,
        "704": 0.6,
        "801": 0.28,
        "802": 0.63,
        "803": 0.55,
        "804": 0.53,
        "805": 0.59,
        "806": 0.53
      }
    },
    "versions": {
      "1": {
        "101": 0.1,
        "103": 0.1,
        "104": 0.1,
        "105": 0.1,
        "106": 0.1,
        "107": 0.1,
        "108": 0.1,
        "109": 0.1,
        "110": 0.1,
        "111": 0.1
      },
      "2": {
        "201": 0.1,
        "202": 0.1,
        "203": 0.1,
        "204": 0.1,
        "205": 0.1,
        "206": 0.1,
        "207": 0.1,
        "208": 0.1,
        "209": 0.1,
        "210": 0.1,
        "212": 0.1,
        "213": 0.1,
        "214": 0.1,
        "215": 0.1,
        "216": 0.1,
        "217": 0.1,
        "218": 0.1,
        "219": 0.1,
        "220": 0.1,
        "221": 0.1,
        "222": 0.1,
        "223": 0.1,
        "224": 0.1,
        "225": 0.1,
        "226": 0.1,
        "227": 0.1,
        "228": 0.1,
        "229": 0.1,
        "230": 0.1,
        "231": 0.1,
        "232": 0.1,
        "233": 0.1,
        "234": 0.1,
        "301": 0.1,
        "302": 0.1,
        "303": 0.1,
        "304": 0.1,
        "305": 0.1,
        "306": 0.1,
        "307": 0.1,
        "308": 0.1,
        "309": 0.1,
        "310": 0.1,
        "311": 0.1,
        "312": 0.1,
        "313": 0.1,
        "314": 0.1,
        "315": 0.1,
        "316": 0.1,
        "317": 0.1,
        "318": 0.1
      },
      "3": {
        "401": 0.1,
        "402": 0.1,
        "403": 0.1,
        "404": 0.1,
        "405": 0.1,
        "406": 0.1,
        "407": 0.1,
        "408": 0.1,
        "409": 0.1,
        "410": 0.1,
        "411": 0.1,
        "412": 0.1,
        "501": 0.1,
        "502": 0.1,
        "601": 0.1,
        "602": 0.1,
        "603": 0.1,
        "604": 0.1,
        "605": 0.1,
        "701": 0.1,
        "702": 0.1,
        "703": 0.1,
        "704": 0.1,
        "801": 0.1,
        "802": 0.1,
        "803": 0.1,
        "804": 0.1,
        "805": 0.1,
        "806": 0.1
      }
    },
    "prediction_status": 1
  },
  "geolocations_preds": [
    "Nepal",
    "Paris"
  ]
}
```


### Entry Prediction Tag Info
##### Response: GET `/vf_tags`
```json
[
  {
    "id": 1,
    "key": "sectors",
    "version": 0.1
  },
  {
    "id": 2,
    "key": "subpillars",
    "version": 0.1
  },
  {
    "id": 3,
    "key": "secondary_tags",
    "version": 0.1
  },
  {
    "id": 101,
    "key": "Agriculture",
    "version": 0.1
  },
  {
    "id": 102,
    "key": "Cross",
    "version": 0.1
  },
  {
    "id": 103,
    "key": "Education",
    "version": 0.1
  },
  {
    "id": 104,
    "key": "Food Security",
    "version": 0.1
  },
  {
    "id": 105,
    "key": "Health",
    "version": 0.1
  },
  {
    "id": 106,
    "key": "Livelihoods",
    "version": 0.1
  },
  {
    "id": 107,
    "key": "Logistics",
    "version": 0.1
  },
  {
    "id": 108,
    "key": "Nutrition",
    "version": 0.1
  },
  {
    "id": 109,
    "key": "Protection",
    "version": 0.1
  },
  {
    "id": 110,
    "key": "Shelter",
    "version": 0.1
  },
  {
    "id": 111,
    "key": "WASH",
    "version": 0.1
  },
  {
    "id": 201,
    "key": "Context->Environment",
    "version": 0.1
  },
  {
    "id": 202,
    "key": "Context->Socio Cultural",
    "version": 0.1
  },
  {
    "id": 203,
    "key": "Context->Economy",
    "version": 0.1
  },
  {
    "id": 204,
    "key": "Context->Demography",
    "version": 0.1
  },
  {
    "id": 205,
    "key": "Context->Legal & Policy",
    "version": 0.1
  },
  {
    "id": 206,
    "key": "Context->Security & Stability",
    "version": 0.1
  },
  {
    "id": 207,
    "key": "Context->Politics",
    "version": 0.1
  },
  {
    "id": 208,
    "key": "Shock/Event->Type And Characteristics",
    "version": 0.1
  },
  {
    "id": 209,
    "key": "Shock/Event->Underlying/Aggravating Factors",
    "version": 0.1
  },
  {
    "id": 210,
    "key": "Shock/Event->Hazard & Threats",
    "version": 0.1
  },
  {
    "id": 212,
    "key": "Displacement->Type/Numbers/Movements",
    "version": 0.1
  },
  {
    "id": 213,
    "key": "Displacement->Push Factors",
    "version": 0.1
  },
  {
    "id": 214,
    "key": "Displacement->Pull Factors",
    "version": 0.1
  },
  {
    "id": 215,
    "key": "Displacement->Intentions",
    "version": 0.1
  },
  {
    "id": 216,
    "key": "Displacement->Local Integration",
    "version": 0.1
  },
  {
    "id": 217,
    "key": "Casualties->Injured",
    "version": 0.1
  },
  {
    "id": 218,
    "key": "Casualties->Missing",
    "version": 0.1
  },
  {
    "id": 219,
    "key": "Casualties->Dead",
    "version": 0.1
  },
  {
    "id": 220,
    "key": "Humanitarian Access->Relief To Population",
    "version": 0.1
  },
  {
    "id": 221,
    "key": "Humanitarian Access->Population To Relief",
    "version": 0.1
  },
  {
    "id": 222,
    "key": "Humanitarian Access->Physical Constraints",
    "version": 0.1
  },
  {
    "id": 223,
    "key": "Humanitarian Access->Number Of People Facing Humanitarian Access Constraints/Humanitarian Access Gaps",
    "version": 0.1
  },
  {
    "id": 224,
    "key": "Information And Communication->Communication Means And Preferences",
    "version": 0.1
  },
  {
    "id": 225,
    "key": "Information And Communication->Information Challenges And Barriers",
    "version": 0.1
  },
  {
    "id": 226,
    "key": "Information And Communication->Knowledge And Info Gaps (Pop)",
    "version": 0.1
  },
  {
    "id": 227,
    "key": "Information And Communication->Knowledge And Info Gaps (Hum)",
    "version": 0.1
  },
  {
    "id": 228,
    "key": "Covid-19->Cases",
    "version": 0.1
  },
  {
    "id": 229,
    "key": "Covid-19->Contact Tracing",
    "version": 0.1
  },
  {
    "id": 230,
    "key": "Covid-19->Deaths",
    "version": 0.1
  },
  {
    "id": 231,
    "key": "Covid-19->Hospitalization & Care",
    "version": 0.1
  },
  {
    "id": 232,
    "key": "Covid-19->Restriction Measures",
    "version": 0.1
  },
  {
    "id": 233,
    "key": "Covid-19->Testing",
    "version": 0.1
  },
  {
    "id": 234,
    "key": "Covid-19->Vaccination",
    "version": 0.1
  },
  {
    "id": 301,
    "key": "At Risk->Number Of People At Risk",
    "version": 0.1
  },
  {
    "id": 302,
    "key": "At Risk->Risk And Vulnerabilities",
    "version": 0.1
  },
  {
    "id": 303,
    "key": "Capacities & Response->International Response",
    "version": 0.1
  },
  {
    "id": 304,
    "key": "Capacities & Response->Local Response",
    "version": 0.1
  },
  {
    "id": 305,
    "key": "Capacities & Response->National Response",
    "version": 0.1
  },
  {
    "id": 306,
    "key": "Capacities & Response->Number Of People Reached/Response Gaps",
    "version": 0.1
  },
  {
    "id": 307,
    "key": "Humanitarian Conditions->Coping Mechanisms",
    "version": 0.1
  },
  {
    "id": 308,
    "key": "Humanitarian Conditions->Living Standards",
    "version": 0.1
  },
  {
    "id": 309,
    "key": "Humanitarian Conditions->Number Of People In Need",
    "version": 0.1
  },
  {
    "id": 310,
    "key": "Humanitarian Conditions->Physical And Mental Well Being",
    "version": 0.1
  },
  {
    "id": 311,
    "key": "Impact->Driver/Aggravating Factors",
    "version": 0.1
  },
  {
    "id": 312,
    "key": "Impact->Impact On People",
    "version": 0.1
  },
  {
    "id": 313,
    "key": "Impact->Impact On Systems, Services And Networks",
    "version": 0.1
  },
  {
    "id": 314,
    "key": "Impact->Number Of People Affected",
    "version": 0.1
  },
  {
    "id": 315,
    "key": "Priority Interventions->Expressed By Humanitarian Staff",
    "version": 0.1
  },
  {
    "id": 316,
    "key": "Priority Interventions->Expressed By Population",
    "version": 0.1
  },
  {
    "id": 317,
    "key": "Priority Needs->Expressed By Humanitarian Staff",
    "version": 0.1
  },
  {
    "id": 318,
    "key": "Priority Needs->Expressed By Population",
    "version": 0.1
  },
  {
    "id": 401,
    "key": "specific_needs_groups->Child Head of Household",
    "version": 0.1
  },
  {
    "id": 402,
    "key": "specific_needs_groups->Chronically Ill",
    "version": 0.1
  },
  {
    "id": 403,
    "key": "specific_needs_groups->Elderly Head of Household",
    "version": 0.1
  },
  {
    "id": 404,
    "key": "specific_needs_groups->Female Head of Household",
    "version": 0.1
  },
  {
    "id": 405,
    "key": "specific_needs_groups->GBV survivors",
    "version": 0.1
  },
  {
    "id": 406,
    "key": "specific_needs_groups->Indigenous people",
    "version": 0.1
  },
  {
    "id": 407,
    "key": "specific_needs_groups->LGBTQI+",
    "version": 0.1
  },
  {
    "id": 408,
    "key": "specific_needs_groups->Minorities",
    "version": 0.1
  },
  {
    "id": 409,
    "key": "specific_needs_groups->Persons with Disability",
    "version": 0.1
  },
  {
    "id": 410,
    "key": "specific_needs_groups->Pregnant or Lactating Women",
    "version": 0.1
  },
  {
    "id": 411,
    "key": "specific_needs_groups->Single Women (including Widows)",
    "version": 0.1
  },
  {
    "id": 412,
    "key": "specific_needs_groups->Unaccompanied or Separated Children",
    "version": 0.1
  },
  {
    "id": 501,
    "key": "gender_kw_pred->Female",
    "version": 0.1
  },
  {
    "id": 502,
    "key": "gender_kw_pred->Male",
    "version": 0.1
  },
  {
    "id": 701,
    "key": "age_kw_pred->Adult (18 to 59 years old)",
    "version": 0.1
  },
  {
    "id": 702,
    "key": "age_kw_pred->Children/Youth (5 to 17 years old)",
    "version": 0.1
  },
  {
    "id": 703,
    "key": "age_kw_pred->Infants/Toddlers (<5 years old)",
    "version": 0.1
  },
  {
    "id": 704,
    "key": "age_kw_pred->Older Persons (60+ years old)",
    "version": 0.1
  },
  {
    "id": 601,
    "key": "severity->Critical",
    "version": 0.1
  },
  {
    "id": 602,
    "key": "severity->Major",
    "version": 0.1
  },
  {
    "id": 603,
    "key": "severity->Minor Problem",
    "version": 0.1
  },
  {
    "id": 604,
    "key": "severity->No problem",
    "version": 0.1
  },
  {
    "id": 605,
    "key": "severity->Of Concern",
    "version": 0.1
  }
]
```
