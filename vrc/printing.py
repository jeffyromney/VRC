from VRC.models import *
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def printVolunteer(ID):
    volunteer = Volunteer.objects.get(id=ID)
    job = volunteer.job
    agency = job.agency
    html = render(HttpRequest(), 'addVolunteer.html', {'volunteer': form, 'job':job, 'agency':agency})
    print(html)
    return(1)




def printJob(ID):
    return(1)
