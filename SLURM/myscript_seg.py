from fastapi import FastAPI, Request
from pydantic import BaseModel
import time
import json
import copy
function= {}
Example = {}

function['A'] = """You are an extraction model designed to identify and extract Personally Identifiable Information (PII) from text and format it into a structured JSON.
Your task is to analyze the provided text and extract the relevant data fields as specified below.

Ensure that the output adheres to the exact JSON structure, including all fields, even if they are empty. If data for a field is not found, output it as "".

"""
function['B'] = """
Please provide only the JSON output, with no additional comments or explanations. Use the following template as base:
"""

function['Person'] = """
The required JSON fields are:
- "Name": Person's full name.
- "Birth_Date": Date of birth.
- "Age": Age of the person.
- "Height": Person's height.
- "Weight": Person's weight.
- "Gender": Person's gender.
- "Marital_Status": Person's marital status.
- "Number_of_Children": Number of children.
- "Place_of_Birth": Birthplace of the person.
- "Mother_Maiden_Name": Mother’s maiden name.
- "Sexual_Preference": Sexual preference.
- "Sex_Life": Sex life details.
"""
Example['Person'] = """
{
    "Name": "",
    "Birth_Date": "",
    "Age": "",
    "Height": "",
    "Weight": "",
    "Gender": "",
    "Marital_Status": "",
    "Number_of_Children": "",
    "Place_of_Birth": "",
    "Mother_Maiden_Name": "",
    "Sexual_Preference": "",
    "Sex_Life": ""
}"""



function['Location'] = """
The required JSON fields are:
- "Home_Town_City": Person's home town.
- "Geographical_Indicators": Geographical Indicators of a Person location.
- "Geo_Location": Coordinates of a Person location.
- "Country": Country where a Person is currently in.
- "ZIP_Code": ZIP Code of a Person Location.
- "Address": Current Address of a Person Location.
- "Date_Time": Date and Time Info on a Person Routine.
"""
Example['Location'] = """
{
    "Home_Town_City": "",
    "Geographical_Indicators": "",
    "Geo_Location": "",
    "Country": "",
    "ZIP_Code": "",
    "Address": "",
    "Date_Time": ""
}"""

function['Contact'] = """
The required JSON fields are:
    - "Home_Address": A list containing: 
        - "Street_Address": A Street name of a Person's home,
        - "City": The City of a Person's Home.
        - "State":The State of a Person's Home.
        - "ZIP_Code": The ZIP Code of a Person's Home.
        - "Country": The Country where a Person's Home is. 
    - "Phone_Number": A Personal Phone Number.
    - "Email_Address": A Person Email Address
    - "Family_Friend_Contact_Information": A Person Related Contact Info.
"""
Example['Contact'] = """
{ 
    "Home_Address": { 
        "Street_Address": "",
        "City": "",
        "State": "",
        "ZIP_Code": "",
        "Country": "" 
    },
    "Phone_Number": "",
    "Email_Address": "",
    "Family_Friend_Contact_Information": ""
}"""

function['Identifiers'] = """
The required JSON fields are:
    - "Personal_Identifiers": A list containing:
        - "National_ID": A Person National Identity Document 
        - "Passport_Number": A Person Passport Number
        - "Social_Security_Number": A Person Social Security Number
        - "Vehicle_Registration": A Person's Vehicle Registration Number
    - "Online_Identifiers": A list containing:
        - "Screen_Name": A Person casual screen name.
        - "Social_Network_Profile": A Person Profile in Social Networks.
        - "Social_Network_Activity": A Person usual activity online.
        - "URLs": A Person related URL.
        - "Online_Aliases": A Person related online Aliases.
        - "IPs": A Person related IP address.   
"""

Example['Identifiers'] = """
{
    "Personal_Identifiers":{
        "National_ID": "", 
        "Passport_Number": "", 
        "Social_Security_Number": "", 
        "Vehicle_Registration": "" 
    }, 
    "Online_Identifiers": { 
        "Screen_Name": "", 
        "Social_Network_Profile": "", 
        "Social_Network_Activity": "", 
        "URLs": "", 
        "Online_Aliases": "", 
        "IPs": "" 
    }
}"""

function['NRP'] = """
The required JSON fields are:
    - "Nationality_Citizenship": A Person Nationality or Citizenship.
    - "Race_Ethnic": A Person Race or Ethnicity.
    - "Religion": A Person Religion.
    - "Philosophical_Belief": A Person Philosophical Belief.
    - "Political_Affiliation": A Person Political Affiliation.
    - "Trade_Union_Affiliation": A Person Trade Union Affiliation. 
"""

