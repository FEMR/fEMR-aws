"""
Serializer objects defining what fields of each model should be exposed to the API.
"""
from django.contrib.auth.models import Group
from rest_framework import serializers
from itertools import chain
from django.db.models import F,Q
from .models import *



class POSTUserSerializer(serializers.ModelSerializer):
    """
    Serializes the `fEMRUser` model for API consumption.
    """

    class Meta:
        """
        Serializer meta class.
        """

        model = User
        fields = "__all__"


class EnrollmentStatusSerializer(serializers.ModelSerializer):
    """
    Serializes the `EnrollmentStatus` model for API consumption.
    """
    class Meta:
        """
        Serializer meta class.
        """

        model = EnrollmentStatus
        fields = "__all__"


class GETUserSerializer(serializers.ModelSerializer):
    """
    Serializes the `fEMRUser` model for API consumption.
    """
    class Meta:
        """
        Serializer meta class.
        """

        model = User
        fields = ['id','firstName','lastName','email', 'password', 'roles','missionTrips','dateCreated','notes','deleted']
        depth = 2


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializes the `django.contrib.auth.models.Group` model for API consumption.
    """

    class Meta:
        """
        Serializer meta class.
        """

        model = Group
        fields = "__all__"


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializes the `Patient` model for API consumption.
    """

    class Meta:
        """
        Serializer meta class.
        """

        model = Patient
        fields = "__all__"


class PatientEncounterSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = PatientEncounter
        fields = "__all__"

# Once the models have been made more concrete this wont be necessary since firstName and lastName will become not null later.
def CoderNameVerify(medicalCodes):
        if (medicalCodes is None):
            return "no medical codes"
        elif (medicalCodes['firstName'] is None) or (medicalCodes['lastName'] is None):
            if (medicalCodes['firstName'] is None):
                return medicalCodes['lastName']
            else:
                return medicalCodes['firstName']
        else:
            return medicalCodes['firstName'] + " " + medicalCodes['lastName']

