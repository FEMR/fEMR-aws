import this
import json

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from pymysql import NULL
from .models import Patient as PatientModel,State
from central_api. models import *
from central_api.serializers import *
from central_api.hl7_convert.hl7_convert import *




# Create your views here.

#Central API view that details the POST method to convert an incoming json 
#from OnChain into a patient record in our database
# Some items are commented out for use in future legacy implementation
@method_decorator(csrf_exempt, name='dispatch')
class Patient(View):
    #this.csrf_protect()
    #need to pass in api request into 'request' below
    def post(self, request):
        print("Print request:", request.body.decode("utf-8"))
        data = request.body.decode("utf-8")
        data = json.loads(data)
        p_id = data.get('id')
        p_campaign_key = data.get('campaign_key')
        p_first_name = data.get('first_name')
        p_middle_name = data.get('middle_name')
        p_last_name = data.get('last_name')
        # p_suffix = data.get('suffix')
        p_social_security_number = data.get('social_security_number')
        p_sex_assigned_at_birth = data.get('sex_assigned_at_birth')
        # p_explain = data.get('explain')
        # p_date_of_birth = data.get('date_of_birth')
        p_age = data.get('age')
        # p_preferred_language = data.get('preferred_language')
        p_current_address = data.get('current_address')
        p_address1 = data.get('address1')
        p_address2 = data.get('address2')
        p_zip_code = data.get('zip_code')
        p_city = data.get('city')
        # p_previous_address = data.get('previous_address')
        p_phone_number = data.get('phone_number')
        p_phone_number_type = data.get('phone_number_type')
        p_shared_phone_number = data.get('shared_phone_number')
        p_email_address = data.get('email_address')
        p_shared_email_address = data.get('shared_email_address')
        p_timestamp = data.get('timestamp')
        # p_race = data.get('race')
        # p_ethnicity = data.get('ethnicity')
        p_state = data.get('state')
        p_campaign = data.get('campaign')

        patient_data = {
            #'on_chain_id': p_id,
            'id': p_id,
            'first_name': p_first_name,
            'middle_name': p_middle_name,
            'last_name': p_last_name,
            #'suffix': p_suffix,
            #'legacy_id':
            #'userid': 
            'phone_number': p_phone_number,
            'age': p_age,
            'sex_assigned_at_birth': p_sex_assigned_at_birth,
            'current_address': p_current_address,
            'address1': p_address1,
            'address2': p_address2,
            'city': p_city,
            # 'photo': p_photo,
            # 'patientencounter': p_patientencounter,
            # 'deleted': p_deleted,
            'social_security_number': p_social_security_number,
            'zip_code': p_zip_code,
            'city': p_city,
            'state': State.objects.get(pk=p_state),
            'phone_number': p_phone_number,
            'phone_number_type': p_phone_number_type,
            'shared_phone_number': p_shared_phone_number,
            'email_address': p_email_address,
            'shared_email_address': p_shared_email_address,
            'timestamp': p_timestamp,
            # 'campaign_key': p_campaign_key,

        }

        patient = PatientModel(**patient_data)
        patient.save()
        #add many to many attributes here
        # patient.campaign.set(p_campaign_key) 
        # patient.save()
        return JsonResponse(data, status=201)

    def get(self, request):
        count = PatientModel.objects.count()
        attributes = PatientModel.objects.all()
        patient_data = []
        for attribute in attributes:
            patient_data.append({
                #'on_chain_id': p_id,
                'id': attribute.id,
                'first_name': attribute.first_name,
                'middle_name': attribute.middle_name,
                'last_name': attribute.last_name,
                #'suffix': p_suffix,
                #'legacy_id':
                #'userid': 
                'phone_number': attribute.phone_number,
                'age': attribute.age,
                'sex_assigned_at_birth': attribute.sex_assigned_at_birth,
                'current_address': attribute.current_address,
                'address1': attribute.address1,
                'address2': attribute.address2,
                'city': attribute.city,
                # 'photo': p_photo,
                # 'patientencounter': p_patientencounter,
                # 'deleted': p_deleted,
                'social_security_number': attribute.social_security_number,
                'zip_code': attribute.zip_code,
                'city': attribute.city,
                'state': attribute.state.id if attribute.state is not None else None ,
                'phone_number': attribute.phone_number,
                'phone_number_type': attribute.phone_number_type,
                'shared_phone_number': attribute.shared_phone_number,
                'email_address': attribute.email_address,
                'shared_email_address': attribute.shared_email_address,
                'timestamp': attribute.timestamp,
                # 'campaign_key': p_campaign_key,
            })
        data = {
            'data': patient_data,
            'count': count,
        }
        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class HL7FHIR(View):
    def get(self, request):
        patientId = self.kwargs['patientId']
        patient = Patient.get(patientId)
        hl7_patient = convert_femr_to_hl7_patient(patient)
        return JsonResponse(hl7_patient)

