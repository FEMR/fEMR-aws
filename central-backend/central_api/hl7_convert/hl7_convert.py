# Functions that take in fEMR data as JSONs and converts it to a specified HL7-FHIR JSON.

# Raised when an undefined error has occurred during the JSON conversion process (e.g., missing required 
# field, connection closed, etc.)
class JSONConversionError(Exception):
    def __init__(self, message="Error has occurred during JSON conversion process."):
        super().__init__(message)

class InputTypeError(Exception):
    def __init__(self, message="Conversion function requires a dictionary input."):
        super().__init__(message)



"""
Takes in fEMR data as various JSONs and creates a HL7-FHIR Patient JSON from available data fields.
The returned Patient JSON is not fully compliant with HL7-FHIR, as they use multiple custom class objects
to represent certain parts of the data (e.g., we have "name" as a string when they have a "HumanName"
object that includes the name, its use, family/given name, and their "name" field can support multiple HumanName's).
HL7-FHIR Patient JSON being returned is modeled from the JSON template from https://hl7.org/fhir/patient.html.

patient = fEMR Patient JSON, fields based from https://chain.teamfemr.org/swagger/
We assume required fields, as marked in the swagger documentation, do not need to be checked for if they exist.
"""
def convert_femr_to_hl7_patient(patient): 
    # Checks that 'patient' input is a dictionary type before any processing/data generation is done.
    if (type(patient) != type({})):
        raise InputTypeError()
    
    hl7_patient = {
        "resourceType" : "Patient",
        "identifier" : {
            "id" : None,
            "campaign_key" : None
        },
        "active" : True,
        "name" : "",
        "telecom" : [],
        "gender" : "", 
        "birthDate" : "",
        "deceasedBoolean" : False,
        "address" : {
            "current_address" : "",
            "address1" : "",
            "address2" : "",
            "zip_code" : "",
            "city" : "",
            "state" : "",
            "previous_address" : ""
        },
        "maritalStatus" : False,
        "multipleBirthBoolean" : False,
        "photo" : [],
        "contact" : [],
        "communication" : [],
        "generalPractitioner" : [],
        "managingOrganization" : "",
        "link" : []
    }

    # Keys from 'patient' are named after ones from GET /api/Patient/ in chain.teamfemr.org/swagger/
    try:
        if ("id" in patient):
            hl7_patient["identifier"]["id"] = patient["id"]
        
        if ("campaign_key" in patient):
            hl7_patient["identifier"]["campaign_key"] = patient["campaign_key"]


        if ("middle_name" in patient):
            hl7_patient["name"] = "{0} {1} {2}".format(patient["first_name"], patient["middle_name"], patient["last_name"])
        else:
            hl7_patient["name"] = "{0} {1}".format(patient["first_name"], patient["last_name"])


        if (patient["shared_phone_number"]):
            phone_number_info = {
                "phone_number" : patient["phone_number"],
                "phone_number_type" : None
            }

            if ("phone_number_type" in patient):
                phone_number_info["phone_number_type"] = patient["phone_number_type"]

            hl7_patient["telecom"].append(phone_number_info)
        
        if (patient["shared_email_address"]):
            hl7_patient["telecom"].append(patient["email_address"])

        
        gender = patient["sex_assigned_at_birth"]
        if (gender == "f"):
            hl7_patient["gender"] = "female"
        elif (gender == "m"):
            hl7_patient["gender"] = "male"
        elif (gender == "o"):
            hl7_patient["gender"] = "other"
        else:
            hl7_patient["gender"] = "unknown"

        # if (patient["date_of_birth"]):        
        #     hl7_patient["birthDate"] = patient["date_of_birth"]

        # TODO: For next quarter, consider creating a function that takes in string keys and does the lookup/assigning
        if ("current_address" in patient):
            hl7_patient["address"]["current_address"] = patient["current_address"]
        
        if ("address1" in patient):
            hl7_patient["address"]["address1"] = patient["address1"]
        
        if ("address2" in patient):
            hl7_patient["address"]["address2"] = patient["address2"]

        if ("zip_code" in patient):
            hl7_patient["address"]["zip_code"] = patient["zip_code"]
        
        if ("city" in patient):
            hl7_patient["address"]["city"] = patient["city"]
        
        if ("state" in patient):
            hl7_patient["address"]["state"] = patient["state"]
        
        if ("previous_address" in patient):
            hl7_patient["address"]["previous_address"] = patient["previous_address"]
        

        # TODO: Check for more fields that can be filled out in hl7_patient

    except KeyError as e:
        raise JSONConversionError()

    return hl7_patient


"""
Takes in fEMR data as various JSONs and creates a HL7-FHIR Observation JSON from available data fields.
Observation JSON is modeled from the JSON template from https://hl7.org/fhir/observation.html.

Currently is incomplete and is only to show what an HL7-FHIR Observation JSON/record looks like (what fields
it contains). This will be worked on in CSC406 as needed.
"""
def convert_femr_to_hl7_observation():
    hl7_observation = {
        "resourceType" : "Observation",
        "identifier" : [],
        "basedOn" : [],
        "partOf" : [],
        "status" : "",
        "category" : [],
        "code" : "",
        "subject" : "",
        "focus" : [],
        "encounter" : "",
        "effectiveDateTime" : "",
        "issued" : "",
        "performer" : [],
        "valueString" : "",
        "dataAbsentReason" : "",
        "interpretation" : [],
        "note" : [],
        "bodySite" : "",
        "method" : "",
        "specimen" : "",
        "device" : "",
        "referenceRange" : [],
        "hasMember" : [],
        "derivedFrom" : [],
        "component" : []
    }

    return hl7_observation


# For local testing purposes only 
def main():
    femr_patient = {
        "id" : 1,
        "campaign_key" : 2,
        "first_name" : "Abc",
        "middle_name" : "Def",
        "last_name" : "Ghi",
        "suffix" : "jr",
        "social_security_number" : "123-45-6789",
        "sex_assigned_at_birth" : "o", 
        "date_of_birth" : "2000-01-01",
        "age" : 22,
        "shared_phone_number" : True,
        "phone_number" : "1234567890",
        "shared_email_address" : True,
        "email_address" : "adghi@calpoly.edu"
    }

    hl7_patient = convert_femr_to_hl7_patient(femr_patient)
    print(hl7_patient)

    # improper_data = [("id", 2), ("campaign_key", 3), ("first_name", "Jkl")]
    # convert_attempt = convert_femr_to_hl7_patient(improper_data)

    improper_data_2 = {}
    convert_attempt_2 = convert_femr_to_hl7_patient(improper_data_2)

    # hl7_observation = convert_femr_to_hl7_observation()
    # print(hl7_observation)

if __name__ == "__main__":
    main()