class ICDPatientEncounterSerializer(serializers.ModelSerializer):

    Coder_1=serializers.SerializerMethodField()

    Coder_2=serializers.SerializerMethodField()
    
    chief_complaint=serializers.SerializerMethodField(method_name='get_complaints')

    diagnosis=serializers.SerializerMethodField()

    codes_=serializers.SerializerMethodField(method_name='get_codes')

    gender=serializers.SerializerMethodField()

    height=serializers.FloatField(source='body_height_secondary') # renamed field

    weight=serializers.FloatField(source='body_weight') # renamed field

    alcohol_use=serializers.BooleanField(source='alcohol') # renamed field

    patient_vitals=serializers.SerializerMethodField('get_vitals')

    assessments=serializers.SerializerMethodField()
    
    physical_examinations=serializers.SerializerMethodField()

    problems=serializers.SerializerMethodField()

    narratives=serializers.SerializerMethodField()

    dispense_medications=serializers.SerializerMethodField()

    age=serializers.SerializerMethodField()

    def get_Coder_1(self, obj):
        medicalCodes = MedicalCodes.objects.filter(patientEncounter_id = obj.id).values(
            firstName = F('coder1_user__firstName'),
            lastName = F('coder1_user__lastName')
        ).first()
        return CoderNameVerify(medicalCodes)
    
    def get_Coder_2(self, obj):
        medicalCodes = MedicalCodes.objects.filter(patientEncounter_id = obj.id).values(
            firstName = F('coder2_user__firstName'),
            lastName = F('coder2_user__lastName')
        ).first()
        return CoderNameVerify(medicalCodes)
    
    def get_complaints(self, obj):
        complaints=[]
        for pid in obj.chief_complaint.all():
            complaint = ChiefComplaint.objects.filter(id = pid.id).values_list('value', flat=True)[0]
            complaints.append(complaint)
        return complaints
    
    def get_codes(self, obj):
        medicalCodesHistory=[]
        encounters = PatientEncounter.objects.filter(patient_id = obj.patient_id).values()
        for encounter in encounters:
            try:
                codes = MedicalCodes.objects.filter(patientEncounter_id = encounter['id']).values(
                    # currently returning everything needs null check for arbiter submission date + codes
                    'arbiter_office_visit_code',
                    'arbiter_problem_code',
                    'arbiter_chief_complaint_code',
                    'arbiter_covid19_code',
                    'arbiter_submission_date'
                )[0]
                if(codes['arbiter_submission_date']  != None) :
                    medicalCodesHistory.append(codes)
                    # print(encounter['id'])
                    # print(obj.id)

                
            except IndexError:
                pass
        return medicalCodesHistory
    
    def get_vitals(self, obj):
        vitals = PatientEncounterVital.objects.filter(encounter_id = obj.id).values(
            'diastolic_blood_pressure',
            'systolic_blood_pressure',
            'heart_rate',
            'glucose_level',
            'oxygen_concentration',
            'respiratory_rate',
            'mean_arterial_pressure').first()
        return vitals

    def get_problems(self, obj):
        problems = PatientEncounterTabFields.objects.filter(patientEncounterId_id = obj.id).filter(tabField__name = 'problem').values(problem=F('tabFieldValue'))
        return problems
    
    def get_assessments(self, obj):
        problems = PatientEncounterTabFields.objects.filter(patientEncounterId_id = obj.id).filter(tabField__name = 'assessment').values(assessment=F('tabFieldValue'))
        return problems
    
    def get_narratives(self, obj):
        narrativesOnchain = HistoryOfPresentIllness.objects.filter(encounter_id = obj.id).values('narrative')
        narrativesLeagacy = PatientEncounterTabFields.objects.filter(patientEncounterId_id = obj.id).filter(tabField__name = 'narrative').values(narrative=F('tabFieldValue'))
        return chain(narrativesLeagacy,narrativesOnchain)
    
    def get_physical_examinations(self, obj):
        physicalExaminationOnchain = HistoryOfPresentIllness.objects.filter(encounter_id = obj.id).values('physical_examination')
        physicalExaminationLegacy = PatientEncounterTabFields.objects.filter(patientEncounterId_id = obj.id).filter(tabField__name = 'physicalExamination').values(physical_examination=F('tabFieldValue'))
        return chain(physicalExaminationOnchain,physicalExaminationLegacy)
    
    def get_diagnosis(self, obj):
        patdiag = PatientDiagnosis.objects.filter(encounter_id = obj.id).values_list('diagnosis__text')
        return [diagnosis[0] for diagnosis in patdiag]
    
    def get_dispense_medications(self, obj):
        meds = Treatment.objects.filter(encounter_id = obj.id).values_list('medication__name')
        return [medication[0] for medication in meds]
    
    def get_gender(self, obj):
        gender = Patient.objects.filter(id = obj.patient_id).values_list('sex_assigned_at_birth')[0][0]
        if(gender == 'f'):
            return 'Female'
        elif(gender == 'm'):
            return 'Male'
        # values_list() returns lists of single values for fields not in PatientEncounter

    def get_age(self, obj):
        return Patient.objects.filter(id = obj.patient_id).values_list('age')[0][0]
        # values_list() returns lists of single values for fields not in PatientEncounter

    class Meta:
        """
        Serializer meta class.
        """

        model = PatientEncounter
        fields = [
            'id',
            'patient',
            'Coder_1',
            'Coder_2',
            'chief_complaint',
            'diagnosis',
            'codes_',
            'age',
            'date_of_triage_visit',
            'gender',
            'height',
            'weight',
            'weeks_pregnant',
            'alcohol_use',
            'history_of_diabetes',
            'family_history',
            'patient_vitals',
            'assessments',
            'physical_examinations',
            'problems',
            'narratives',
            'current_medications',
            'dispense_medications'
        ]


class MedicalCodesSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = MedicalCodes
        fields = "__all__"

class InstanceSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = Instance
        fields = "__all__"


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = Campaign
        fields = "__all__"



class StateSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = State
        fields = "__all__"



