from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import Group
from django.contrib import messages

from .models import DoctorTimeSlot, TimeSlot

from .forms import DoctorUserForm, DoctorForm, TimeSlotForm

# Create your views here.
USER_GROUP = {
    'DOCTOR': 'DOCTOR',
}


def home(request):
    return render(request, 'doctor/index.html')


def add_doctor(request):
    doctor_user_form = DoctorUserForm()
    doctor_form = DoctorForm()
    template_context = {
        'doctor_user_form': doctor_user_form,
        'doctor_form': doctor_form
    }
    if request.method == 'POST':
        doctor_user_form = DoctorUserForm(request.POST)
        doctor_form = DoctorForm(request.POST, request.FILES)
        print(doctor_user_form.errors)
        print(doctor_form.errors)
        if doctor_user_form.is_valid() and doctor_form.is_valid():

            doctor_user = doctor_user_form.save()
            doctor_user.set_password(doctor_user.password)
            doctor_user.save()

            doctor = doctor_form.save(commit=False)
            doctor.user = doctor_user
            doctor = doctor.save()

            add_user_to_group(doctor_user, 'DOCTOR')

            return HttpResponse('Doctor added successfully')
    return render(request, 'doctor/add_doctor.html', context=template_context)


def add_user_to_group(user, group):
    group = Group.objects.get(name=USER_GROUP[group])
    group.user_set.add(user)


def add_time_slot(request):
    time_slot_form = TimeSlotForm()
    if request.method == 'POST':
        time_slot_form = TimeSlotForm(request.POST or None)
        if time_slot_form.is_valid():
            time_slot, created = TimeSlot.objects.get_or_create(
                day=time_slot_form.cleaned_data['day'],
                start_time=time_slot_form.cleaned_data['start_time'],
                end_time=time_slot_form.cleaned_data['end_time'],
                half_time=time_slot_form.cleaned_data['half_time']
            )
            # doctor_time_slot = DoctorTimeSlot.objects.filter(
            #     doctor=request.user, time_slot=time_slot)
            # if doctor_time_slot.exists():
            #     raise time_slot_form.ValidationError(
            #         "Time Slot already exists")

            doctor_time_slot, created = DoctorTimeSlot.objects.get_or_create(
                doctor=request.user,
                time_slot=time_slot
            )
            if created:
                messages.success(request, 'Time Slot added successfully')
                return render(request, 'doctor/add_time_slot.html', context={'time_slot_form': time_slot_form})
            else:
                time_slot_form.errors.update(
                    {'__all__': ['Time Slot already exists']})
    template_context = {'time_slot_form': time_slot_form}
    return render(request, 'doctor/add_time_slot.html', context=template_context)
