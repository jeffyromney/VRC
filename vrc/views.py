from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
from VRC.forms import *

def addVolunteer(request):
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_Volunteer = form.save()
            return HttpResponse("Form Valid" + str(cd) + str(new_Volunteer))
        else:
            return HttpResponse("Form not Valid")
    else:
        form = VolunteerForm()
        return render(request, 'add.html', {'form': form, 'type': "Job"})


def addOrganization(request):
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_Organization = form.save()
            return HttpResponse("Form Valid" + str(cd))
        else:
            return HttpResponse("Form not Valid")
    else:
        form = OrganizationForm()
        return render(request, 'add.html', {'form': form, 'type': "Job"})

def addJob(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_Job = form.save()
            return HttpResponse("Form Valid" + str(cd))
        else:
            return HttpResponse("Form not Valid")
    else:
        form = JobForm()
        return render(request, 'add.html', {'form': form, 'type': "Job"})


def welcome(request):
    return render(request, 'base.html', {})
