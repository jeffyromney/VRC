from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context, RequestContext
from django.template.loader import get_template
from django.shortcuts import render, redirect
from VRC.forms import *
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserChangeForm
from django.forms import CheckboxInput
from django.forms.models import model_to_dict
from printing import *
import datetime

#@permission_required('VRC.add_volunteer')
def addVolunteer(request):
    runCleanup()
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
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
    runCleanup()
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_Organization = form.save()
            #return render(request, 'addOrganization.html', {'form': form})
            return HttpResponseRedirect('/Organization/viewNew/' + str(new_Organization.id))
        else:
            return render(request, 'addOrganization.html', {'form': form})
    else:
        form = OrganizationForm()
        print(form)
        return render(request, 'addOrganization.html', {'form': form})

@permission_required('VRC.add_job')
def addJob(request):
    runCleanup()
    if request.method == 'POST':
        form = JobForm(request.POST)
        print(request.POST['title'])
        if form.is_valid():
            cd = form.cleaned_data
            new_Job = form.save()
            return HttpResponseRedirect('/Job/viewNew/' + str(new_Job.id))
        else:
            return render(request, 'addJob.html', {'form': form})
    else:
        form = JobForm()
        return render(request, 'addJob.html', {'form': form})


def welcome(request,loggedOut=False):
    runCleanup()
    #print(UserChangeForm())
    return render(request, 'base.html', {'loggedOut':loggedOut, 'request':request})


def loginSuccess(request):
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
    runCleanup()
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
    runCleanup()
    volunteer = Volunteer.objects.get(id=dbID)
    form = VolunteerForm(request.POST or None, instance=volunteer, initial = {'job': volunteer.job })
    if volunteer.job is not None and volunteer.job.full:
        form.fields['job'].queryset=Job.objects.filter(id=volunteer.job.id) | Job.objects.filter(full=False)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            new_Volunteer = form.save()
            #return HttpResponse("Form Valid" + str(cd) + str(new_Volunteer))
            return viewVolunteer(request,dbID) #render(request, 'addVolunteer.html', {'volunteer':volunteer, 'form': form, 'viewNew':False, 'viewOnly':True})
        else:
            return render(request, 'addVolunteer.html', {'volunteer':volunteer, 'form': form, 'modify':True})
    else:
        #form = VolunteerForm(instance=volunteer)
        return render(request, 'addVolunteer.html', {'volunteer':volunteer, 'form': form, 'modify':True})


#@permission_required('VRC.View_data')
def viewVolunteer(request,dbID,viewNew=False):
    runCleanup()
    if(request.user.has_perm('VRC.View_data') or viewNew):
        volunteer = Volunteer.objects.get(id=dbID)
        form = VolunteerForm(instance=volunteer).disabled()
        return render(request, 'addVolunteer.html', {'volunteer':volunteer, 'form': form, 'viewNew':viewNew, 'viewOnly':True})
    else:
        return HttpResponseRedirect('/accounts/login?next=' + request.path)
    
    
def viewNewVolunteer(request,dbID):
    runCleanup()
    #printVolunteer(dbID)
    return viewVolunteer(request,dbID,viewNew=True)

def printVolunteer(request,dbID):
    volunteer = Volunteer.objects.get(id=dbID)
    autoPrint = True
    if volunteer.job:
        job = volunteer.job
        org = volunteer.job.agency
    return render(request, 'printVolunteer.html', locals())

@permission_required('VRC.delete_Volunteer')
def deleteVolunteer(request, dbID):
    runCleanup()
    if request.method == 'POST':
        volunteer = Volunteer.objects.get(id=dbID)
        name = volunteer.name
        volunteer.delete()
        return render(request, 'deleted.html', {'name':name})
    else:
        prevUrl = request.REQUEST.get('next', '')
        return render(request, 'confirmation.html', {'message':'Are you sure?','prev_link':prevUrl,'action_link':'/Volunteer/delete/'+str(dbID)+'/'})
    
    


#@permission_required('VRC.change_job')
def modifyJob(request,dbID):
    runCleanup()
    job = Job.objects.get(id=dbID)
    form = JobForm(request.POST or None,instance=job)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            new_Job = form.save()
            return viewJob(request,dbID) #HttpResponse("Form Valid" + str(cd) + str(new_Job))
        else:
            return render(request, 'addJob.html', {'job':job, 'form': form})
    else:
        return render(request, 'addJob.html', {'job':job, 'form': form})


