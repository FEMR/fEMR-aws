from math import fabs
from pydoc import describe
from pyexpat import model
from re import T
from statistics import mode
from django.conf import settings
from django.db import models

from django.core.validators import (
    BaseValidator,
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.utils.deconstruct import deconstructible


birth_sex_choices = (("f", "Female"), ("m", "Male"), ("o", "Other"))
unit_choices = (("i", "Imperial"), ("m", "Metric"))

class State(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self) -> str:
        return str(self.name)

class fEMRUser(models.Model): # I hate you ChainGang.
     pass
class Deleted(models.Model):
    pass
class Campaign(models.Model):
    pass
class  Organization(models.Model):
    pass
class InventoryEntry(models.Model):
    pass
class Roles(models.Model):
    pass
class ConceptPrescriptionAdministration(models.Model):
    pass


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # pylint: disable=C0103
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
@deconstructible
class ModifiedMaxValueValidator(BaseValidator):
    #message = _("Ensure this value is less than %(limit_value)s.")
    code = "max_value"

    def compare(self, a, b):
        return a > b



class Patient(models.Model):

    legacy_id = models.IntegerField(unique=True,null=True)
    userid = models.IntegerField(null=True)
    first_name = models.CharField(max_length=30,null=True)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30,null=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    age = models.IntegerField(null=True)
    
    sex_assigned_at_birth = models.CharField(max_length=6, 
                                             choices=birth_sex_choices
                                            ,null=True)


    current_address = models.CharField(max_length=30, null=True, blank=True)
    address1 = models.CharField(
        "Address line 1", max_length=1024, null=True, blank=True
    )

    address2 = models.CharField(
        "Address line 2", max_length=1024, null=True, blank=True
    )
    city = models.CharField("City", max_length=1024, null=True, blank=True)
    photo = models.ForeignKey("Photo", on_delete=models.CASCADE, blank=True, null=True)
    patientencounter = models.ForeignKey("PatientEncounter", on_delete=models.CASCADE, null=True, related_name="patient_patient_encounter") 
    deleted = models.ForeignKey('Deleted', null=True, on_delete=models.CASCADE)
    social_security_number = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        blank=True,
        validators=[MinLengthValidator(4)],
    )
    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=12,
        null=True,
        blank=True,
        validators=[MinLengthValidator(5)],
    )
    city = models.CharField("City", max_length=1024, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)

    phone_number = models.CharField(max_length=13, null=True, blank=True)
    phone_number_type = models.CharField(max_length=30, null=True, blank=True)
    shared_phone_number = models.BooleanField(null=True)
    email_address = models.CharField(max_length=40, null=True, blank=True)
    shared_email_address = models.BooleanField(null=True)

    timestamp = models.DateTimeField(
        auto_now=True, editable=False, null=True, blank=False
    )

    campaign = models.ManyToManyField("MissionTrip", default=1, null=True)

