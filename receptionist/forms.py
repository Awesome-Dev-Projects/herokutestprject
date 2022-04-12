from django import forms
from django.contrib.auth import get_user_model
from datetime import date

from doctor.models import Doctor

from .models import Receptionist

User = get_user_model()


class ReceptionistUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class ReceptionistForm(forms.ModelForm):
    class Meta:
        model = Receptionist
        fields = ['first_name', 'middle_name',
                  'last_name', 'phone_no', 'address', 'profile_image']


class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class DailyBookingForm(forms.Form):
    doctor_choices = Doctor.objects.all().values_list('id', 'first_name')
    date = forms.DateField(initial=date.today(),
                           widget=forms.DateInput(attrs={'type': 'date'}))
    # doctors = forms.MultipleChoiceField(
    #     choices=doctor_choices, widget=forms.CheckboxSelectMultiple())
    doctors = CustomModelMultipleChoiceField(label="Select Doctors", queryset=Doctor.objects.all(), initial=list(Doctor.objects.all()), widget=forms.CheckboxSelectMultiple())