# ja removed views that caused attribute error


# ja fixed view for creating and getting diagnosis
@api_view(['GET', 'POST'])
def diagnosis_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE DIAGNOSIS")
    if request.method == 'GET':
        all_diagnosis = Diagnosis.objects.all()
        serializer = DiagnosisSerializer(all_diagnosis, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING A NEW DIAGNOSIS")
        serializer = DiagnosisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ja fixed view for creating and getting AdministrationSchedule
@api_view(['GET', 'POST'])
def administration_schedule_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE administration_schedule")
    if request.method == 'GET':
        all_admin_schedule = AdministrationSchedule.objects.all()
        serializer = AdministrationScheduleSerializer(all_admin_schedule, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING administration_schedule")
        serializer = AdministrationScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ja fixed view for creating and getting PatientAgeClassification
@api_view(['GET', 'POST'])
def patient_age_classification_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE PatientAgeClassification")
    if request.method == 'GET':
        all_patient_age_classification = PatientAgeClassification.objects.all()
        serializer = PatientAgeClassificationSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING PatientAgeClassification")
        serializer = PatientAgeClassificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 # ja added treatment view
@api_view(['GET', 'POST'])
def treatment_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Treatments")
    if request.method == 'GET':
        all_treatment = Treatment.objects.all()
        serializer = TreatmentSerializer(all_treatment, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Treatment")
        serializer = TreatmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def photo_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE administration_schedule")
    if request.method == 'GET':
        all_patient_age_classification = Photo.objects.all()
        serializer = PhotoSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING PatientAgeClassification")
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
def patient_prescription_replacement_reason_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE PatientPrescriptionReplacementReason")
    if request.method == 'GET':
        all_patient_age_classification = PatientPrescriptionReplacementReason.objects.all()
        serializer = PatientPrescriptionReplacementReasonSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING PatientPrescriptionReplacementReason")
        serializer = PatientPrescriptionReplacementReasonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def patient_encounter_vital_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE PatientVitals")
    if request.method == 'GET':
        vitals = PatientEncounterVital.objects.all()
        serializer = PatientEncounterVitalSerializer(vitals, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING PatientVitals")
        serializer = PatientEncounterVitalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def patient_diagnosis_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE PatientVitals")
    if request.method == 'GET':
        diagnoses = PatientDiagnosis.objects.all()
        serializer = PatientDiagnosisSerializer(diagnoses, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING PatientVitals")
        serializer = PatientDiagnosisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST'])
def patient_prescriptions_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE PatientVitals")
    if request.method == 'GET':
        prescriptions = PatientPrescriptions.objects.all()
        serializer = PatientPrescriptionsSerializer(prescriptions, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING PatientVitals")
        serializer = PatientPrescriptionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def history_of_present_illness_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE HistoryOfPresentIllness")
    if request.method == 'GET':
        all_patient_age_classification = HistoryOfPresentIllness.objects.all()
        serializer = HistoryOfPresentIllnessSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING HistoryOfPresentIllness")
        serializer = HistoryOfPresentIllnessSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def vital_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE PatientPrescriptionReplacementReason")
    if request.method == 'GET':
        all_patient_age_classification = Vital.objects.all()
        serializer = VitalSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING PatientPrescriptionReplacementReason")
        serializer = VitalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def role_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = Role.objects.all()
        serializer = RoleSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def tab_field_size_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = TabFieldSize.objects.all()
        serializer = TabFieldSizeSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = TabFieldSizeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def tab_field_type_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = TabFieldType.objects.all()
        serializer = TabFieldTypeSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = TabFieldTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def tab_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = Tab.objects.all()
        serializer = TabSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = TabSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def inventory_form_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = InventoryForm.objects.all()
        serializer = InventoryFormSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = InventoryFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def inventory_category_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = InventoryCategory.objects.all()
        serializer = InventoryCategorySerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = InventoryCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def manufacturer_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = Manufacturer.objects.all()
        serializer = ManufacturerSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = ManufacturerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def concept_medication_forms_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = ConceptMedicationForms.objects.all()
        serializer = ConceptMedicationFormsSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = ConceptMedicationFormsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def medication_generics_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = MedicationGenerics.objects.all()
        serializer = MedicationGenericsSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = MedicationGenericsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def concept_medication_unit_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = ConceptMedicationUnit.objects.all()
        serializer = ConceptMedicationUnitSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = ConceptMedicationUnitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def mission_country_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = MissionCountry.objects.all()
        serializer = MissionCountrySerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = MissionCountrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def mission_city_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = MissionCity.objects.all()
        serializer = MissionCitySerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = MissionCitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def mission_team_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = MissionTeam.objects.all()
        serializer = MissionTeamSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = MissionTeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def mission_trip_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = MissionTrip.objects.all()
        serializer = MissionTripSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = MissionTripSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def user_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = User.objects.all()
        serializer = GETUserSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = POSTUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST'])
def enrollment_status_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = EnrollmentStatus.objects.all()
        serializer = EnrollmentStatusSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = EnrollmentStatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST'])
def single_enrollment_status_view(request, requestid, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    try:
        enrollment_status = EnrollmentStatus.objects.get(requestid=requestid)
    except EnrollmentStatus.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        print("GET A SPECIFIED EnrollmentStatus")
        serializer = EnrollmentStatusSerializer(enrollment_status)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING EnrollmentStatus")
        serializer = EnrollmentStatusSerializer(enrollment_status, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mesage': 'Enrollment status updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# gr added single user view
@api_view(['GET'])
def single_user_view(request, email, format=None):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        print("GET A SPECIFIED User")
        serializer = GETUserSerializer(user)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def login_attempt_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = LoginAttempt.objects.all()
        serializer = LoginAttemptSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = LoginAttemptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# gr added campaigns view
@api_view(['GET']) #TODO: POST method
def campaigns_view(request, format=None):
    """
    List all code snippets.
    """
    print("GET ALL THE Campaigns")
    if request.method == 'GET':
        all_campaigns = Campaign.objects.all()
        serializer = CampaignSerializer(all_campaigns, many=True)
        return Response(serializer.data)

# bjk added patient encounter view
@api_view(['GET', 'POST'])
def patient_encounter_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE PatientEncounters")
    if request.method == 'GET':
        all_patient_age_classification = PatientEncounter.objects.all()
        serializer = PatientEncounterSerializer(all_patient_age_classification, many=True)
        
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING PatientEncounter")
        serializer = PatientEncounterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # creates new MedicalCodes object for a new PatientEncounter object so it can be ready for coding
            m = MedicalCodes(patientEncounter_id = int(serializer.data['id']))
            m.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ar added get single patient encounter view
@api_view(['GET','PATCH'])
def single_patient_encounter_view(request, id, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    try:
        encounter = PatientEncounter.objects.get(id=id)
    except PatientEncounter.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        print("GET A SPECIFIED PatientEncounter")
        serializer = PatientEncounterSerializer(encounter)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        print("PATCH for updating PatientEncounter")
        serializer = PatientEncounterSerializer(encounter, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mesage': 'Patient encounter updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# iyowa added ICD patient encounter view
@api_view(['GET', 'POST'])
def ICD_patient_encounter_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE PatientEncounters")
    if request.method == 'GET':
        all_patient_age_classification = PatientEncounter.objects.all()
        serializer = ICDPatientEncounterSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)

# frog96 added ICD single patient encounter view
@api_view(['GET'])
def ICD_single_patient_encounter_view(request, id, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    try:
        encounter = PatientEncounter.objects.get(id=id)
    except PatientEncounter.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        print("GET A SPECIFIED PatientEncounter")
        serializer = ICDPatientEncounterSerializer(encounter)
        return Response(serializer.data)

@api_view(['GET'])
def uncoded_patient_encounter_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    #TODO: ensure priority of encounters with a single set of codes
    #TODO: lock encounter if it's actively being worked on to prevent overloading (>2 coders)
    try:
        #use the codes table to get a half coded id
        #NOTE: this might break based on how MedicalCodes is populated
        #This snippet assumes 'coder1_problem_code' won't be null
        uncoded_subquery = MedicalCodes.objects.filter(coder2_problem_code__isnull=True).values_list('id', flat=True)
        encounter = PatientEncounter.objects.filter(id__in=uncoded_subquery).first()

        if encounter == None:
            #TODO: use the codes table to get uncoded id
            uncoded_subquery = MedicalCodes.objects.values_list('patientEncounter_id', flat=True)
            encounter = PatientEncounter.objects.exclude(id__in=uncoded_subquery).first()

        if encounter == None:
            return Response(status=status.HTTP_404_NOT_FOUND)    

    except PatientEncounter.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        print("GET a PatientEncounter that isn't coded")
        serializer = PatientEncounterSerializer(encounter)
        return Response(serializer.data)

# nyan added medical codes view
@api_view(['GET', 'POST'])
def medical_codes_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        print("GET ALL THE Medical Codes")
        codes = MedicalCodes.objects.all()
        serializer = MedicalCodesSerializer(codes, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR ADDING Medical Codes")
        serializer = MedicalCodesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# potato added update patient encounter view
@api_view(['GET','PATCH'])
def patient_encounter_medical_codes_view(request, id, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    try:
        encounter_codes = MedicalCodes.objects.get(patientEncounter_id=id)
    except MedicalCodes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        print("GET Patient Encounter Codes")
        serializer = MedicalCodesSerializer(encounter_codes)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        print("PATCH FOR EDITING MedicalCodes from PatientEncounter")
        serializer = MedicalCodesSerializer(encounter_codes, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
            # return Response({'mesage': 'Patient encounter codes updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def patient_encounter_tab_fields_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = PatientEncounterTabFields.objects.all()
        serializer = PatientEncounterTabFieldsSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = PatientEncounterTabFieldsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def chief_complaint_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = ChiefComplaint.objects.all()
        serializer = ChiefComplaintSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = ChiefComplaintSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def tab_fields_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = TabFields.objects.all()
        serializer = TabFieldsSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = TabFieldsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def tab_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = Tab.objects.all()
        serializer = TabSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = TabSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def medication_inventory_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = MedicationInventory.objects.all()
        serializer = MedicationInventorySerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = MedicationInventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def inventory_form_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = InventoryForm.objects.all()
        serializer = InventoryFormSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = InventoryFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def inventory_category_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = InventoryCategory.objects.all()
        serializer = InventoryCategorySerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = InventoryCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def manufacturer_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = Manufacturer.objects.all()
        serializer = ManufacturerSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = ManufacturerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def medication_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = Medication.objects.all()
        serializer = MedicationSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = MedicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def concept_medication_forms_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = ConceptMedicationForms.objects.all()
        serializer = ConceptMedicationFormsSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = ConceptMedicationFormsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def medication_generic_strength_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = MedicationGenericStrength.objects.all()
        serializer = MedicationGenericStrengthSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = MedicationGenericStrengthSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def instance_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = Instance.objects.all()
        serializer = InstanceSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = InstanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET', 'POST'])
def database_change_log_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = DatabaseChangeLog.objects.all()
        serializer = DatabaseChangeLogSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = DatabaseChangeLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET', 'POST'])
def audit_entry_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = AuditEntry.objects.all()
        serializer = AuditEntrySerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = AuditEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET', 'POST'])
def inventory_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = Inventory.objects.all()
        serializer = InventorySerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET', 'POST'])
def units_setting_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = UnitsSetting.objects.all()
        serializer = UnitsSettingSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = UnitsSettingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET', 'POST'])
def message_of_the_day_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = MessageOfTheDay.objects.all()
        serializer = MessageOfTheDaySerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = MessageOfTheDaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['GET', 'POST'])
def contact_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = Contact.objects.all()
        serializer = ContactSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['GET', 'POST'])
def test_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = Test.objects.all()
        serializer = TestSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def csv_upload_document_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = CSVUploadDocument.objects.all()
        serializer = CSVUploadDocumentSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = CSVUploadDocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['GET', 'POST'])
def patient_encounter_photo_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = PatientEncounterPhoto.objects.all()
        serializer = PatientEncounterPhotoSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = PatientEncounterPhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def database_status_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = DatabaseStatus.objects.all()
        serializer = DatabaseStatusSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = DatabaseStatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET', 'POST'])
def feedback_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = Feedback.objects.all()
        serializer = FeedbackSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET', 'POST'])
def kit_update_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = KitUpdate.objects.all()
        serializer = KitUpdateSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = KitUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['GET', 'POST'])
def kit_status_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = KitStatus.objects.all()
        serializer = KitStatusSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = KitStatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
@api_view(['GET', 'POST'])
def internet_status_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = InternetStatus.objects.all()
        serializer = InternetStatusSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = InternetStatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def network_status_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = NetworkStatus.objects.all()
        serializer = NetworkStatusSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = NetworkStatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def system_setting_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = SystemSetting.objects.all()
        serializer = SystemSettingSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = SystemSettingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def identifier_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = Identifier.objects.all()
        serializer = IdentifierSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = IdentifierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def telecom_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = Telecom.objects.all()
        serializer = TelecomSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = TelecomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def communication_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = Communication.objects.all()
        serializer = CommunicationSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = CommunicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def general_practitioner_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = GeneralPractitioner.objects.all()
        serializer = GeneralPractitionerSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = GeneralPractitionerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def managing_organization_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = ManagingOrganization.objects.all()
        serializer = ManagingOrganizationSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = ManagingOrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def link_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = Link.objects.all()
        serializer = LinkSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = LinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def address_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    print("GET ALL THE Role")
    if request.method == 'GET':
        all_patient_age_classification = Address.objects.all()
        serializer = AddressSerializer(all_patient_age_classification, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR CREATING Role")
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def all_notifications_view(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """

    print("GET ALL THE NOTIFICATION")
    if request.method == 'GET':
        all_notifications = Notification.objects.all()
        serializer = NotificationSerialier(all_notifications, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("POST FOR A NOTIFICATION")
        serializer = NotificationSerialier(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def notification_for_one_user_view(request, user_id, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    try:
        # id from the param is user id
        notifications = Notification.objects.filter(user_id=user_id)
    except Notification.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    print("GET ALL THE NOTIFICATION FOR USER")
    if request.method == 'GET':
        serializer = NotificationSerialier(notifications, many=True)
        return Response(serializer.data)


@api_view(['DELETE'])
def notification_for_delete_view(request, id, format=None):
    """
    Remove a notifcation
    """
    try:
        # id from the param is user id
        notification = Notification.objects.get(id=id)
        print("notification = ", notification)
    except Notification.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    print("GET THE NOTIFICATION that will be deleted")
    if request.method == 'DELETE':
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def home_page_view(request):
    return JsonResponse("Welcome to fEMR Central!")