class PatientEncounter(models.Model):

    """
    Individual data point in a patient's medical record.
    """
    legacy_id = models.IntegerField(unique=True,null=True)
    patient = models.ForeignKey(
        "Patient", on_delete=models.CASCADE, null=True, blank=True, related_name="patient_encounter_patient"
    )
    nurse = models.ForeignKey("User", on_delete=models.CASCADE, null= True,related_name="patient_encounter_nurse" )
    date_of_triage_visit = models.DateTimeField(null=True, blank=False)
    chief_complaints = models.ForeignKey("ChiefComplaint", on_delete=models.CASCADE, related_name="chief_complaint",null=True)
    date_of_medical_visit = models.TimeField(auto_now_add = True, null=True) #needs to be DateTime field
    date_of_pharmacy_visit = models.TimeField(auto_now_add= True, null = True) #needs to be DateTime field
    doctor = models.ForeignKey("User", on_delete=models.CASCADE, null=True, related_name="patient_encounter_doctor")
    pharmacist = models.ForeignKey("User",on_delete=models.CASCADE, null=True, related_name="patient_encounter_pharmacist")
    patient_age_classification = models.ForeignKey("PatientAgeClassification", on_delete=models.CASCADE, null=True)
    mission_trip_id = models.ForeignKey("MissionTrip", on_delete=models.CASCADE, null=True, related_name="patient_encounter_mission_trip_id")
    date_of_diabetes_screen = models.TimeField(auto_now_add =True, null=True) #needs to be DateTime field
    user_id_diabetes_screen = models.ForeignKey("User", on_delete=models.CASCADE, null=True)
    is_diabetes_screened = models.BooleanField(null=True)
    
    body_height_primary = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        validators=[MaxValueValidator(8), MinValueValidator(0)],
    )
    body_height_secondary = models.FloatField(
        null=True,
        blank=True,
        validators=[ModifiedMaxValueValidator(200), MinValueValidator(0)],
    )
    body_weight = models.FloatField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(500), MinValueValidator(0.25)],
    )
    bmi_percentile = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(1)], null=True, blank=True
    )
    weight_for_length_percentile = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(1)], null=True, blank=True
    )
    head_occipital_frontal_circumference_percentile = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(1)], null=True, blank=True
    )
    body_mass_index = models.FloatField(
        validators=[MaxValueValidator(500), MinValueValidator(0)], null=True, blank=True
    )
    weeks_pregnant = models.IntegerField(
        validators=[MaxValueValidator(45), MinValueValidator(0)], null=True, blank=True
    )

    smoking = models.BooleanField(default=False)
    history_of_diabetes = models.BooleanField(default=False)
    history_of_hypertension = models.BooleanField(default=False)
    history_of_high_cholesterol = models.BooleanField(default=False)
    alcohol = models.BooleanField(default=False)

    chief_complaint = models.ManyToManyField("ChiefComplaint", blank=True)
    patient_history = models.CharField(max_length=1000, null=True, blank=True)

    community_health_worker_notes = models.CharField(
        max_length=500, null=True, blank=True
    )

    procedure = models.CharField(max_length=1000, null=True, blank=True)
    pharmacy_notes = models.CharField(max_length=1000, null=True, blank=True)

    medical_history = models.CharField(max_length=1000, null=True, blank=True)
    social_history = models.CharField(max_length=1000, null=True, blank=True)
    current_medications = models.CharField(max_length=1000, null=True, blank=True)
    family_history = models.CharField(max_length=1000, null=True, blank=True)

    photos = models.ManyToManyField("Photo", blank=True)

    timestamp = models.DateTimeField(null=True, blank=False)

    active = models.BooleanField(default=True)

    campaign = models.ForeignKey(
        "MissionTrip",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=False,
        default=1,
    )

class PatientDiagnosis(models.Model):
    encounter = models.ForeignKey(
        "PatientEncounter", on_delete=models.CASCADE, null=True, blank=True
    )
    diagnosis = models.ManyToManyField("Diagnosis")

class Diagnosis(models.Model):
    text = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return str(self.text)

class HistoryOfPresentIllness(models.Model):
    chief_complaint = models.ForeignKey(
        "ChiefComplaint", on_delete=models.CASCADE
    )
    encounter = models.ForeignKey(
        "PatientEncounter", on_delete=models.CASCADE
    )

    onset = models.CharField(max_length=50, null=True, blank=True)
    provokes = models.CharField(max_length=50, null=True, blank=True)
    palliates = models.CharField(max_length=50, null=True, blank=True)
    quality = models.CharField(max_length=50, null=True, blank=True)
    radiation = models.CharField(max_length=50, null=True, blank=True)
    severity = models.CharField(max_length=50, null=True, blank=True)
    time_of_day = models.CharField(max_length=50, null=True, blank=True)
    narrative = models.CharField(max_length=4000, null=True, blank=True)
    physical_examination = models.CharField(max_length=4000, null=True, blank=True)

    tests_ordered = models.CharField(max_length=255, null=True, blank=True)