Example['NRP'] = """
{
    "Nationality_Citizenship": "",
    "Race_Ethnic": "",
    "Religion": "",
    "Philosophical_Belief": "",
    "Political_Affiliation": "",
    "Trade_Union_Affiliation": ""
}"""


function['Finance'] = """
The required JSON fields are:
    - "Banking_Details": A list containing:
        - "Credit_Card_Number": A Person Credit Card Number
        - "Credit_Score": A Person given credit score
        - "ABA_Routing_Number": A Person ABA Routing Number
        - "Bank_Account_Number": A Person Bank Account Number
        - "Individual_Taxpayer_Identification": A Person Taxpayer Identifier
        - "SWIFT_Code": A Person SWIFT Code
        - "Crypto": A Person Crypto Wallet
    - "Invoice_Payments": A Person Invoice Payment Info
    - "Financial_Information": Any other Financial Related Info.
"""

Example['Finance'] = """
{
    "Banking_Details": {
        "Credit_Card_Number": "",
        "Credit_Score": "",
        "ABA_Routing_Number": "",
        "Bank_Account_Number": "",
        "Individual_Taxpayer_Identification": "",
        "SWIFT_Code": "",
        "Crypto": ""
    },
    "Invoice_Payments": "",
    "Financial_Information": ""
}"""

function['Security'] = """
The required JSON fields are:
    - "Digital_Signature": The HASH Footprint of a Person Digital Signature
    - "Password": A Person related Password for any kind of activity.
    - "License_Numbers": A list containing:
        - "Drivers_License_Number": A Person Driver's Licence Number
        - "Vehicle_Registration_Number": A Person's Vehicle Registration Number
        - "License_Plate_Number": A Licence Plate Number related to a Person.
    - "Biometric_Data": A list containing:
        - "Fingerprint_Data": The biometric information about a Person Fingerprint.
        - "Voice_Print": The Characteristic Data about a Person Voice Print.
        - "Handwriting_Sample": A Sample of a Person Handwrite.
        - "Physiological_Data": Any Phisiological Data related to a Person.
        - "Genetic_Data": Any Genetic Data related to a Person.
        - "X_Ray": Any X Ray log on a Person.
"""

Example['Security'] = """
{
    "Digital_Signature": "",
    "Password": "",
    "License_Numbers": {
        "Drivers_License_Number": "",
        "Vehicle_Registration_Number": "",
        "License_Plate_Number": ""
    },
    "Biometric_Data": {
        "Fingerprint_Data": "",
        "Voice_Print": "",
        "Handwriting_Sample": "",
        "Physiological_Data": "",
        "Genetic_Data": "",
        "X_Ray": ""
    }
}"""

function['Work'] = """
The required JSON fields are:
    - "Job_Title": A Person Job Title
    - "Occupation": A Person Life Occupation
    - "Work_ID": A Person Work related ID
    - "Work_Address": A list containing:
        - "Street_Address": The Address of a Person workplace
        - "City": The City of a Person workplace
        - "State": The State where a Person workplace is.
        - "ZIP_Code": The ZIP Code of a Person workplace.
        - "Country": The Contry where a Person workplace is.
    - "Work_Contact_Information": A list containing:
        - "Work_Phone_Number": A Person Work Phone Number.
        - "Work_Email_Address": A Person Work Email Address.
    - "Employment_Information": A list containing:
        - "Employment_Status": The info on the Employment Status of a Person.
        - "Work_Experience": Info related to Work Experience.
        - "Skills": The said skills of a Person related to a Job.
        - "Education": The Educational Level of a Person.
    - "Income_Level": Info related to a Person Income Level.
"""

Example['Work'] = """
{
    "Job_Title": "",
    "Occupation": "",
    "Work_ID": "",
    "Work_Address": {
        "Street_Address": "",
        "City": "",
        "State": "",
        "ZIP_Code": "",
        "Country": ""
    },
    "Work_Contact_Information": {
        "Work_Phone_Number": "",
        "Work_Email_Address": ""
    },
    "Employment_Information": {
        "Employment_Status": "",
        "Work_Experience": "",
        "Skills": "",
        "Education": ""
    },
    "Income_Level": ""
}"""

