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
      "client_id": "entry id value",
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
    "client_id": "1881",
    "model_preds": [
        {
            "tags": {
                "1": {
                    "101": {
                        "prediction": 0.0009809271432459354,
                        "threshold": 0.41000000000000003,
                        "is_selected": false
                    },
                    "103": {
                        "prediction": 0.002870741857053793,
                        "threshold": 0.46,
                        "is_selected": false
                    },
                    "104": {
                        "prediction": 0.0025155357434414327,
                        "threshold": 0.48,
                        "is_selected": false
                    },
                    "105": {
                        "prediction": 2.648323608769311,
                        "threshold": 0.36,
                        "is_selected": true
                    },
                    "106": {
                        "prediction": 0.017231033722821035,
                        "threshold": 0.38,
                        "is_selected": false
                    },
                    "107": {
                        "prediction": 0.0033341911621391773,
                        "threshold": 0.5,
                        "is_selected": false
                    },
                    "108": {
                        "prediction": 0.003857407196215829,
                        "threshold": 0.49,
                        "is_selected": false
                    },
                    "109": {
                        "prediction": 0.024287596923010104,
                        "threshold": 0.58,
                        "is_selected": false
                    },
                    "110": {
                        "prediction": 0.0030457485644590286,
                        "threshold": 0.42,
                        "is_selected": false
                    },
                    "111": {
                        "prediction": 0.009205310939336723,
                        "threshold": 0.53,
                        "is_selected": false
                    }
                },
                "2": {
                    "201": {
                        "prediction": 0.003244201223807115,
                        "threshold": 0.38,
                        "is_selected": false
                    },
                    "202": {
                        "prediction": 0.0028143073637586303,
                        "threshold": 0.17,
                        "is_selected": false
                    },
                    "203": {
                        "prediction": 0.0023983575108392934,
                        "threshold": 0.41000000000000003,
                        "is_selected": false
                    },
                    "204": {
                        "prediction": 0.03473917592544945,
                        "threshold": 0.49,
                        "is_selected": false
                    },
                    "205": {
                        "prediction": 0.002362836159825806,
                        "threshold": 0.31,
                        "is_selected": false
                    },
                    "206": {
                        "prediction": 0.0027625678657469425,
                        "threshold": 0.44,
                        "is_selected": false
                    },
                    "207": {
                        "prediction": 0.00310999535334607,
                        "threshold": 0.3,
                        "is_selected": false
                    },
                    "208": {
                        "prediction": 0.0062938983319327235,
                        "threshold": 0.2,
                        "is_selected": false
                    },
                    "209": {
                        "prediction": 0.013584146440467413,
                        "threshold": 0.17,
                        "is_selected": false
                    },
                    "210": {
                        "prediction": 0.03200973505559175,
                        "threshold": 0.23,
                        "is_selected": false
                    },
                    "212": {
                        "prediction": 0.009840355548811587,
                        "threshold": 0.38,
                        "is_selected": false
                    },
                    "213": {
                        "prediction": 0.0001934542622719262,
                        "threshold": 0.37,
                        "is_selected": false
                    },
                    "214": {
                        "prediction": 0.00012094086710492086,
                        "threshold": 0.29,
                        "is_selected": false
                    },
                    "215": {
                        "prediction": 0.00023344017742936942,
                        "threshold": 0.38,
                        "is_selected": false
                    },
                    "216": {
                        "prediction": 0.004564649425446987,
                        "threshold": 0.25,
                        "is_selected": false
                    },
                    "217": {
                        "prediction": 0.000980646291282028,
                        "threshold": 0.13,
                        "is_selected": false
                    },
                    "218": {
                        "prediction": 0.0008387683640019251,
                        "threshold": 0.13,
                        "is_selected": false
                    },
                    "219": {
                        "prediction": 0.0022046211857481724,
                        "threshold": 0.28,
                        "is_selected": false
                    },
                    "220": {
                        "prediction": 0.0072525300342461164,
                        "threshold": 0.29,
                        "is_selected": false
                    },
                    "221": {
                        "prediction": 0.0014619975301780198,
                        "threshold": 0.19,
                        "is_selected": false
                    },
                    "222": {
                        "prediction": 0.0023239071500332407,
                        "threshold": 0.48,
                        "is_selected": false
                    },
                    "223": {
                        "prediction": 0.0010538867308183552,
                        "threshold": 0.47000000000000003,
                        "is_selected": false
                    },
                    "224": {
                        "prediction": 0.014774697566671031,
                        "threshold": 0.21,
                        "is_selected": false
                    },
                    "225": {
                        "prediction": 0.0006417883560061455,
                        "threshold": 0.15,
                        "is_selected": false
                    },
                    "226": {
                        "prediction": 0.0012694694709757136,
                        "threshold": 0.18,
                        "is_selected": false
                    },
                    "227": {
                        "prediction": 0.002328895950793392,
                        "threshold": 0.18,
                        "is_selected": false
                    },
                    "228": {
                        "prediction": 0.0026775070000439882,
                        "threshold": 0.8,
                        "is_selected": false
                    },
                    "229": {
                        "prediction": 0.0001924166169304114,
                        "threshold": 0.39,
                        "is_selected": false
                    },
                    "230": {
                        "prediction": 0.0013101000890687658,
                        "threshold": 0.81,
                        "is_selected": false
                    },
                    "231": {
                        "prediction": 0.0018647602168706857,
                        "threshold": 0.41000000000000003,
                        "is_selected": false
                    },
                    "232": {
                        "prediction": 0.006384604974933292,
                        "threshold": 0.46,
                        "is_selected": false
                    },
                    "233": {
                        "prediction": 0.0009332533006238032,
                        "threshold": 0.79,
                        "is_selected": false
                    },
                    "234": {
                        "prediction": 0.0013843739267300676,
                        "threshold": 0.54,
                        "is_selected": false
                    }
                },
                "3": {
                    "301": {
                        "prediction": 0.00023012808014755137,
                        "threshold": 0.12,
                        "is_selected": false
                    },
                    "302": {
                        "prediction": 0.016112014560437784,
                        "threshold": 0.41000000000000003,
                        "is_selected": false
                    },
                    "303": {
                        "prediction": 1.528833854583002,
                        "threshold": 0.62,
                        "is_selected": true
                    },
                    "304": {
                        "prediction": 0.0023799765040166676,
                        "threshold": 0.1,
                        "is_selected": false
                    },
                    "305": {
                        "prediction": 0.4667431809181391,
                        "threshold": 0.43,
                        "is_selected": false
                    },
                    "306": {
                        "prediction": 0.09864356596859133,
                        "threshold": 0.49,
                        "is_selected": false
                    },
                    "307": {
                        "prediction": 0.01058419196245571,
                        "threshold": 0.36,
                        "is_selected": false
                    },
                    "308": {
                        "prediction": 0.019500859909587435,
                        "threshold": 0.45,
                        "is_selected": false
                    },
                    "309": {
                        "prediction": 0.004097318366890953,
                        "threshold": 0.31,
                        "is_selected": false
                    },
                    "310": {
                        "prediction": 0.03721689941679559,
                        "threshold": 0.41000000000000003,
                        "is_selected": false
                    },
                    "311": {
                        "prediction": 0.008000135054125598,
                        "threshold": 0.38,
                        "is_selected": false
                    },
                    "312": {
                        "prediction": 0.005017997781661424,
                        "threshold": 0.33,
                        "is_selected": false
                    },
                    "313": {
                        "prediction": 0.014817145549588732,
                        "threshold": 0.45,
                        "is_selected": false
                    },
                    "314": {
                        "prediction": 0.0042566549382172525,
                        "threshold": 0.24,
                        "is_selected": false
                    },
                    "315": {
                        "prediction": 0.006351343102075836,
                        "threshold": 0.55,
                        "is_selected": false
                    },
                    "316": {
                        "prediction": 0.0017733968949566286,
                        "threshold": 0.15,
                        "is_selected": false
                    },
                    "317": {
                        "prediction": 0.0020504186007504663,
                        "threshold": 0.3,
                        "is_selected": false
                    },
                    "318": {
                        "prediction": 0.008379371836781502,
                        "threshold": 0.25,
                        "is_selected": false
                    }
                },
                "4": {
                    "401": {
                        "prediction": 0.0002582040324341506,
                        "threshold": 0.25,
                        "is_selected": false
                    },
                    "402": {
                        "prediction": 0.002513411213997109,
                        "threshold": 0.58,
                        "is_selected": false
                    },
                    "403": {
                        "prediction": 0.0029885374325593662,
                        "threshold": 0.14,
                        "is_selected": false
                    },
                    "404": {
                        "prediction": 0.002463895119338607,
                        "threshold": 0.48,
                        "is_selected": false
                    },
                    "405": {
                        "prediction": 0.021848065826373223,
                        "threshold": 0.78,
                        "is_selected": false
                    },
                    "406": {
                        "prediction": 0.002455976433478869,
                        "threshold": 0.13,
                        "is_selected": false
                    },
                    "407": {
                        "prediction": 0.00023902353061158662,
                        "threshold": 0.41000000000000003,
                        "is_selected": false
                    },
                    "408": {
                        "prediction": 0.011608299751908092,
                        "threshold": 0.59,
                        "is_selected": false
                    },
                    "409": {
                        "prediction": 0.0007886766979936509,
                        "threshold": 0.56,
                        "is_selected": false
                    },
                    "410": {
                        "prediction": 2.0394893325105006,
                        "threshold": 0.49,
                        "is_selected": true
                    },
                    "411": {
                        "prediction": 0.0110106251668185,
                        "threshold": 0.2,
                        "is_selected": false
                    },
                    "412": {
                        "prediction": 0.00020141856415042034,
                        "threshold": 0.6,
                        "is_selected": false
                    }
                },
                "5": {
                    "501": {
                        "prediction": 1.4041466612211415,
                        "threshold": 0.71,
                        "is_selected": true
                    },
                    "502": {
                        "prediction": 0.010200739118524572,
                        "threshold": 0.44,
                        "is_selected": false
                    }
                },
                "6": {
                    "601": {
                        "prediction": 0.05603748528907697,
                        "threshold": 0.48,
                        "is_selected": false
                    },
                    "602": {
                        "prediction": 0.026138677177104084,
                        "threshold": 0.44,
                        "is_selected": false
                    },
                    "603": {
                        "prediction": 0.04484661389142275,
                        "threshold": 0.4,
                        "is_selected": false
                    },
                    "604": {
                        "prediction": 0.00565023672934927,
                        "threshold": 0.61,
                        "is_selected": false
                    }
                },
                "8": {
                    "801": {
                        "prediction": 0.00020663861156607123,
                        "threshold": 0.73,
                        "is_selected": false
                    },
                    "802": {
                        "prediction": 0.008624091067097403,
                        "threshold": 0.55,
                        "is_selected": false
                    },
                    "803": {
                        "prediction": 0.004657054903791911,
                        "threshold": 0.67,
                        "is_selected": false
                    },
                    "804": {
                        "prediction": 0.0004473439184948802,
                        "threshold": 0.75,
                        "is_selected": false
                    },
                    "805": {
                        "prediction": 0.00035789134926744737,
                        "threshold": 0.64,
                        "is_selected": false
                    },
                    "806": {
                        "prediction": 0.009627632339889149,
                        "threshold": 0.53,
                        "is_selected": false
                    }
                },
                "9": {
                    "902": {
                        "prediction": 0.5,
                        "threshold": 0.5,
                        "is_selected": false
                    },
                    "903": {
                        "prediction": 0.5,
                        "threshold": 0.5,
                        "is_selected": false
                    },
                    "904": {
                        "prediction": 0.5,
                        "threshold": 0.5,
                        "is_selected": false
                    },
                    "905": {
                        "prediction": 0.5,
                        "threshold": 0.5,
                        "is_selected": false
                    },
                    "906": {
                        "prediction": 0.5,
                        "threshold": 0.5,
                        "is_selected": false
                    },
                    "907": {
                        "prediction": 0.5,
                        "threshold": 0.5,
                        "is_selected": false
                    }
                }
            },
            "prediction_status": "1",
            "model_info": {
                "id": "all_tags_model",
                "version": "1.0.0"
            }
        },
        {
            "model_info": {
                "id": "geolocation",
                "version": "1.0.0"
            },
            "values": ["Nepal"],
            "prediction_status": 1
        },
        {
            "model_info": {
                "id": "reliability",
                "version": "1.0.0"
            },
            "tags": {
                "10": {
                    "1002": {
                        "is_selected": true
                    }
                }
            },
            "prediction_status": 1
        }
    ]
}
```


### Entry Prediction Tag Info
##### Response: GET `/vf_tags`
```json
{
   " 101" :{
      " label" :" Agriculture" ,
      " group" :" Sectors" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 1" 
   },
   " 102" :{
      " label" :" Cross" ,
      " group" :" Sectors" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 1" 
   },
   " 103" :{
      " label" :" Education" ,
      " group" :" Sectors" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 1" 
   },
   " 104" :{
      " label" :" Food Security" ,
      " group" :" Sectors" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 1" 
   },
   " 105" :{
      " label" :" Health" ,
      " group" :" Sectors" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 1" 
   },
   " 106" :{
      " label" :" Livelihoods" ,
      " group" :" Sectors" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 1" 
   },
   " 107" :{
      " label" :" Logistics" ,
      " group" :" Sectors" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 1" 
   },
   " 108" :{
      " label" :" Nutrition" ,
      " group" :" Sectors" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 1" 
   },
   " 109" :{
      " label" :" Protection" ,
      " group" :" Sectors" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 1" 
   },
   " 110" :{
      " label" :" Shelter" ,
      " group" :" Sectors" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 1" 
   },
   " 111" :{
      " label" :" WASH" ,
      " group" :" Sectors" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 1" 
   },
   " 201" :{
      " label" :" Environment" ,
      " group" :" Context" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 202" :{
      " label" :" Socio Cultural" ,
      " group" :" Context" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 203" :{
      " label" :" Economy" ,
      " group" :" Context" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 204" :{
      " label" :" Demography" ,
      " group" :" Context" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 205" :{
      " label" :" Legal & Policy" ,
      " group" :" Context" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 206" :{
      " label" :" Security & Stability" ,
      " group" :" Context" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 207" :{
      " label" :" Politics" ,
      " group" :" Context" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 208" :{
      " label" :" Type And Characteristics" ,
      " group" :" Shock/Event" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 209" :{
      " label" :" Underlying/Aggravating Factors" ,
      " group" :" Shock/Event" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 210" :{
      " label" :" Hazard & Threats" ,
      " group" :" Shock/Event" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 212" :{
      " label" :" Type/Numbers/Movements" ,
      " group" :" Displacement" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 213" :{
      " label" :" Push Factors" ,
      " group" :" Displacement" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 214" :{
      " label" :" Pull Factors" ,
      " group" :" Displacement" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 215" :{
      " label" :" Intentions" ,
      " group" :" Displacement" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 216" :{
      " label" :" Local Integration" ,
      " group" :" Displacement" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 217" :{
      " label" :" Injured" ,
      " group" :" Casualties" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 218" :{
      " label" :" Missing" ,
      " group" :" Casualties" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 219" :{
      " label" :" Dead" ,
      " group" :" Casualties" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 220" :{
      " label" :" Relief To Population" ,
      " group" :" Humanitarian Access" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 221" :{
      " label" :" Population To Relief" ,
      " group" :" Humanitarian Access" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 222" :{
      " label" :" Physical Constraints" ,
      " group" :" Humanitarian Access" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 223" :{
      " label" :" Number Of People Facing Humanitarian Access Constraints/Humanitarian Access Gaps" ,
      " group" :" Humanitarian Access" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 224" :{
      " label" :" Communication Means And Preferences" ,
      " group" :" Information And Communication" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 225" :{
      " label" :" Information Challenges And Barriers" ,
      " group" :" Information And Communication" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 226" :{
      " label" :" Knowledge And Info Gaps (Pop)" ,
      " group" :" Information And Communication" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 227" :{
      " label" :" Knowledge And Info Gaps (Hum)" ,
      " group" :" Information And Communication" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 228" :{
      " label" :" Cases" ,
      " group" :" Covid-19" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 229" :{
      " label" :" Contact Tracing" ,
      " group" :" Covid-19" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 230" :{
      " label" :" Deaths" ,
      " group" :" Covid-19" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 231" :{
      " label" :" Hospitalization & Care" ,
      " group" :" Covid-19" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 232" :{
      " label" :" Restriction Measures" ,
      " group" :" Covid-19" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 233" :{
      " label" :" Testing" ,
      " group" :" Covid-19" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 234" :{
      " label" :" Vaccination" ,
      " group" :" Covid-19" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 2" 
   },
   " 301" :{
      " label" :" Number Of People At Risk" ,
      " group" :" At Risk" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 3" 
   },
   " 302" :{
      " label" :" Risk And Vulnerabilities" ,
      " group" :" At Risk" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 3" 
   },
   " 303" :{
      " label" :" International Response" ,
      " group" :" Capacities & Response" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 3" 
   },
   " 304" :{
      " label" :" Local Response" ,
      " group" :" Capacities & Response" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 3" 
   },
   " 305" :{
      " label" :" National Response" ,
      " group" :" Capacities & Response" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 3" 
   },
   " 306" :{
      " label" :" Number Of People Reached/Response Gaps" ,
      " group" :" Capacities & Response" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 3" 
   },
   " 307" :{
      " label" :" Coping Mechanisms" ,
      " group" :" Humanitarian Conditions" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 3" 
   },
   " 308" :{
      " label" :" Living Standards" ,
      " group" :" Humanitarian Conditions" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 3" 
   },
   " 309" :{
      " label" :" Number Of People In Need" ,
      " group" :" Humanitarian Conditions" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 3" 
   },
   " 310" :{
      " label" :" Physical And Mental Well Being" ,
      " group" :" Humanitarian Conditions" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 3" 
   },
   " 311" :{
      " label" :" Driver/Aggravating Factors" ,
      " group" :" Impact" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 3" 
   },
   " 312" :{
      " label" :" Impact On People" ,
      " group" :" Impact" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 3" 
   },
   " 313" :{
      " label" :" Impact On Systems, Services And Networks" ,
      " group" :" Impact" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 3" 
   },
   " 314" :{
      " label" :" Number Of People Affected" ,
      " group" :" Impact" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 3" 
   },
   " 315" :{
      " label" :" Expressed By Humanitarian Staff" ,
      " group" :" Priority Interventions" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 3" 
   },
   " 316" :{
      " label" :" Expressed By Population" ,
      " group" :" Priority Interventions" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 3" 
   },
   " 317" :{
      " label" :" Expressed By Humanitarian Staff" ,
      " group" :" Priority Needs" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 3" 
   },
   " 318" :{
      " label" :" Expressed By Population" ,
      " group" :" Priority Needs" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 3" 
   },
   " 401" :{
      " label" :" Child Head of Household" ,
      " group" :" Specific Needs Group" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 4" 
   },
   " 402" :{
      " label" :" Chronically Ill" ,
      " group" :" Specific Needs Group" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 4" 
   },
   " 403" :{
      " label" :" Elderly Head of Household" ,
      " group" :" Specific Needs Group" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 4" 
   },
   " 404" :{
      " label" :" Female Head of Household" ,
      " group" :" Specific Needs Group" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 4" 
   },
   " 405" :{
      " label" :" GBV survivors" ,
      " group" :" Specific Needs Group" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 4" 
   },
   " 406" :{
      " label" :" Indigenous people" ,
      " group" :" Specific Needs Group" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 4" 
   },
   " 407" :{
      " label" :" LGBTQI+" ,
      " group" :" Specific Needs Group" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 4" 
   },
   " 408" :{
      " label" :" Minorities" ,
      " group" :" Specific Needs Group" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 4" 
   },
   " 409" :{
      " label" :" Persons with Disability" ,
      " group" :" Specific Needs Group" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 4" 
   },
   " 410" :{
      " label" :" Pregnant or Lactating Women" ,
      " group" :" Specific Needs Group" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 4" 
   },
   " 411" :{
      " label" :" Single Women (including Widows)" ,
      " group" :" Specific Needs Group" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 4" 
   },
   " 412" :{
      " label" :" Unaccompanied or Separated Children" ,
      " group" :" Specific Needs Group" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 4" 
   },
   " 901" :{
      " label" :" Infants/Toddlers (<5 years old) " ,
      " group" :" Demographic Groups" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 9" 
   },
   " 902" :{
      " label" :" Female Children/Youth (5 to 17 years old)" ,
      " group" :" Demographic Groups" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 9" 
   },
   " 903" :{
      " label" :" Male Children/Youth (5 to 17 years old)" ,
      " group" :" Demographic Groups" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 9" 
   },
   " 904" :{
      " label" :" Female Adult (18 to 59 years old)" ,
      " group" :" Demographic Groups" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 9" 
   },
   " 905" :{
      " label" :" Male Adult (18 to 59 years old)" ,
      " group" :" Demographic Groups" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 9" 
   },
   " 906" :{
      " label" :" Female Older Persons (60+ years old)" ,
      " group" :" Demographic Groups" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 9" 
   },
   " 907" :{
      " label" :" Male Older Persons (60+ years old)" ,
      " group" :" Demographic Groups" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 9" 
   },
   " 701" :{
      " label" :" Critical" ,
      " group" :" Severity" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 7" 
   },
   " 702" :{
      " label" :" Major" ,
      " group" :" Severity" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 7" 
   },
   " 703" :{
      " label" :" Minor Problem" ,
      " group" :" Severity" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 7" 
   },
   " 704" :{
      " label" :" No problem" ,
      " group" :" Severity" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 7" 
   },
   " 705" :{
      " label" :" Of Concern" ,
      " group" :" Severity" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 7" 
   },
   " 801" :{
      " label" :" Asylum Seekers" ,
      " group" :" Affected Groups" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 8" 
   },
   " 802" :{
      " label" :" Host" ,
      " group" :" Affected Groups" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 8" 
   },
   " 803" :{
      " label" :" IDP" ,
      " group" :" Affected Groups" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 8" 
   },
   " 804" :{
      " label" :" Migrants" ,
      " group" :" Affected Groups" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 8" 
   },
   " 805" :{
      " label" :" Refugees" ,
      " group" :" Affected Groups" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 8" 
   },
   " 806" :{
      " label" :" Returnees" ,
      " group" :" Affected Groups" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 8" 
   },
   " 1001" :{
      " label" :" Completely reliable" ,
      " group" :" Reliability" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 10" 
   },
   " 1002" :{
      " label" :" Usually reliable" ,
      " group" :" Reliability" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 10" 
   },
   " 1003" :{
      " label" :" Fairly Reliable" ,
      " group" :" Reliability" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 10" 
   },
   " 1004" :{
      " label" :" Unreliable" ,
      " group" :" Reliability" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 10" 
   },
   " 501" :{
      " label" :" Female" ,
      " group" :" Gender" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 5" 
   },
   " 502" :{
      " label" :" Male" ,
      " group" :" Gender" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 5" 
   },
   " 601" :{
      " label" :" Adult (18 to 59 years old)" ,
      " group" :" Age" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 6" 
   },
   " 602" :{
      " label" :" Children/Youth (5 to 17 years old)" ,
      " group" :" Age" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 6" 
   },
   " 603" :{
      " label" :" Infants/Toddlers (<5 years old)" ,
      " group" :" Age" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 6" 
   },
   " 604" :{
      " label" :" Older Persons (60+ years old)" ,
      " group" :" Age" ,
      " hide_in_analysis_framework_mapping" :false,
      " is_category" :false,
      " parent_id" :" 6" 
   }
}
```

### Model Info
##### Request: GET `/model_info` [Req from DEEP to DEEPL]
```json

{
   "statusCode": 200,
   "body": {
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
}
```