from django.urls import path
from .views import index, get_otp, verify_otp, save_patient_profile, check_slot_availability

app_name = 'patient'

urlpatterns = [
    path('', index, name='index'),
    path('get-otp/', get_otp, name='get-otp'),
    path('verify-otp/', verify_otp, name='verify-otp'),
    path('save-patient-profile/', save_patient_profile,
         name='save-patient-profile'),
    path('check-slot-availability/',
         check_slot_availability, name='check-slot-availability')
]