function['Others'] = """
The required JSON fields are:
    - "Health_Information": A list containing:
        - "Health_Insurance_ID": The Health Insurance ID Number of a Person.
        - "Medical_History": Info related to the Medical History of a Person.
        - "Physiological_Data": Info related to Phisiological Data of a Person.
    - "Cultural_and_Social_Identity": A list containing:
        - "Cultural_Social_Identity": A Person Socio-cultural Identity.
        - "Shopping_Behavior": Info related to Shopping Behavior of a Person.
        - "Survey_Answers": Any Survey related answers related to a Person.
        - "Signed_Petitions": Any Signed Petitions Info related to a Person.
        - "Activities": Any extra activities related to a Person.
        - "Law_Enforcement_Records": Any Law Enforcing Records related to a Person.
    - "Appearance": A list containing:
        - "Picture_of_Face": The Bitcode related to a Person's Facial Footprint or a Description of a Person Face.
        - "Distinguishing_Characteristic": A Person full-body recognizable characteristics.
"""

Example['Others'] = """
{
    "Health_Information": {
        "Health_Insurance_ID": "",
        "Medical_History": "",
        "Physiological_Data": ""
    },
    "Cultural_and_Social_Identity": {
        "Cultural_Social_Identity": "",
        "Shopping_Behavior": "",
        "Survey_Answers": "",
        "Signed_Petitions": "",
        "Activities": "",
        "Law_Enforcement_Records": ""
    },
    "Appearance": {
        "Picture_of_Face": "",
        "Distinguishing_Characteristic": ""
    }
}"""


eqi_table = {}

eqi_table['Person'] = ['LOCATION','PERSON']
eqi_table['Location'] = ['DATE_TIME','LOCATION']
eqi_table['Contact'] = ['LOCATION','PHONE_NUMBER']
eqi_table['Identifiers'] = ['IP_ADDRESS','URL','US_PASSPORT','US_SSN','UK_NINO','ES_NIF','ES_NIE','IT_FISCAL_CODE','IT_PASSPORT','IT_IDENTITY_CARD','PL_PESEL','SG_NRIC_FIN','SG_UEN','AU_ABN','AU_ACN','IN_PAN','IN_AADHAAR','IN_VOTER','IN_PASSPORT','FI_PERSONAL_IDENTITY_CODE','ID']
eqi_table['NRP'] = ['NRP','IN_VOTER']
eqi_table['Finance'] = ['CREDIT_CARD','CRYPTO','IBAN_CODE','US_BANK_NUMBER','US_ITIN','UK_NINO','IT_FISCAL_CODE','IT_VAT_CODE','AU_TFN']
eqi_table['Security'] = ['IT_DRIVER_LICENSE','US_DRIVER_LICENSE','IN_VEHICLE_REGISTRATION']
eqi_table['Work'] = ['DATE_TIME','LOCATION','MEDICAL_LICENSE','AU_ABN']
eqi_table['Others'] = ['MEDICAL_LICENSE','UK_NHS','UK_NINO','AU_MEDICARE']

table_eqi = {}
table_eqi['PERSON'] = {'Person':['Name',
                                 'Mother_Maiden_Name'],
                       'Contact':['Family_Friend_Contact_Info']
                      }


table_eqi['LOCATION'] = {'Person':['Place_of_Birth'],
                         'Location': ['Home_Town_City',
                                      'Country',
                                      'Address'],
                         'Contact':{'Home_Address': ['Street_Address',
                                                     'City',
                                                     'State',
                                                     'Country']
                                   }
                        }

table_eqi['EMAIL'] = {'Contact':['Email_Address'],
                          'Work': {'Work_Contact_Info':['Work_Email_Address']
                                  }
                     }

table_eqi['DATE_TIME'] = {'Person':['Birth_Date'],
                          'Location':['Date_Time']
                         }

table_eqi['NRP'] = {'NRP':['Nationality_Citizenship',
                           'Race_Ethnic',
                           'Religion',
                           'Philosophical_Belief',
                           'Political_Affiliation',
                           'Trade_Union_Affiliation']
                   }

table_eqi['PASSPORT'] = {'Identifiers':{'Personal_Identifiers': ['Passport_Number']
                                       },
                        }

table_eqi['PHONE_NUMBER'] = {'Contact':['Phone_Number'],
                             'Work':{'Work_Contact_Information':['Work_Phone_Number']
                                    }
                            }

table_eqi['URL'] = {'Identifiers':{'Online_Identifiers': ['URLs']
                                       }
                        }



# -- vLLM parameters
import asyncio
import httpx
import os
model = os.getenv("MYMODEL", "Qwen/Qwen2.5-3B-Instruct")
print(f"Model {model}")
model_len = int(os.getenv("MYMODEL_LEN", 1024*4))
host = os.getenv("MYHOST", "localhost")
port = int(os.getenv("MYPORT", 8000))
API_KEY = os.getenv("MYKEY","")
BASE_URL = f"http://{host}:{port}/v1/chat/completions"

