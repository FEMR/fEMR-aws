from fake_onChain_DB_maker import popluate_test_db
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter, Retry
from hl7_convert.hl7_convert import *
from dotenv import load_dotenv

import os
import json
import requests


load_dotenv()
baseUrl = "http://femr-onchain-dev.eba-umphej7e.us-west-2.elasticbeanstalk.com/"
user, pswd = os.getenv('ONCHAIN_USER'), os.getenv('ONCHAIN_PASS')
fake_paitient_list = []
authCreds = HTTPBasicAuth(user,pswd)
def prGreen(stmt): print("\033[92m {}\033[00m" .format(stmt))
def prYellow(stmt): print("\033[93m {}\033[00m" .format(stmt))



def run_demo():
    prYellow("| Starting Demo to populate FEMR Central DB (dev-env) ...")
    fake_p = popluate_test_db(1,1)
    print("Patient Created : ", fake_p[0])
    prGreen(">>> Created fake patient in OnChain DB!")
    print(" ")
    prYellow("| Sending patient to Central API to store ...")
    resp = requests.post('http://127.0.0.1:8000/api/Patient/', json=fake_p[0])
    if resp.ok:
        prGreen(">>> Stored fake patient in FEMR Central DB!" + str(resp))
        print(" ")
        prYellow("| Mocking data transformation from FEMR Central schema to HL7 FHIR schema...")

        # Allows for retries for the GET request; retries 5 times of 0s, 2s, 4s, 8s, 16s.
        s2 = requests.Session()
        retries = Retry(total=5, backoff_factor=1)
        s2.mount("http://", HTTPAdapter(max_retries=retries))
        resp2 = s2.get('http://127.0.0.1:8000/api/Patient/')
        if not resp2.ok:
            print("Error while getting data from central api",resp2.data)
            raise SystemExit   
        prGreen(">>> Succesfully retrieved Patient Data" + str(resp2))
        print(" ")
        prYellow("| Finding added patient data...")
        p_list = json.loads(resp2.content.decode('utf-8'))
        for i in p_list:
            if (i['first_name'] == fake_p[0]['first_name'] and i['last_name'] == fake_p[0]['last_name']):
                hl7_p = convert_femr_to_hl7_patient(i)
                prGreen(">>> Converted central patient to HL7 FHIR!")
                print(hl7_p)
                return
        prYellow("| ERROR: Could not find patient in response")
    else:
        print("Error while posting data to central api",resp)
        raise SystemExit

run_demo()