from django.urls import path
from .views import home, add_doctor,add_time_slot

app_name = 'doctor'

urlpatterns = [
    path('', home, name='home'),
    path('add-doctor/', add_doctor, name='add-doctor'),
    path('add-time-slot/', add_time_slot, name='add-time-slot')
]