print(f"Base URL: {BASE_URL}" )
# --- Tokenizer & LLM Placeholder ---
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(model)



from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer, RecognizerRegistry

#-- Presidio ---
ID_pattern = Pattern(name="ID", regex='\\w{0,1} ?\\d{8} ?-? ?\\w{0,1}', score=0.7)
ID_recognizer = PatternRecognizer(supported_entity="ID", patterns=[ID_pattern])

Cards_pattern = Pattern(name='CC', regex='\\b((4\\d{3}|5[1-5]\\d{2}|2\\d{3}|3[47]\\d{1,2})[\\s\\-]?\\d{4,6}[\\s\\-]?\\d{4,6}?([\\s\\-]\\d{3,4})?(\\d{3})?)\\b', score=0.7)
Cards_recognizer = PatternRecognizer(supported_entity="CC", patterns=[Cards_pattern])

registry = RecognizerRegistry()
registry.load_predefined_recognizers()
registry.add_recognizer(ID_recognizer)
registry.add_recognizer(Cards_recognizer)

analyzer = AnalyzerEngine(registry=registry, default_score_threshold=0.3)



# --- Funciones auxiliares ---

class TextRequest(BaseModel):
    text: str

async def call_llm(message):
    if message == []:
        return output
    API_KEY = ""
    headers = {
        "Authorization": f"Bearer EMPTY",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": message["data"],
        "temperature":0,
        "top_p":0.2,
        "max_tokens":512*18

    }
    print(headers)
    print(payload)
    timeout = httpx.Timeout(connect=10.0,read=60.0,write=60.0,pool=5.0)
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(BASE_URL, json=payload, headers=headers)

            response.raise_for_status()
            print(f"RESPONSE {response}")
            result = {message["type"]:response.json()["choices"][0]["message"]["content"]}
        return result
    except httpx.RequestError as e:
        print(f"Error de solicitud: {e}")
        response.headers
        return ""
    except httpx.HTTPStatusError as e:
        print(f"Error de HTTP: {e}")
        response.headers
        return ""
def parse_output(outputs,cmp):
    out_temp = cmp
    for i in outputs:
        try:
            print("****************************")
            key = list(i.keys())[0]
            print(key)
            l = json.loads(i[key])
            out_temp[key] = l
        except:
            out_temp[key] = cmp[key]
    return out_temp

def split_document(document, window_size, overlap):
    tokens = tokenizer.tokenize(document)
    chunks = []
    if len(tokens) > window_size:
        for i in range(0, len(tokens), window_size - overlap):
            chunk = tokenizer.convert_tokens_to_string(tokens[i:i + window_size])
            chunks.append(chunk)
            if i + window_size >= len(tokens):
                break
    else:
        chunks.append(document)
    return chunks

def parse_presidio(data,templates,eqi_table):
    out_pulses = {}
    types = []
    for i in data:
         if i.entity_type not in types:
            types.append(i.entity_type)
    for temp in templates:
        if any(x in types for x in eqi_table[temp]):
            out_pulses[temp] = 1
        else:
            out_pulses[temp] = 0
    return out_pulses
def build_messages(text,templates, out_pulse, cmp):
    text2 = []
    for var in templates:
        if out_pulse[var] == 1:
            print(f"----------")
            print(cmp[var])
            print(f"----------")
            messages = {
                "data":[
                    {"role": "system", "content": (function['A'] + function[var] + function['B'] + cmp[var])},
                    {"role": "user", "content": text}
                ],
                "type": var
            }
            text2.append(messages)
    return text2

async def get_inference(text):
    templates = Example.keys()
    results = analyzer.analyze(text=text, language='en')
    chunks = split_document(text, model_len//2, model_len//8)
    pulses = parse_presidio(results,templates,eqi_table)
    #output = Example['Template']
    print(pulses)
    outputs = copy.deepcopy(Example)
    start = time.time()
    for chunk in chunks:
        messages = build_messages(chunk,templates,pulses,outputs)
        temps = await asyncio.gather(*[call_llm(message) for message in messages])
        outputs = parse_output(temps,outputs)
    end = time.time()
    print("done")
    return results, outputs, end - start
class TextRequest(BaseModel):
    text: str

# --- FastAPI Server ---
app = FastAPI()
print(f"APP Ready")
print(API_KEY)

@app.post("/extract_pii")
async def extract_pii(request: TextRequest):
    results, structured_json, duration = await get_inference(request.text)
    print(structured_json)
    return {
        "duration": duration,
        "structured_json": structured_json,
        "results": results
    }

