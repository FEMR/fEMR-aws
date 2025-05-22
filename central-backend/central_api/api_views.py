from rest_framework import permissions
from rest_framework import viewsets

from .models import (
    fEMRUser,
    Patient,
    PatientEncounter,
    MessageOfTheDay,
    Campaign,
    Instance,
    State,
    Organization,
    ChiefComplaint,
    AdministrationSchedule,
    Diagnosis,
    Medication,
    Test,
    Photo,
    HistoryOfPresentIllness,
    PatientDiagnosis,
    Treatment,
    InventoryForm,
    InventoryCategory,
    Manufacturer,
    InventoryEntry,
    Inventory,
    UnitsSetting,
    HL7FHIR,
)

from .serializers import (
    POSTUserSerializer,
    GETUserSerializer,
    GroupSerializer,
    PatientSerializer,
    PatientEncounterSerializer,
    MessageOfTheDaySerializer,
    CampaignSerializer,
    InstanceSerializer,
    StateSerializer,
    OrganizationSerializer,
    ChiefComplaintSerializer,
    AdministrationScheduleSerializer,
    DiagnosisSerializer,
    MedicationSerializer,
    TestSerializer,
    PhotoSerializer,
    HistoryOfPresentIllnessSerializer,
    PatientDiagnosisSerializer,
    TreatmentSerializer,
    InventoryFormSerializer,
    InventoryCategorySerializer,
    ManufacturerSerializer,
    InventoryEntrySerializer,
    InventorySerializer,
    UnitsSettingSerializer,
    HL7FHIRSerializer,
    PatientAgeClassificationSerializer,
)

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    #permission_classes = [permissions.IsAuthenticated, IsAPIAllowed]

class HL7FHIRViewSet(viewsets.ModelViewSet):
    queryset = HL7FHIR.objects.all()
    serializer_class = HL7FHIRSerializer

class DiagnosisViewSet(viewsets.ModelViewSet):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer

class AdministrationScheduleViewSet(viewsets.ModelViewSet):
    queryset = Diagnosis.objects.all()
    serializer_class = AdministrationScheduleSerializer

class PatientAgeClassificationViewSet(viewsets.ModelViewSet):
    queryset = Diagnosis.objects.all()
    serializer_class = PatientAgeClassificationSerializer

# add patient encounter
class PatientEncounterViewSet(viewsets.ModelViewSet):
    queryset = PatientEncounter.objects.all()
    serializer_class = PatientEncounterSerializer

class ChiefComplaintViewSet(viewsets.ModelViewSet):
    queryset = ChiefComplaint.objects.all()
    serializer_class = ChiefComplaintSerializer