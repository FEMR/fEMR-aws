from hl7_convert import *

import pytest

# Tests for proper naming conversion, including when "middle_name" field may not exist, in convert_femr_to_hl7_patient().
def test_convert_femr_to_hl7_patient_check_name():
    femr_mock_patient_mid_name = {
        "first_name" : "Abc",
        "middle_name" : "Def",
        "last_name" : "Ghi",
        "sex_assigned_at_birth" : "o",
        "shared_phone_number" : False,
        "shared_email_address" : False,
        "date_of_birth" : "2000-01-01"
    }

    femr_mock_patient_no_mid = {
        "first_name" : "Jkl",
        "last_name" : "Mno",
        "sex_assigned_at_birth" : "o",
        "shared_phone_number" : False,
        "shared_email_address" : False,
        "date_of_birth" : "2000-01-01"
    }

    hl7_patient_mid = convert_femr_to_hl7_patient(femr_mock_patient_mid_name)
    hl7_patient_no_mid = convert_femr_to_hl7_patient(femr_mock_patient_no_mid)

    assert hl7_patient_mid["resourceType"] == "Patient"
    assert hl7_patient_no_mid["resourceType"] == "Patient"

    assert hl7_patient_mid["name"] == "Abc Def Ghi"
    assert hl7_patient_no_mid["name"] == "Jkl Mno"


# Tests for proper date-of-birth conversion in convert_femr_to_hl7_patient().
def test_convert_femr_to_hl7_patient_check_dob():
    femr_mock_patient_dob = {
        "first_name" : "Pqr",
        "last_name" : "Stu",
        "sex_assigned_at_birth" : "o",
        "shared_phone_number" : False,
        "shared_email_address" : False,
        "date_of_birth" : "2000-01-01"
    }

    hl7_patient = convert_femr_to_hl7_patient(femr_mock_patient_dob)

    assert hl7_patient["resourceType"] == "Patient"
    assert hl7_patient["birthDate"] == "2000-01-01"


# Tests that convert_femr_to_hl7_patient() properly raises JSONConversionError if an error occurs
# during the conversion process.
def test_convert_json_conversion_error_hl7_patient():
    femr_mock_patient_wrong = {
        "last_name" : "Nofirst", 
        "sex_assigned_at_birth" : "o",
        "shared_phone_number" : False,
        "shared_email_address" : False,
        "date_of_birth" : "2000-01-01"
    }

    with pytest.raises(JSONConversionError):
        hl7_patient = convert_femr_to_hl7_patient(femr_mock_patient_wrong)


# Tests for proper gender coding conversion in convert_femr_to_hl7_patient().
def test_convert_femr_to_hl7_patient_check_gender():
    femr_mock_patient_male = {
        "first_name" : "Vwx",
        "last_name" : "Yza",
        "sex_assigned_at_birth" : "m",
        "shared_phone_number" : False,
        "shared_email_address" : False,
        "date_of_birth" : "2000-01-01"
    }

    hl7_patient_male = convert_femr_to_hl7_patient(femr_mock_patient_male)

    femr_mock_patient_male["sex_assigned_at_birth"] = "f"
    femr_mock_patient_female = femr_mock_patient_male

    hl7_patient_female = convert_femr_to_hl7_patient(femr_mock_patient_female)

    femr_mock_patient_male["sex_assigned_at_birth"] = "o"
    femr_mock_patient_other = femr_mock_patient_male

    hl7_patient_other = convert_femr_to_hl7_patient(femr_mock_patient_other)

    femr_mock_patient_male["sex_assigned_at_birth"] = "unknown"
    femr_mock_patient_unknown = femr_mock_patient_male

    hl7_patient_unknown = convert_femr_to_hl7_patient(femr_mock_patient_unknown)

    assert hl7_patient_male["resourceType"] == "Patient"
    assert hl7_patient_female["resourceType"] == "Patient"
    assert hl7_patient_other["resourceType"] == "Patient"
    assert hl7_patient_unknown["resourceType"] == "Patient"

    assert hl7_patient_male["gender"] == "male"
    assert hl7_patient_female["gender"] == "female"
    assert hl7_patient_other["gender"] == "other"
    assert hl7_patient_unknown["gender"] == "unknown"


# Tests for proper address fields conversion in convert_femr_to_hl7_patient().
def test_convert_femr_to_hl7_patient_check_address():
    femr_mock_patient_full_addr = {
        "first_name" : "Bcd",
        "last_name" : "Efg",
        "sex_assigned_at_birth" : "o",
        "shared_phone_number" : False,
        "shared_email_address" : False,
        "date_of_birth" : "2000-01-01",
        "current_address" : "1 Grand Ave",
        "address1" : "Office Building 1",
        "address2" : "Cubicle #3",
        "zip_code" : "54321",
        "city" : "SLO",
        "state" : "CA",
        "previous_address" : "5 Grand St"
    }

    hl7_patient_full_addr = convert_femr_to_hl7_patient(femr_mock_patient_full_addr)

    assert hl7_patient_full_addr["resourceType"] == "Patient"
    assert hl7_patient_full_addr["address"]["current_address"] == "1 Grand Ave"
    assert hl7_patient_full_addr["address"]["address1"] == "Office Building 1"
    assert hl7_patient_full_addr["address"]["address2"] == "Cubicle #3"
    assert hl7_patient_full_addr["address"]["zip_code"] == "54321"
    assert hl7_patient_full_addr["address"]["city"] == "SLO"
    assert hl7_patient_full_addr["address"]["state"] == "CA"
    assert hl7_patient_full_addr["address"]["previous_address"] == "5 Grand St"