class Treatment(models.Model):
    medication = models.ManyToManyField("Medication", blank=True)
    administration_schedule = models.ForeignKey(
        "AdministrationSchedule", on_delete=models.CASCADE, null=True, blank=True
    )
    days = models.IntegerField()
    prescriber = models.ForeignKey(
        "fEMRUser", on_delete=models.CASCADE, null=True, blank=True
    )
    diagnosis = models.ForeignKey(
        "Diagnosis", on_delete=models.CASCADE, null=True, blank=True
    )
    encounter = models.ForeignKey(
        "PatientEncounter",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    timestamp = models.DateTimeField(
        auto_now=True, null=True, blank=True
    )

    def __str__(self):
        return str(self.medication)
class AdministrationSchedule(models.Model):
    text = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return str(self.text)

class ChiefComplaint(models.Model):
    legacy_id = models.IntegerField(unique=True,null=False)
    value = models.CharField(max_length=1024)
    patientEncounter = models.ForeignKey(
        "PatientEncounter",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    sortOrder = models.IntegerField()
    active = models.BooleanField()

class PatientAgeClassification(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=1024)
    isDeleted = models.BooleanField()
    sortOrder = models.IntegerField()

class Photo(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    description = models.CharField(max_length=3072)
    file_path = models.CharField(max_length=1024)
    insertTS = models.DateField(null=True)
    photo = models.BinaryField()
    photoFile = models.FileField(upload_to="photos/", blank=True, null=True)
    imaging_link = models.CharField(max_length=255, blank=True, null=True)

class PatientPrescriptions(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    patientEncounter = models.ForeignKey("PatientEncounter", on_delete=models.CASCADE, null=False)
    medication = models.ForeignKey("Medication", on_delete=models.CASCADE, null=False)
    conceptPrescriptionAdministration = models.ForeignKey("ConceptPrescriptionAdministration", on_delete=models.CASCADE, null=True)
    physician = models.ForeignKey("User", on_delete=models.CASCADE, null=False)
    amount = models.IntegerField(null=True)
    dateTaken = models.DateTimeField(null=False)
    specialInstructions = models.CharField(max_length=1024, null=True)
    isCounseled = models.BooleanField(null=False)
    dateDispensed = models.DateTimeField()
    patientPrescriptionReplacements = models.ManyToManyField("PatientPrescriptionReplacement", null=True) #made not null for testing

class PatientPrescriptionReplacement(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    originalPrescription = models.ForeignKey("PatientPrescriptions", on_delete=models.CASCADE, null=False,related_name="patient_prescription_replacement_original_prescription")
    replacementPrescription = models.ForeignKey("PatientPrescriptions", on_delete=models.CASCADE,null=False, related_name="patient_prescription_replacement_replacement_prescription")
    patientPrescriptionReplacementReason = models.ForeignKey("PatientPrescriptionReplacementReason", on_delete=models.CASCADE)

class PatientPrescriptionReplacementReason(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    name = models.CharField(max_length=30,null=False)
    description = models.CharField(max_length=1024)

class PatientEncounterVital(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    userId = models.CharField(max_length=30,null=False)
    patientEncounterId = models.IntegerField(null=False)
    vital = models.ForeignKey("Vital", on_delete=models.CASCADE, null=False)
    vitalValue = models.FloatField(null=False)
    dateTaken = models.CharField(max_length=30,null=False)
    encounter = models.ForeignKey("PatientEncounter", on_delete=models.CASCADE, null=True, blank=True
    )
    diastolic_blood_pressure = models.IntegerField(
        validators=[MaxValueValidator(200), MinValueValidator(1)], null=True, blank=True
    )
    systolic_blood_pressure = models.IntegerField(
        validators=[MaxValueValidator(200), MinValueValidator(1)], null=True, blank=True
    )
    mean_arterial_pressure = models.FloatField(
        validators=[MinValueValidator(1)], null=True, blank=True
    )
    heart_rate = models.IntegerField(
        validators=[MaxValueValidator(170), MinValueValidator(40)],
        null=True,
        blank=True,
    )
    respiratory_rate = models.IntegerField(
        validators=[MaxValueValidator(500), MinValueValidator(1)], null=True, blank=True
    )
    body_temperature = models.FloatField(
        validators=[MaxValueValidator(200), MinValueValidator(1)], null=True, blank=True
    )
    oxygen_concentration = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(70)],
        null=True,
        blank=True,
    )
    glucose_level = models.FloatField(
        validators=[MaxValueValidator(500), MinValueValidator(1)], null=True, blank=True
    )
    #time stamp should be same as date taken

class Vital(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    name = models.CharField(max_length=30,unique=True, null=False)
    data_type = models.CharField(max_length=30,null=True)
    unitOfMeasurement = models.CharField(max_length=30,null=True)
    deleted = models.BooleanField(null=False)

class Role(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    name = models.CharField(max_length=30,unique=True, null=False)


class User(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    firstName = models.CharField(max_length=30,null=False)
    lastName = models.CharField(max_length=30,null=False)
    email = models.CharField(max_length=30,unique=True, null=False)
    password = models.CharField(max_length=30, null=False)
    roles =  models.ManyToManyField("Role")
    lastLogin = models.DateTimeField(null=False)
    deleted = models.BooleanField(null=False)
    passwordReset = models.BooleanField(null=False)
    notes = models.CharField(max_length=1024)
    passwordCreatedDate = models.DateTimeField(null=False)
    dateCreated = models.DateTimeField(null=False)
    createdBy = models.IntegerField(unique=True, null=False)
    missionTrips =  models.ManyToManyField("MissionTrip", related_name="user_mission_trips",blank=True)


class EnrollmentStatus(models.Model):
    requestid = models.IntegerField(unique=True, null=False, primary_key=True)
    role = models.IntegerField(unique=False,null=False)
    enrollmentstatus = models.CharField(max_length=30,null=False)
    firstName = models.CharField(max_length=30,null=False)
    lastName = models.CharField(max_length=30,null=False)
    email = models.CharField(max_length=30,unique=True, null=False)
    phone = models.CharField(max_length=30,null=False, default="000-000-0000")
    organization = models.CharField(max_length=64,null=False)
    message = models.CharField(max_length=1024,null=False)
    dateCreated = models.DateTimeField(null=False)
   
class LoginAttempt(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    user = models.ForeignKey("User", on_delete=models.CASCADE, unique=False, null=True)
    ip_address = models.BinaryField(unique=False, null=True)
    loginDate = models.DateTimeField(unique=False, null=True)
    isSuccessful = models.BooleanField(null=False)
    usernameAttempt = models.CharField(max_length=1024,null=False)

class PatientEncounterTabFields(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    userId = models.IntegerField(null = False)
    user = models.ForeignKey("User", on_delete=models.CASCADE, null = False)
    patientEncounterId = models.ForeignKey("PatientEncounter", on_delete=models.CASCADE, null=False, unique=False)
    tabField = models.ForeignKey("TabFields", on_delete=models.CASCADE, null=False)
    tabFieldValue = models.CharField(max_length=1024,null=False)
    dateTaken = models.DateTimeField(null=False)
    chiefComplaint = models.ForeignKey("ChiefComplaint", on_delete=models.CASCADE, null=True)
    isDeleted = models.DateTimeField(null=True)
    deletedByUserId = models.IntegerField(null=True)

class TabFields(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    name = models.CharField(max_length=30,unique=True, null=False)
    isDeleted = models.BooleanField(null=False)
    tab = models.ForeignKey("Tab", on_delete=models.CASCADE, null=True)
    tabFieldType = models.ForeignKey("TabFieldType", on_delete=models.CASCADE, null=False)
    tabFieldSize = models.ForeignKey("TabFieldSize", on_delete=models.CASCADE, null=False)
    order = models.IntegerField(unique=False, null=True)
    placeholder = models.CharField(max_length=30,unique=False, null=True)

class TabFieldSize(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    name = models.CharField(max_length=30,unique=True, null=False)

class TabFieldType(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    name = models.CharField(max_length=30,unique=True, null=False)

class Tab(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    name = models.CharField(max_length=30,null=False)
    userId = models.IntegerField(null=False)
    dateCreated = models.DateTimeField(null=False)
    isDeleted = models.BooleanField(null=False)
    leftColumnSize = models.IntegerField(null=False)
    rightColumnSize = models.IntegerField(null=False)
    isCustom = models.BooleanField(null=False)
    tabFields =  models.ManyToManyField("TabFields",related_name="tab_tab_fields",blank=True)

class MedicationInventory(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    quantityCurrent = models.IntegerField(unique=False, null=False)
    quantityInitial = models.IntegerField(unique=False, null=False)
    medication = models.ForeignKey("Medication", on_delete=models.CASCADE,related_name="medication_inventory_medication")
    missionTrip = models.ForeignKey("MissionTrip", on_delete=models.CASCADE)
    isDeleted = models.DateTimeField(null = True)
    timeAdded = models.DateTimeField()
    createdBy = models.IntegerField()
    category = models.ForeignKey(
        "InventoryCategory", on_delete=models.CASCADE, null=True, blank=True
    )
    form = models.ForeignKey("InventoryForm", on_delete=models.CASCADE)
    strength = models.CharField(max_length=25, null=True, blank=True)
    count = models.PositiveIntegerField(default=0)
    item_number = models.CharField(max_length=25, null=True, blank=True)
    box_number = models.CharField(max_length=25, null=True, blank=True)
    expiration_date = models.DateField(blank=True, null=True)
    manufacturer = models.ForeignKey(
        "Manufacturer", on_delete=models.CASCADE, null=True, blank=True
    )

class InventoryForm(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.name)


class InventoryCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.name)


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.name)

class Medication(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    name = models.CharField(max_length=30,unique=False, null=True)
    text = models.CharField(max_length=1024, null=True, blank=True)
    isDeleted = models.BooleanField(null=False)
    conceptMedicationForm = models.ForeignKey("ConceptMedicationForms", on_delete=models.CASCADE, null=True) #made not null for testing
    medicationGenericStrengths =  models.ManyToManyField("MedicationGenericStrength", null=True) #made not null for testing
    medicationInventory = models.ForeignKey("MedicationInventory", on_delete=models.CASCADE, related_name="medication_medication_inventory", null=True) #made not null for testing

class ConceptMedicationForms(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    name = models.CharField(max_length=30, unique=True, null=False)
    description = models.CharField(max_length=1024)
    isDeleted = models.BooleanField()


class MedicationGenericStrength(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    conceptMedicationUnit = models.ForeignKey("ConceptMedicationUnit", on_delete=models.CASCADE)
    medicationGeneric = models.ForeignKey("MedicationGenerics", on_delete=models.CASCADE)
    isDenominator = models.BooleanField(null=False)
    value = models.FloatField(unique=True, null=False)

class MedicationGenerics(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    name = models.CharField(max_length=1024,unique=True, null=False)

class ConceptMedicationUnit(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    name = models.CharField(max_length=30,unique=True, null=False)
    description = models.CharField(max_length=1024)
    isDeleted = models.BooleanField()


class MissionCountry(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    name = models.CharField(max_length=30,unique=True, null=False)

class MissionCity(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    name = models.CharField(max_length=30,unique=True, null=False)
    mission_country = models.ForeignKey(MissionCountry,on_delete=models.CASCADE, null=False)

class MissionTeam(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    name = models.CharField(max_length=30,unique=True, null=False)
    location = models.CharField(max_length=30,unique=True, null=False)
    description = models.CharField(max_length=1024,unique=True, null=False)
    mission_trips = models.ForeignKey("MissionTrip",on_delete=models.CASCADE,null=True)
    active = models.BooleanField()
    contract_start_date = models.DateField()
    address1 = models.CharField(max_length=1024, null=True, blank=True)
    address2 = models.CharField(max_length=1024, null=True, blank=True)
    zip_coden_ned_dafult_text_filed = models.CharField(max_length=1024)
 
class MissionTrip(models.Model):
    legacy_id = models.IntegerField(unique=True, null=False)
    mission_team = models.ForeignKey(MissionTeam,on_delete=models.CASCADE, unique=True, null=False)
    mission_city = models.ForeignKey(MissionCity,on_delete=models.CASCADE, null=False)
    state_date = models.DateField()
    end_date = models.DateField()
    user = models.ManyToManyField(User, blank=True)

def get_test_org():
    return Organization.objects.get_or_create(name="Test")[0].id

class Instance(models.Model):
    name = models.CharField(max_length=30, unique=True)
    active = models.BooleanField(default=True)
    main_contact = models.ForeignKey(
        "fEMRUser",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="instance_main_contact",
    )
    admins = models.ManyToManyField("fEMRUser", related_name="instance_admins")
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, default=get_test_org,null= True
    )
    contract_start_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Operation"

class DatabaseChangeLog(models.Model):
    action = models.CharField(max_length=64)
    model = models.CharField(max_length=64)
    instance = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    username = models.CharField(max_length=256, null=True)
    timestamp = models.DateTimeField(auto_now=True)
    campaign = models.ForeignKey(MissionTrip, on_delete=models.CASCADE)

    def __str__(self):
        # pylint: disable=C0301
        return f"{self.action} {self.model} {self.instance} - by {self.ip} at {self.username}, {self.timestamp}"


class AuditEntry(models.Model):
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    username = models.CharField(max_length=256, null=True)
    timestamp = models.DateTimeField(auto_now=True)
    campaign = models.ForeignKey(
        MissionTrip, on_delete=models.CASCADE, blank=True, null=True
    )
    browser_user_agent = models.CharField(max_length=256, null=True)

    def __str__(self):
        return f"{self.action} - {self.username} - {self.ip} - {self.timestamp} - {self.campaign}"

class Inventory(models.Model):
    entries = models.ManyToManyField(InventoryEntry)


class UnitsSetting(SingletonModel):
    units = models.CharField(max_length=30, choices=unit_choices, default="i")


class MessageOfTheDay(SingletonModel):
    text = models.CharField(max_length=2048)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

class Contact(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email_address = models.CharField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Test(models.Model):
    text = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return str(self.text)


class CSVUploadDocument(models.Model):
    document = models.FileField(upload_to="csv/")
    mode_option = models.CharField(
        max_length=10,
        choices=(
            ("1", "New"),
            ("2", "Update"),
        ),
    )

# class UserSession(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         related_name="logged_in_user",
#         on_delete=models.CASCADE,
#     )
#     session_key = models.CharField(max_length=32, null=True, blank=True)
#     timestamp = models.DateTimeField(
#         auto_now=True, editable=False, null=False, blank=False
#     )


# class Photo(models.Model):
#     description = models.CharField(max_length=100)
#     photo = models.FileField(upload_to="photos/", blank=True, null=True)
#     imaging_link = models.CharField(max_length=255, blank=True, null=True)

#     def __str__(self) -> str:
#         return str(self.description)


class PatientEncounterPhoto(models.Model):
    photo_id = models.IntegerField(null=False)
    patient_encounter =models.IntegerField(null=False)

class DatabaseStatus(models.Model):
    legacy_id = models.IntegerField(unique=True,null=False)
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=30)

class Feedback(models.Model):
    legacy_id = models.IntegerField(unique=True,null=False)
    date = models.DateField(null=False)
    feedback = models.CharField(max_length=1024,null=False)

class KitUpdate(models.Model):
    legacy_id = models.IntegerField(unique=True,null=False)
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=30)    

class KitStatus(models.Model):
    legacy_id = models.IntegerField(unique=True,null=False)
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=30)   

class InternetStatus(models.Model):
    legacy_id = models.IntegerField(unique=True,null=False)
    status = models.BooleanField(unique=False, null=False)
    
class NetworkStatus(models.Model):
    legacy_id = models.IntegerField(unique=True,null=False)
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=30) 

class SystemSetting(models.Model):
    legacy_id = models.IntegerField(unique=True,null=False)
    name = models.CharField(max_length=30)
    is_active = models.BooleanField()
    description = models.CharField(max_length=1024)

class Identifier(models.Model):
    identifier_id = models.IntegerField(unique=True,null=True)
    campaign_key = models.CharField(max_length=30)

class Telecom(models.Model):
    data = models.CharField(max_length=1024)

class Communication(models.Model):
    data = models.CharField(max_length=1024)

class GeneralPractitioner(models.Model):
    data = models.CharField(max_length=1024)

class ManagingOrganization(models.Model):
    data = models.CharField(max_length=1024)

class Link(models.Model):
    data = models.CharField(max_length=1024)

class Address(models.Model):
    current_address = models.CharField(max_length=1024)
    address1 = models.CharField(max_length=1024)
    address2 = models.CharField(max_length=1024)
    zip_code = models.CharField(max_length=1024)
    city = models.CharField(max_length=1024)
    state = models.CharField(max_length=1024)
    previous_address = models.CharField(max_length=1024)

class HL7FHIR(models.Model):
    resource_type = models.CharField(max_length=1024)
    identifier = models.ForeignKey(Identifier, on_delete=models.CASCADE, blank=True, null=True)
    active = models.BooleanField()
    name = models.CharField(max_length=1024)
    telecom = models.ManyToManyField(Telecom)
    gender = models.CharField(max_length=30)
    birthDate = models.CharField(max_length=64)
    deceasedBoolean = models.BooleanField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    maritalStatus = models.BooleanField()
    multipleBirthBoolean = models.BooleanField()
    photo = models.ManyToManyField(Photo)
    contact = models.ManyToManyField(Contact)
    communication = models.ManyToManyField(Communication)
    generalPractitioner = models.ManyToManyField(GeneralPractitioner)
    managingOrganization = models.ManyToManyField(ManagingOrganization)
    link = models.ManyToManyField(Link)

class MedicalCodes(models.Model):
    patientEncounter = models.ForeignKey("PatientEncounter", on_delete=models.CASCADE, null=False, unique=True, related_name="codes_encounter")

    coder1_user = models.ForeignKey("User", on_delete=models.CASCADE, null= True,related_name="codes_coder1" )
    coder1_office_visit_code = models.JSONField(null=True, blank=True)
    coder1_problem_code = models.JSONField(null=True, blank=True)
    coder1_chief_complaint_code = models.JSONField(null=True, blank=True)
    coder1_covid19_code = models.JSONField(null=True, blank=True)
    coder1_submission_date = models.DateTimeField(null=True, blank=False)

    coder2_user = models.ForeignKey("User", on_delete=models.CASCADE, null= True,related_name="codes_coder2" )
    coder2_office_visit_code = models.JSONField(null=True, blank=True)
    coder2_problem_code = models.JSONField(null=True, blank=True)
    coder2_chief_complaint_code = models.JSONField(null=True, blank=True)
    coder2_covid19_code = models.JSONField(null=True, blank=True)
    coder2_submission_date = models.DateTimeField(null=True, blank=False)

    arbiter_user = models.ForeignKey("User", on_delete=models.CASCADE, null= True,related_name="codes_arbiter" )
    arbiter_office_visit_code = models.JSONField(null=True, blank=True)
    arbiter_problem_code = models.JSONField(null=True, blank=True)
    arbiter_chief_complaint_code = models.JSONField(null=True, blank=True)
    arbiter_covid19_code = models.JSONField(null=True, blank=True)
    arbiter_submission_date = models.DateTimeField(null=True, blank=False)

class Notification(models.Model):
    user_id =  models.ForeignKey("User", on_delete=models.CASCADE, null= True,related_name="user" )
    type = models.CharField(max_length=1024, null= True)
    message = models.TextField(null= True)
    date = models.DateField(null=True)