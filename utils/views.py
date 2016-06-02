from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context, RequestContext
from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.forms.models import model_to_dict
import datetime
from django.core import serializers
import socket



def sync_mobile(request):
    if(checkInput_mobile(request) and sync_mobileData(request)):
        return HttpResponse('Mobile device synced successfully',200)
    else:
        return HttpResponse('Request must be a POST request with the database data in proper format',400)


def checkInput_mobile(request):
    if(request.method == 'POST' and
       databaseData   in request.POST and 
       userID         in request.POST and 
       timestamp      in request.POST and
       sourceID       in request.POST ):
        return True
    else:
        return False

def sync_mobileData(request):
    if True:
        return True
    else:
        return False


def sync_vrc(request):
    if(checkInput_vrc(request) and sync_vrcData(request)):
        return HttpResponse('VRC ' + str(request.POST.get('vrcID')) + 'Synced successfully',200)
    else:
        return HttpResponse('Request must be a POST request with the database data in proper format',400)

def checkInput_vrc(request):
    if(request.method == 'POST' and
       vrcID          in request.POST and
       timestamp      in request.POST ):
        return True
    else:
        return False


# Checks each entry in the database and syncs with main online database
# Compares each item in the request with all the items of the same type in the database. 
# If it matches, it checks the timestamps and updates or keeps the database entry to match the newest
# When done, it filters a new list of all the entries for the given vrcID and returns the new database information with a request ID number.
# The client VRC should update it's database according to what is returned and send an ACK to the server for the given request ID.
def sync_vrcData(request):
    retVal = False
    try:
        for org in data['orgs']:
            pass #process each org
        for job in data['jobs']:
            pass #process each job
        for vol in data['vols']:
            pass #process each volunteer
        for group in data['auth']['groups']:
            pass #process group changes
        for user in data['auth']['users']:
            pass #process user changes
    except:
        retVal = False

    return retVal