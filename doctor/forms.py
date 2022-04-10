from django import forms

from users.models import User
from .models import Doctor, TimeSlot


class DoctorUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['first_name', 'middle_name',
                  'last_name', 'phone_no', 'address', 'qualification', 'experience', 'specialization', 'fees', 'timings', 'profile_image', 'certificate_image']


class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['day', 'start_time', 'end_time', 'half_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    # def clean(self):
    #     day = self.cleaned_data['day']
    #     start_time = self.cleaned_data['start_time']
    #     end_time = self.cleaned_data['end_time']
    #     half_time = self.cleaned_data['half_time']
    #     # time_slot = TimeSlot.objects.filter(
    #     #     day=day, start_time=start_time, end_time=end_time, half_time=half_time)
    #     # if time_slot.exists():
    #     #     raise forms.ValidationError("Time Slot already exists")
    #     # time_slot, created = TimeSlot.objects.get_or_create(
    #     #     day=day, start_time=start_time, end_time=end_time, half_time=half_time)
    #     # print(created)
    #     return self.cleaned_data

    # def save(self,commit=True):
    #     time_slot = super(TimeSlotForm, self).save(commit=False)
    #     time_slot.day = self.cleaned_data['day'].title()
    #     time_slot.half_time = self.cleaned_data['half_time'].title()
    #     if commit:
    #         time_slot.save()
    #     return time_slot
