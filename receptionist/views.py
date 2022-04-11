from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import Group
from django.contrib import messages

from .forms import ReceptionistUserForm, ReceptionistForm

# Create your views here.

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
