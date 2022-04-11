from django import forms
from django.contrib.auth import get_user_model

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