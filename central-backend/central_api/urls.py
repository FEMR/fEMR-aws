from django.urls import path
from .views import Patient as PatientView
from .views import HL7FHIR as HL7FHIRView
from django.urls import path, re_path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers
from rest_framework.authtoken import views as rest_framework_views
from central_api import views
from .api_views import (
    PatientViewSet,
    HL7FHIRViewSet
)

app_name = "central_api"

schema_view = get_schema_view(
    openapi.Info(
        title="ChainGang API",
        default_version='v1',
        description="ChaingGang RESTful API for connecting OnChain and Legacy Deployments",
        terms_of_service="https://chain-gang.gitbook.io/untitled/privacy-policy",
        contact=openapi.Contact(email="chaingang.capstone@gmail.com"),
        license=openapi.License(name="https://chain-gang.gitbook.io/untitled/licensing"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r"Patient", PatientViewSet)
router.register(r"Hl7fhir", HL7FHIRViewSet)


urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),

    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    re_path(r'^patient/', PatientView.as_view()),
    path('^hl7fhir/<int:patientId>', HL7FHIRView.as_view()),
    path('diagnosis/', views.diagnosis_view),
    path('administration-schedule/', views.administration_schedule_view),
    path('patient-age-classification/', views.patient_age_classification_view),
    path('treatment/', views.treatment_view),
    path('photo/', views.photo_view),
    path('patient-prescription-replacement-reason/', views.patient_prescription_replacement_reason_view),
    path('vital/', views.vital_view),
    path('role/',views.role_view),
    path('tab-field-size/',views.tab_field_size_view),
    path('tab-field-type/',views.tab_field_type_view),
    path('inventory-form/',views.inventory_form_view),
    path('inventory-category/',views.inventory_category_view),
    path('manufacturer/',views.manufacturer_view),
    path('concept-medication-forms/',views.manufacturer_view),
    path('medication-generics/',views.medication_generics_view),
    path('concept-medication-unit/',views.concept_medication_unit_view),
    path('mission-country/',views.mission_country_view),
    path('mission-city/',views.mission_city_view),
    path('mission-team/',views.mission_team_view),
    path('mission-trip/',views.mission_trip_view),
    path('user/',views.user_view),
    path('enrollment-status/',views.enrollment_status_view),
    path('enrollment-status/<int:requestid>/',views.single_enrollment_status_view),
    path('login-attempt/',views.login_attempt_view),
    # bjk added patient encounter
    path('patient-encounter/',views.patient_encounter_view),
    path('patient-encounter-tab-fields/',views.patient_encounter_tab_fields_view),
    path('chief-complaint/',views.chief_complaint_view),
    path('patient-diagnosis/', views.patient_diagnosis_view),
    path('tab-fields/',views.tab_fields_view),
    path('tab/',views.tab_view),
    path('patient-prescriptions/',views.patient_prescriptions_view),
    path('medication-inventory/',views.medication_inventory_view),
    path('inventory-form/',views.inventory_form_view),
    path('inventory-category/',views.inventory_category_view),
    path('manufacturer/',views.manufacturer_view),
    path('medication/',views.medication_view),
    path('concept-medication-forms/',views.concept_medication_forms_view),
    path('medication-generic-strength/',views.medication_generic_strength_view),
    path('medication-generics/',views.medication_generics_view),
    path('instance/',views.instance_view),
    path('database-change-log/',views.database_change_log_view),
    path('audit-entry/',views.audit_entry_view),
    path('inventory/',views.inventory_view),
    path('unit-setting/',views.units_setting_view),
    path('message-of-the-day/',views.message_of_the_day_view),
    path('contact/',views.contact_view),
    path('test/',views.test_view),
    path('csv-upload-document/',views.csv_upload_document_view),
    path('patient-encounter-photo/',views.patient_encounter_photo_view),
    path('database-status/',views.database_status_view),
    path('feedback/',views.feedback_view),
    path('kit-update/',views.kit_update_view),
    path('kit-status/',views.kit_status_view),
    path('internet-status/',views.internet_status_view),
    path('network-status/',views.network_status_view),
    path('identifier/',views.identifier_view),
    path('telecom/',views.telecom_view),
    path('communication/',views.communication_view),
    path('managing-organization',views.managing_organization_view),
    path('link/',views.link_view),    
    path('address/',views.address_view),
    path('campaigns/', views.campaigns_view),
    path('medical-codes/', views.medical_codes_view),
    path('medical-codes/<int:id>/', views.patient_encounter_medical_codes_view),
    path('patient-encounter/<int:id>/',views.single_patient_encounter_view),
    path('uncoded-patient-encounter/',views.uncoded_patient_encounter_view),
    path('notifcations/', views.all_notifications_view),
    path('notifcations/<int:user_id>/', views.notification_for_one_user_view),
    path('user/<str:email>/', views.single_user_view),
    path('test_encounter/', views.ICD_patient_encounter_view),
    path('test_encounter/<int:id>/', views.ICD_single_patient_encounter_view),
    path('patient_encounter_vital/', views.patient_encounter_vital_view),
    path('history_of_present_illness/', views.history_of_present_illness_view),
    path('notifcation/<int:id>/', views.notification_for_delete_view)

]