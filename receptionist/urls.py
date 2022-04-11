from django.urls import path
from .views import home,add_receptionist

app_name = 'receptionist'

urlpatterns = [
    path('', home, name='home'),
    path('add-receptionist/', add_receptionist, name='add-receptionist'),
]
