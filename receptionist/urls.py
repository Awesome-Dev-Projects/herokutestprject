from django.urls import path
from .views import home,add_receptionist,generate_daily_bookings

app_name = 'receptionist'

urlpatterns = [
    path('', home, name='home'),
    path('add-receptionist/', add_receptionist, name='add-receptionist'),
    path('generate-daily-bookings/', generate_daily_bookings, name='generate-daily-bookings'),
]
