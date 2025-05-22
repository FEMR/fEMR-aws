from django.contrib import admin
from .models import HL7FHIR, Patient, Diagnosis, AdministrationSchedule, PatientAgeClassification, PatientEncounter

admin.site.register({Patient})
admin.site.register({HL7FHIR})
admin.site.register({Diagnosis})
admin.site.register({AdministrationSchedule})
admin.site.register({PatientAgeClassification})
admin.site.register({PatientEncounter})
# Register your models here.