class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = Organization
        fields = "__all__"


class ChiefComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = ChiefComplaint
        fields = "__all__"


class AdministrationScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = AdministrationSchedule
        fields = "__all__"


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = Diagnosis
        fields = "__all__"


class PatientPrescriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = PatientPrescriptions
        fields = "__all__"

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = Medication
        fields = "__all__"


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = Test
        fields = "__all__"


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = Photo
        fields = "__all__"


class HistoryOfPresentIllnessSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = HistoryOfPresentIllness
        fields = "__all__"



class PatientDiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = PatientDiagnosis
        fields = "__all__"


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = Treatment
        fields = "__all__"


class InventoryFormSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = InventoryForm
        fields = "__all__"


class InventoryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = InventoryCategory
        fields = "__all__"


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = Manufacturer
        fields = "__all__"


class InventoryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = InventoryEntry
        fields = "__all__"


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = Inventory
        fields = "__all__"


class UnitsSettingSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = UnitsSetting
        fields = "__all__"


class MessageOfTheDaySerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = MessageOfTheDay
        fields = "__all__"



class PatientAgeClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = PatientAgeClassification
        fields = "__all__"

class PatientPrescriptionReplacementReasonSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = PatientPrescriptionReplacementReason
        fields = "__all__"


class VitalSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = Vital
        fields = "__all__"


class PatientEncounterVitalSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = PatientEncounterVital
        fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = Role
        fields = "__all__"

class TabFieldSizeSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = TabFieldSize
        fields = "__all__"

class TabFieldTypeSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = TabFieldType
        fields = "__all__"

class TabSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = Tab
        fields = "__all__"


class ConceptMedicationFormsSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = ConceptMedicationForms
        fields = "__all__"


class MedicationGenericsSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = MedicationGenerics
        fields = "__all__"



class ConceptMedicationUnitSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = ConceptMedicationUnit
        fields = "__all__"

class MissionCountrySerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = MissionCountry
        fields = "__all__"

class MissionCitySerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = MissionCity
        fields = "__all__"


class MissionTeamSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = MissionTeam
        fields = "__all__"


class MissionTripSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = MissionTrip
        fields = "__all__"


class HL7FHIRSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = HL7FHIR
        fields = "__all__"


class LoginAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = LoginAttempt
        fields = "__all__"

class PatientEncounterTabFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = PatientEncounterTabFields
        fields = "__all__"


class TabFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = TabFields
        fields = "__all__"

class MedicationInventorySerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = MedicationInventory
        fields = "__all__"


class MedicationGenericStrengthSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = MedicationGenericStrength

        fields = "__all__"

class DatabaseChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = DatabaseChangeLog

        fields = "__all__"

class AuditEntrySerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = AuditEntry

        fields = "__all__"

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = Contact

        fields = "__all__"

class CSVUploadDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = CSVUploadDocument

        fields = "__all__"


class PatientEncounterPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = PatientEncounterPhoto

        fields = "__all__"

        

class DatabaseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = DatabaseStatus

        fields = "__all__"

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = Feedback

        fields = "__all__"
        
class KitUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = KitUpdate

        fields = "__all__"

class KitStatusSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = KitStatus

        fields = "__all__"

        
class InternetStatusSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = InternetStatus

        fields = "__all__"

        
class NetworkStatusSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = NetworkStatus

        fields = "__all__"


        
class SystemSettingSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = SystemSetting

        fields = "__all__"

        
class IdentifierSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = Identifier

        fields = "__all__"

        
class TelecomSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = Telecom

        fields = "__all__"


        
class CommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = Communication

        fields = "__all__"


        
class GeneralPractitionerSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = GeneralPractitioner

        fields = "__all__"


        
class ManagingOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = ManagingOrganization

        fields = "__all__"
        
class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = Link

        fields = "__all__"



class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = Address

        fields = "__all__"


class NotificationSerialier(serializers.ModelSerializer):
    class Meta:
        """
        Serializer meta class.
        """

        model = Notification

        fields = "__all__"

       