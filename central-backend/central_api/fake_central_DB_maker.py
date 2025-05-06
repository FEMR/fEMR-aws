from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter, Retry
from dotenv import load_dotenv
from faker import Faker

import requests
import random
import datetime
import os
import json


load_dotenv()
centralUrl = "http://femr-onchain-dev.eba-umphej7e.us-west-2.elasticbeanstalk.com/"
user, pswd = os.getenv('CENTRAL_USER'), os.getenv('CENTRAL_PASS')
fake_paitient_list = []
authCreds = HTTPBasicAuth(user,pswd)

def get_campaign_ids():
    # Allows for retries for the GET request; retries 5 times of 0s, 2s, 4s, 8s, 16s.
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1)
    s.mount("http://", HTTPAdapter(max_retries=retries))
    resp = s.get(baseUrl+'api/Campaign/',auth=authCreds)

    if resp.ok:
        return(json.loads(resp.text))
    else:
        print("Error out while getting campain ids", resp.text)
        raise SystemExit


def get_cheif_complaint():
    # Allows for retries for the GET request; retries 5 times of 0s, 2s, 4s, 8s, 16s.
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1)
    s.mount("http://", HTTPAdapter(max_retries=retries))
    resp = s.get(baseUrl+"api/ChiefComplaint/", auth=authCreds)
    
    if resp.ok:
        return(random.choice(json.loads(resp.text))['id'])
    else:
        print("Errored out while getting cheif_complaint()", resp.text)
        raise SystemExit


sexs = [ 'f', 'm', 'o' ]
fake = Faker()

def create_fake_paitient(num):
    p = {}
    dob = fake.date_of_birth()
    p['first_name'] = fake['en-US'].first_name()
    p['last_name'] = fake['en-US'].last_name()
    p['sex_assigned_at_birth'] = random.choice(sexs)
    p['date_of_birth'] = str(dob.year)+"-"+str(dob.month)+"-"+str(dob.day)
    p['age'] = int(datetime.datetime.today().year) - int(dob.year)
    p['shared_phone_number'] =False
    p['shared_email_address'] = False
    campaing = random.choice(get_campaign_ids())
    p['campaign'] = 1
    p['ethnicity'] = random.choice(campaing['ethnicity_options'])
    p['race'] = random.choice(campaing['race_options'])
    new_p = requests.post(baseUrl+'api/Patient/', data=p,auth =authCreds)
    if new_p.ok:
        fake_p = json.loads(new_p.text)
        fake_p['camp'] = campaing
        fake_paitient_list.append(fake_p)
        # print("New Patient Created = id:",fake_p['id'] , " => ", fake_p['first_name'], " ", fake_p['last_name'] )
        return p
    else:
        print("Error while posting Patitents", new_p.text)
        raise SystemExit


def create_fake_encounter(fake_p):
    encounter= {}
    encounter['timestamp'] = datetime.datetime.now().isoformat()
    encounter['campaign '] = fake_p['camp']['id']
    encounter['chief_complaint'] = [get_cheif_complaint()]
    encounter['patient'] = fake_p['id']
    fake_encounter = requests.post(baseUrl+'api/Encounter/', data=encounter,auth =authCreds)
    if fake_encounter.ok:
        return json.loads(fake_encounter.text)
    else:
        print("Error while posting Encounters",fake_encounter.text)
        raise SystemExit


def populate_paitient_schema(number):
    fakes = list(map(create_fake_paitient, [1]*number))
    return fakes


def populate_encounter_schema(number):
    for i in range(number):
        p = random.choice(fake_paitient_list)
        enc = create_fake_encounter(p)
        print("Created Fake Encounters = id:", enc['id'], "for paitientId:", p['id'])


def popluate_test_db(p_number=5, encounter=3):
    populate_paitient_schema(p_number)
    populate_encounter_schema(encounter)
    return fake_paitient_list

popluate_test_db(1, 1)