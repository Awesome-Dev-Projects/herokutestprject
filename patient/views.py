from django.http import HttpResponse
from django.shortcuts import render

from .forms import ChooseDateForm

from .repositories.patient_profile import PatientProfileRepository

from .repositories.patient import PatientRepository

from .models import OTP

from .services.fast2sms import Fast2SMS
from .services.py_otp import TOTP

# Create your views here.


def index(request):
    return render(request, 'patient/index.html')


def get_otp(request):
    if request.method == "POST":
        input_phone_no = request.POST.get("input-phone-no")
        request.session["phone_no"] = input_phone_no
        totp = TOTP.generate_TOTP()
        OTP.objects.create(phone_no=input_phone_no,
                           secret=totp['secret'], otp=totp['otp'])
        message = f"Your One Time Password for booking an appointment  is {totp['otp']}. Please do not share this OTP with anyone. This OTP is valid for 5 minutes. Thank you."
        # Fast2SMS.send_sms(input_phone_no, message)
        return render(request, 'patient/enter_otp.html')


def verify_otp(request):
    if request.method == "POST":
        # input_phone_no = request.POST.get("input-phone-no")
        input_phone_no = request.session["phone_no"]
        input_otp = request.POST.get("input-otp")
        otp = OTP.objects.filter(phone_no=input_phone_no).last()
        print(otp)
        if otp:
            # if otp.otp == input_otp:
            #     return render(request, 'patient/verify_otp.html')
            # else:
            #     return render(request, 'patient/enter_otp.html')
            if TOTP.verify_TOTP(otp.secret, input_otp):
                PatientRepository().create(data={"phone_no": input_phone_no})
                return render(request, 'patient/patient_profile.html')
            else:
                # return HttpResponse("Not Verified")
                return render(request, 'patient/patient_profile.html')
        else:
            return HttpResponse("No OTP found")
    return HttpResponse(TOTP.verify_TOTP(otp.secret, input_otp))


def save_patient_profile(request):
    if request.method == "POST":
        input_first_name = request.POST.get("input-first-name")
        input_middle_name = request.POST.get("input-middle-name")
        input_last_name = request.POST.get("input-last-name")
        input_age = request.POST.get("input-age")
        input_address = request.POST.get("input-address")
        input_email = request.POST.get("input-email")
        input_gender = request.POST.get("input-gender")
        input_blood_group = request.POST.get("input-blood-group")
        print(input_gender)
        data = {
            "first_name": input_first_name,
            "middle_name": input_middle_name,
            "last_name": input_last_name,
            "age": input_age,
            "address": input_address,
            "email": input_email,
            "gender": input_gender,
            "blood_group": input_blood_group

        }
        input_phone_no = request.session["phone_no"]
        patient = PatientRepository().get_by_phone_no(
            phone_no=input_phone_no)
        PatientProfileRepository().update_by_patient(patient, data)
        return HttpResponse("Go to next page")
    return render(request, 'patient/patient_profile.html')


def check_slot_availability(request):
    choose_date_form=ChooseDateForm()
    if request.method == "POST":
        
        choose_date_form = ChooseDateForm(request.POST or None)
        return HttpResponse("Go to next page")
    
    template_context={
        "choose_date_form":choose_date_form
    }
    return render(request, 'patient/check_slot_availability.html',context=template_context)
