import email
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib import messages

from appointment.models import DailySlotBooking
from doctor.models import Doctor, DoctorTimeSlot
from .forms import DailyBookingForm, ReceptionistUserForm, ReceptionistForm

# Create your views here.

User = get_user_model()

USER_GROUP = {
    'RECEPTIONIST': 'RECEPTIONIST',
}


def home(request):
    return render(request, 'receptionist/index.html')


def add_receptionist(request):
    receptionist_user_form = ReceptionistUserForm()
    receptionist_form = ReceptionistForm()
    template_context = {
        'receptionist_user_form': receptionist_user_form,
        'receptionist_form': receptionist_form
    }
    if request.method == 'POST':
        receptionist_user_form = ReceptionistUserForm(request.POST)
        receptionist_form = ReceptionistForm(request.POST, request.FILES)
        print(receptionist_user_form.errors)
        print(receptionist_form.errors)
        if receptionist_user_form.is_valid() and receptionist_form.is_valid():

            receptionist_user = receptionist_user_form.save()
            receptionist_user.set_password(receptionist_user.password)
            receptionist_user.save()

            receptionist = receptionist_form.save(commit=False)
            receptionist.user = receptionist_user
            receptionist = receptionist.save()

            add_user_to_group(receptionist_user, 'RECEPTIONIST')

            return HttpResponse('Receptionist added successfully')
    return render(request, 'receptionist/add_receptionist.html', context=template_context)


def add_user_to_group(user, group):
    group = Group.objects.get(name=USER_GROUP[group])
    group.user_set.add(user)


def generate_daily_bookings(request):
    daily_booking_form = DailyBookingForm()
    template_context = {
        'daily_booking_form': daily_booking_form
    }
    if request.method == 'POST':
        daily_booking_form = DailyBookingForm(request.POST or None)
        if daily_booking_form.is_valid():
            print(daily_booking_form.cleaned_data)
            date = daily_booking_form.cleaned_data['date']
            doctors = daily_booking_form.cleaned_data['doctors']
            for doctor in doctors:
                doctor = User.objects.get(email=doctor.user.email)

                doctor_time_slots = DoctorTimeSlot.objects.filter(
                    doctor=doctor)
                for doctor_time_slot in doctor_time_slots:
                    daily_slot_booking, created = DailySlotBooking.objects.get_or_create(
                        doctor_time_slot=doctor_time_slot,
                        date=date,
                        status='AVAILABLE'
                    )
            # messages.success(request, 'Daily Bookings generated successfully')
            return HttpResponse('Daily Bookings generated successfully')
    return render(request, 'receptionist/generate_daily_bookings.html', context=template_context)