@permission_required('VRC.View_data')
def viewJob(request,dbID,viewNew=False):
    runCleanup()
    job = Job.objects.get(id=dbID)
    form = JobForm(instance=job).disabled()
    vols = job.volunteer_set
    return render(request, 'addJob.html', {'job':job, 'form': form, 'viewNew':viewNew, 'viewOnly':True, 'vols':vols})
    
    
def viewNewJob(request,dbID):
    runCleanup()
    return viewJob(request,dbID,viewNew=True)

@permission_required('VRC.delete_Volunteer')
def deleteJob(request, dbID):
    runCleanup()
    if request.method == 'POST':
        job = Job.objects.get(id=dbID)
        title = job.title
        job.delete()
        return render(request, 'deleted.html', {'name':title})
    else:
        prevUrl = request.REQUEST.get('next', '')
        return render(request, 'confirmation.html', {'message':'Are you sure?','prev_link':prevUrl,'action_link':'/Job/delete/'+str(dbID)+'/'})





#@permission_required('VRC.change_organization')
def modifyOrganization(request,dbID):
    runCleanup()
    organization = Organization.objects.get(id=dbID)
    form = OrganizationForm(request.POST or None,instance=organization)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            new_Organization = form.save()
            return viewOrganization(request,dbID) #HttpResponse("Form Valid" + str(cd) + str(new_Organization))
        else:
            return render(request, 'addOrganization.html', {'organization':organization, 'form': form})
    else:
        return render(request, 'addOrganization.html', {'organization':organization, 'form': form})


@permission_required('VRC.View_data')
def viewOrganization(request,dbID,viewNew=False):
    runCleanup()
    organization = Organization.objects.get(id=dbID)
    form = OrganizationForm(instance=organization).disabled()
    jobs = organization.job_set
    return render(request, 'addOrganization.html', {'organization':organization, 'form': form, 'viewNew':viewNew, 'viewOnly':True,'jobs':jobs})
    
    
def viewNewOrganization(request,dbID):
    runCleanup()
    return viewOrganization(request,dbID,viewNew=True)

@permission_required('VRC.delete_Volunteer')
def deleteOrganization(request, dbID):
    runCleanup()
    if request.method == 'POST':
        organization = Organization.objects.get(id=dbID)
        name = organization.name
        organization.delete()
        return render(request, 'deleted.html', {'name':name})
    else:
        prevUrl = request.REQUEST.get('next', '')
        return render(request, 'confirmation.html', {'message':'Are you sure?','prev_link':prevUrl,'action_link':'/Organization/delete/'+str(dbID)+'/'})
    
    

def Stations(request, dbID):
    runCleanup()
    volunteer = Volunteer.objects.get(id=dbID)
    form = VolunteerForm(request.POST or None, instance=volunteer, initial = {'job': volunteer.job })
    if volunteer.job is not None and volunteer.job.full:
        form.fields['job'].queryset=Job.objects.filter(id=volunteer.job.id) | Job.objects.filter(full=False)
    for field in form.fields:
        if form.fields[field].widget.__class__.__name__ == CheckboxInput().__class__.__name__:
            if field not in ['idCheck', 'dataValidation', 'interview', 'safety', 'idbadge', 'maps']:
                form.fields[field].widget.attrs['disabled'] = True
        elif field != 'job':
            form.fields[field].widget.attrs['disabled'] = True
            form.fields[field].widget.attrs['readonly'] = True
            
    if request.method == 'POST':
        form.is_valid()
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
        return viewVolunteer(request,dbID)
    else:
        return render(request, 'stations.html', {'volunteer':volunteer, 'form': form})
    
def help(request):
    return render(request, 'help.html')
    
#from registration.backends.simple.views import RegistrationView

#class MyRegistrationView(RegistrationView):
#    def get_success_url(self, request, user):
#        return "/"
        
def runCleanup():
    start = datetime.datetime.now()
    #volunteers = Volunteer.objects.all()
    jobs = Job.objects.all()
    #for volunteer in volunteers:
    #    if False:
    #        pass
            #volunteer.delete()
    for job in jobs:
        debug1 = datetime.datetime.now().date()
        debug2 = job.edate
        initialFull = job.full
        if job.volunteer_set.count() >= job.number:
            job.full = True
            reason = 'Request Fulfilled'
        elif job.edate is not None:
            if job.edate < datetime.datetime.now().date():
                job.full = True
                reason = 'Expired'
            else:
                job.full = False
                reason = 'No Longer Full'
        else:
            job.full = False
            reason = 'No Longer Full'
        if job.full != initialFull:
            pass
            job.save(update_fields=['full'])
            print('CLEANUP - CHANGED STATUS OF JOB: ' + job.title + '. Reason: ' + reason)




