from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context, RequestContext
from django.template.loader import get_template
from django.shortcuts import render, redirect
from VRC.forms import *
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.forms import CheckboxInput
from itertools import chain
from django.forms.models import model_to_dict

#@permission_required('VRC.add_volunteer')
def addVolunteer(request):
    if request.method == 'POST':
        form = VolunteerForm(request.POST,request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            new_Volunteer = form.save()
            return HttpResponseRedirect('/Volunteer/viewNew/' + str(new_Volunteer.id))
        else:
            return render(request, 'addVolunteer.html', {'form': form})
    else:
        form = VolunteerForm()
        return render(request, 'addVolunteer.html', {'form': form})


@permission_required('VRC.add_organization')
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
        return render(request, 'addOrganization.html', {'form': form})

@permission_required('VRC.add_job')
def addJob(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_Job = form.save()
            return HttpResponse("Form Valid" + str(cd))
        else:
            return render(request, 'addJob.html', {'form': form})#return HttpResponse("Form not Valid")
    else:
        form = JobForm()
        return render(request, 'addJob.html', {'form': form})


def welcome(request,loggedOut=False):
    return render(request, 'base.html', {'loggedOut':loggedOut, 'request':request})


def loginSuccess(request):
    permissions = request.user.get_all_permissions()
    return render(request, 'registration/success.html')
    
    
def loggedOut(request):
    return welcome(request,loggedOut=True)


import re

from django.db.models import Q

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query



@permission_required('VRC.View_data')
def search(request):
    query_string = ''
    vols = None
    jobs = None
    orgs = None
    if ('q' in request.GET) and request.GET['q'].strip():
        if request.GET['q'] == 'ALL':
            vols = Volunteer.objects.all().order_by('id')
            jobs = Job.objects.all().order_by('id')
            orgs = Organization.objects.all().order_by('id')
        else:
            query_string = request.GET['q']
            entry_query_vol = get_query(query_string, ['name', 'id','cellPhone', 'dayPhone'])
            entry_query_job = get_query(query_string, ['id','title'])
            entry_query_org = get_query(query_string, ['name', 'id', 'contact', 'phone'])
            vols = Volunteer.objects.filter(entry_query_vol).order_by('id')
            jobs = Job.objects.filter(entry_query_job).order_by('id')
            orgs = Organization.objects.filter(entry_query_org).order_by('id')

    return render(request,'search.html', { 'query': query_string, 'vols': vols, 'jobs':jobs, 'orgs':orgs }, )#context_instance=RequestContext(request))


@permission_required('VRC.change_volunteer')
def modifyVolunteer(request,dbID):
    volunteer = Volunteer.objects.get(id=dbID)
    if request.method == 'POST':
        form = VolunteerForm(request.POST, request.FILES, instance=volunteer)
        if form.is_valid():
            cd = form.cleaned_data
            new_Volunteer = form.save()
            return HttpResponse("Form Valid" + str(cd) + str(new_Volunteer))
        else:
            return render(request, 'addVolunteer.html', {'volunteer':volunteer, 'form': form})
            #return HttpResponse("Form not Valid")
    else:
        form = VolunteerForm(instance=volunteer)
        return render(request, 'addVolunteer.html', {'volunteer':volunteer, 'form': form})


#@permission_required('VRC.View_data')
def viewVolunteer(request,dbID,viewNew=False):
    if(request.user.has_perm('VRC.View_data') or viewNew):
        volunteer = Volunteer.objects.get(id=dbID)
        form = VolunteerForm(instance=volunteer).disabled()
        return render(request, 'addVolunteer.html', {'volunteer':volunteer, 'form': form, 'viewNew':viewNew, 'viewOnly':True})
    else:
        return HttpResponseRedirect('/accounts/login?next=' + request.path)
    
    
def viewNewVolunteer(request,dbID):
    return viewVolunteer(request,dbID,viewNew=True)

def deleteVolunteer(request, dbID):
    volunteer = Volunteer.objects.get(id=dbID)
    name = volunteer.name
    volunteer.delete()
    return render(request, 'deleted.html', {'name':name})
    
    



#@permission_required('VRC.change_job')
def modifyJob(request,dbID):
    job = Job.objects.get(id=dbID)
    form = JobForm(request.POST or None,instance=job)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            new_Job = form.save()
            return HttpResponse("Form Valid" + str(cd) + str(new_Job))
        else:
            return render(request, 'addJob.html', {'job':job, 'form': form})
            #return HttpResponse("Form not Valid")
    else:
        return render(request, 'addJob.html', {'job':job, 'form': form})


@permission_required('VRC.View_data')
def viewJob(request,dbID,viewNew=False):
    job = Job.objects.get(id=dbID)
    form = JobForm(instance=job).disabled()
    return render(request, 'addJob.html', {'job':job, 'form': form, 'viewNew':viewNew, 'viewOnly':True})
    
    
def viewNewJob(request,dbID):
    return viewJob(request,dbID,viewNew=True)

def deleteJob(request, dbID):
    job = Job.objects.get(id=dbID)
    title = job.title
    job.delete()
    return render(request, 'deleted.html', {'title':title})





#@permission_required('VRC.change_organization')
def modifyOrganization(request,dbID):
    organization = Organization.objects.get(id=dbID)
    form = OrganizationForm(request.POST or None,instance=organization)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            new_Organization = form.save()
            return HttpResponse("Form Valid" + str(cd) + str(new_Organization))
        else:
            return render(request, 'addOrganization.html', {'organization':organization, 'form': form})
            #return HttpResponse("Form not Valid")
    else:
        return render(request, 'addOrganization.html', {'organization':organization, 'form': form})


@permission_required('VRC.View_data')
def viewOrganization(request,dbID,viewNew=False):
    organization = Organization.objects.get(id=dbID)
    form = OrganizationForm(instance=organization).disabled()
    return render(request, 'addOrganization.html', {'organization':organization, 'form': form, 'viewNew':viewNew, 'viewOnly':True})
    
    
def viewNewOrganization(request,dbID):
    return viewOrganization(request,dbID,viewNew=True)

def deleteOrganization(request, dbID):
    organization = Organization.objects.get(id=dbID)
    name = organization.name
    organization.delete()
    return render(request, 'deleted.html', {'name':name})
    
    

def Stations(request, dbID):
    volunteer = Volunteer.objects.get(id=dbID)
    form = VolunteerForm(request.POST or None, instance=volunteer, initial = {'job': volunteer.job })
    if volunteer.job is not None and volunteer.job.full:
        form.fields['job'].queryset=Job.objects.filter(id=volunteer.job.id) | Job.objects.filter(full=False)
    for field in form.fields:
        if form.fields[field].widget.__class__.__name__ == CheckboxInput().__class__.__name__:
            if field not in ['idCheck', 'dataValidation', 'interview', 'safety', 'idbadge', 'maps']:
                form.fields[field].widget.attrs['disabled'] = True
        elif field != 'job':
            form.fields[field].widget.attrs['readonly'] = True
            
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            if(request.user.has_perm('VRC.IDCheck')):
                volunteer.save(update_fields=['idCheck'])
            if(request.user.has_perm('VRC.Data_Validation')):
                volunteer.save(update_fields=['dataValidation'])
            if(request.user.has_perm('VRC.Interview')):
                volunteer.save(update_fields=['job','interview'])
            if(request.user.has_perm('VRC.Safety')):
                volunteer.save(update_fields=['safety'])
            if(request.user.has_perm('VRC.IDBadge')):
                volunteer.save(update_fields=['idbadge'])
            if(request.user.has_perm('VRC.Maps')):
                volunteer.save(update_fields=['maps'])
            return HttpResponse("Form Valid" + str(cd) + "\n" + 'f')
        else:
            return HttpResponse("Form not Valid")
    else:
        return render(request, 'stations.html', {'volunteer':volunteer, 'form': form})
    
def help(request):
    return render(request, 'help.html')
