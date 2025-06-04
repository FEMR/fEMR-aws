#test script to re-create sending data pacakets to CentralAPI from OnChain. 

from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter, Retry
from dotenv import load_dotenv
from faker import Faker

import requests
import os
import random
import json


load_dotenv()

baseUrl = "http://femr-onchain-dev.eba-umphej7e.us-west-2.elasticbeanstalk.com/"
user, pswd = os.getenv('ONCHAIN_USER'), os.getenv('ONCHAIN_PASS')
authCreds = HTTPBasicAuth(user,pswd)

def get_encounter(paitient):
    pId = paitient['id']
    print("Getting Encounters from Paitient ID => ",pId)
    encounter_url = """api/Encounter/{pId}/""".format(pId=pId)

    # Allows for retries for the GET request; retries 5 times of 0s, 2s, 4s, 8s, 16s.
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1)
    s.mount("http://", HTTPAdapter(max_retries=retries))
    resp = s.get(baseUrl+encounter_url, auth=authCreds)
    if resp.ok:
        return json.loads(resp.text)
    else:
        print("Error while getting Encounters", resp.text)
        raise SystemExit

def get_paitients(number):
    # Allows for retries for the GET request; retries 5 times of 0s, 2s, 4s, 8s, 16s.
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1)
    s.mount("http://", HTTPAdapter(max_retries=retries))
    resp = s.get(baseUrl+'api/Patient/', auth=authCreds)
    if resp.ok:
        p_list = json.loads(resp.text)
        p_list = list(map(lambda x: random.choice(p_list), [0]*number ))
        return p_list
    else:
        print("Error while getting Patients", resp.text)
        raise SystemExit
def get_encounters_for_paitients(p_list):
    return list(map(get_encounter, p_list))

def mock_data_transfer(numOfP):
    paitients = get_paitients(numOfP)
    encounter_forP = get_encounters_for_paitients(paitients)
    print("The Paitients to be sent => ", paitients)
    print("The Encounters to be sent => ", encounter_forP)
    #call ping_paitients()
    #call ping_encounters()


# def ping_paitiens_toCentral(p_list):
#     #call api route to take in paitient list in central API

# def ping_encounters(e_list):
#     #call api route to take in encounters list in central API



mock_data_transfer(5)