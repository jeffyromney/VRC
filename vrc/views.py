from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context, RequestContext
from django.template.loader import get_template
from django.shortcuts import render, redirect
from vrcAPP.forms import *
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserChangeForm
from django.forms import CheckboxInput
from django.forms.models import model_to_dict
from vrc.printing import *
import datetime
import vrc.vrcLogging
from django.core import serializers
import socket
from django.contrib.admin.models import LogEntry


# for logs, insert=1 update=2 delete=3 volunteer=1 job=2 organization=3

def addVolunteer(request):
	runCleanup()
	if request.method == 'POST':   #If form is being submitted
		if ('continue' in request.GET) and request.GET.get('continue') == '1':
			form = VolunteerForm(request.session.get('formBackupVol'))
			try:
				del request.session['formBackupVol']
			except KeyError:
	 			pass
		else:
			form = VolunteerForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			dups = getDuplicateVolunteers({'name':cd['name'], 'birthday':cd['birthday']})
			print(dups)
			if dups:
				if ('continue' in request.GET) and request.GET.get('continue') == '1':
					new_Volunteer = form.save() #save to database
					LogEntry.objects.log_action(
							user_id = request.user.id or 0,
							content_type_id = 1,
							object_id = new_Volunteer.id,
							object_repr=new_Volunteer.name,
							change_message = 'Added new Volunteer to Database',
							action_flag = 1
						   )
					return HttpResponseRedirect('/Volunteer/viewNew/' + str(new_Volunteer.id))
				else:
					request.session['formBackupVol'] = request.POST
					return render(request, 'duplicateCheck.html', {'form':form, 'duplicates':dups, 'type':'vol'})
			else:
				new_Volunteer = form.save() #save to database
				LogEntry.objects.log_action(
							user_id = request.user.id or 0,
							content_type_id = 1,
							object_id = new_Volunteer.id,
							object_repr=new_Volunteer.name,
							change_message = 'Added new Volunteer to Database',
							action_flag = 1
						   )
				#vrcLogging.logData('added new volunteer---	 name:' + str(new_Volunteer.name) + 'id: ' + str(new_Volunteer.id))
				return HttpResponseRedirect('/Volunteer/viewNew/' + str(new_Volunteer.id))
		else:
			return render(request, 'addVolunteer.html', {'form': form})
	else:
		form = VolunteerForm()
		return render(request, 'addVolunteer.html', {'form': form})

# Add an organization to the database
@permission_required('vrcAPP.Phone_Bank')
def addOrganization(request):
	runCleanup()
	if request.method == 'POST':   #If form is being submitted
		if ('continue' in request.GET) and request.GET.get('continue') == '1':
			form = OrganizationForm(request.session.get('formBackupOrg'))
			try:
				del request.session['formBackupOrg']
			except KeyError:
	 			pass
		else:
			form = OrganizationForm(request.POST) 
		if form.is_valid():
			cd = form.cleaned_data
			dups = getDuplicateOrganizations(cd['name'])
			if dups:
				if ('continue' in request.GET) and request.GET.get('continue') == '1':
					new_Organization = form.save() #save to database
					LogEntry.objects.log_action(
							user_id = request.user.id or 0,
							content_type_id = 3,
							object_id = new_Organization.id,
							object_repr=new_Organization.name,
							change_message = 'Added new Organization to Database',
							action_flag = 1
						   )
					return HttpResponseRedirect('/Organization/viewNew/' + str(new_Organization.id))
				else:
					request.session['formBackupOrg'] = request.POST
					return render(request, 'duplicateCheck.html', {'form':form, 'duplicates':dups, 'type':'org'})
			else:
				new_Organization = form.save() #save to database
				LogEntry.objects.log_action(
							user_id = request.user.id or 0,
							content_type_id = 3,
							object_id = new_Organization.id,
							object_repr=new_Organization.name,
							change_message = 'Added new Organization to Database',
							action_flag = 1
						   )
				return HttpResponseRedirect('/Organization/viewNew/' + str(new_Organization.id)) 
		else:
			return render(request, 'addOrganization.html', {'form': form}) #form is not valid - return to form
	else:  # new  blank form
		form = OrganizationForm()
		return render(request, 'addOrganization.html', {'form': form})

# Add a request for volunteers to the database
@permission_required('vrcAPP.Phone_Bank')
def addJob(request):
	runCleanup()
	if request.method == 'POST':   #If form is being submitted
		if ('continue' in request.GET) and request.GET.get('continue') == '1':
			form = JobForm(request.session.get('formBackupJob'))
			try:
				del request.session['formBackupJob']
			except KeyError:
	 			pass
		else:
			form = JobForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			dups = getDuplicateJobs(cd['title'])
			if dups:
				if ('continue' in request.GET) and request.GET.get('continue') == '1':
					new_Job = form.save() #save to database
					LogEntry.objects.log_action(
							user_id = request.user.id or 0,
							content_type_id = 2,
							object_id = new_Job.id,
							object_repr=new_Job.title,
							change_message = 'Added new Job to Database',
							action_flag = 1
						   )
					return HttpResponseRedirect('/Job/viewNew/' + str(new_Job.id))
				else:
					request.session['formBackupOrg'] = request.POST
					return render(request, 'duplicateCheck.html', {'form':form, 'duplicates':dups, 'type':'job'})
			else:
				new_Job = form.save() #save to database
				LogEntry.objects.log_action(
							user_id = request.user.id or 0,
							content_type_id = 2,
							object_id = new_Job.id,
							object_repr=new_Job.title,
							change_message = 'Added new Job to Database',
							action_flag = 1
						   )
				return HttpResponseRedirect('/Job/viewNew/' + str(new_Job.id))
		else:
			return render(request, 'addJob.html', {'form': form})  #form is not valid - return to form
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

def getDuplicateVolunteers(info):
	vols = None
	entry_query = get_query(info['name'],['name'])
	vols = Volunteer.objects.filter(entry_query).filter(birthday=info['birthday']).order_by('name')
	return vols
	
def getDuplicateOrganizations(name):
	orgs = None
	entry_query = get_query(name,['name'])
	orgs = Organization.objects.filter(entry_query).filter(name=name).order_by('name')
	return orgs
	
def getDuplicateJobs(title):
	jobs = None
	entry_query = get_query(title,['title'])
	jobs = Job.objects.filter(entry_query).filter(title=title).order_by('title')
	return jobs


@permission_required('vrcAPP.View_data')
def search(request):
	runCleanup()
	query_string = ''
	vols = None
	jobs = None
	orgs = None
	if ('q' in request.GET) and request.GET['q'].strip():
		if request.GET['q'] == 'ALL':
			vols = Volunteer.objects.all().order_by('name')
			jobs = Job.objects.all().order_by('title')
			orgs = Organization.objects.all().order_by('name')
		else:
			query_string = request.GET['q']
			entry_query_vol = get_query(query_string, ['name', 'id','cellPhone', 'dayPhone'])
			entry_query_job = get_query(query_string, ['id','title'])
			entry_query_org = get_query(query_string, ['name', 'id', 'contact', 'phone'])
			vols = Volunteer.objects.filter(entry_query_vol).order_by('name')
			jobs = Job.objects.filter(entry_query_job).order_by('title')
			orgs = Organization.objects.filter(entry_query_org).order_by('name')
	return render(request,'search.html', { 'query': query_string, 'vols': vols, 'jobs':jobs, 'orgs':orgs }, )#context_instance=RequestContext(request))


@permission_required('vrcAPP.change_volunteer')
def modifyVolunteer(request,dbID):
	runCleanup()
	volunteer = Volunteer.objects.get(id=dbID)
	form = VolunteerForm(request.POST or None, instance=volunteer, initial = {'job': volunteer.job })
	if volunteer.job is not None and volunteer.job.full:
		form.fields['job'].queryset=Job.objects.filter(id=volunteer.job.id) | Job.objects.filter(full=False)
	if request.method == 'POST':   #If form is being submitted
		if form.is_valid():
			cd = form.cleaned_data
			new_Volunteer = form.save() #save to database
			LogEntry.objects.log_action(
							user_id = request.user.id or 0,
							content_type_id = 1,
							object_id = new_Volunteer.id,
							object_repr=new_Volunteer.name,
							change_message = 'Modified Volunteer in Database',
							action_flag = 2
						   )
			return viewVolunteer(request,dbID) 
		else:   #form is not valid - return to form
			return render(request, 'addVolunteer.html', {'volunteer':volunteer, 'form': form, 'modify':True}) 
	else:
		return render(request, 'addVolunteer.html', {'volunteer':volunteer, 'form': form, 'modify':True})


#@permission_required('vrcAPP.View_data')
def viewVolunteer(request,dbID,viewNew=False):
	runCleanup()
	if(request.user.has_perm('vrcAPP.View_data') or viewNew):
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
	
	
def printJob(request,dbID):
	job = Job.objects.get(id=dbID)
	autoPrint = True
	if job.agency:
		agency = job.agency
	vols = job.volunteer_set.all()
	viewOnly = True
	return render(request, 'printJob.html', locals())

@permission_required('vrcAPP.delete_Volunteer')
def deleteVolunteer(request, dbID):
	runCleanup()
	if request.method == 'POST':   #If form is being submitted
		volunteer = Volunteer.objects.get(id=dbID)
		name = volunteer.name
		volunteer.delete()   #Delete volunteer from database
		try:
			LogEntry.objects.log_action(
							user_id = request.user.id or 0,
							content_type_id = 1,
							object_id = volunteer.id,
							object_repr=volunteer.name,
							change_message = 'Deleted Volunteer from Database',
							action_flag = 3
						   )
		except:
			pass
		return render(request, 'deleted.html', {'name':name})
	else:
		prevUrl = request.REQUEST.get('next', '')
		return render(request, 'confirmation.html', {'message':'Are you sure?','prev_link':prevUrl,'action_link':'/Volunteer/delete/'+str(dbID)+'/'})  #  Send back to previous URL
	
	


#@permission_required('vrcAPP.change_job')
def modifyJob(request,dbID):
	runCleanup()
	job = Job.objects.get(id=dbID)
	form = JobForm(request.POST or None,instance=job)
	if request.method == 'POST':   #If form is being submitted
		if form.is_valid():
			cd = form.cleaned_data
			new_Job = form.save() #save to database
			LogEntry.objects.log_action(
							user_id = request.user.id or 0,
							content_type_id = 2,
							object_id = new_Job.id,
							object_repr=new_Job.title,
							change_message = 'Modified Job in Database',
							action_flag = 2
						   )
			return viewJob(request,dbID) #HttpResponse("Form Valid" + str(cd) + str(new_Job))
		else:
			return render(request, 'addJob.html', {'job':job, 'form': form})
	else:
		return render(request, 'addJob.html', {'job':job, 'form': form})


@permission_required('vrcAPP.View_data')
def viewJob(request,dbID,viewNew=False):
	runCleanup()
	job = Job.objects.get(id=dbID)
	form = JobForm(instance=job).disabled()
	vols = job.volunteer_set
	return render(request, 'addJob.html', {'job':job, 'form': form, 'viewNew':viewNew, 'viewOnly':True, 'vols':vols})
	
	
def viewNewJob(request,dbID):
	runCleanup()
	return viewJob(request,dbID,viewNew=True)

@permission_required('vrcAPP.delete_Volunteer')
def deleteJob(request, dbID):
	runCleanup()
	if request.method == 'POST':   #If form is being submitted
		job = Job.objects.get(id=dbID)
		title = job.title
		job.delete()
		LogEntry.objects.log_action(
							user_id = request.user.id or 0,
							content_type_id = 2,
							object_id = job.id,
							object_repr=job.title,
							change_message = 'Deleted Job from Database',
							action_flag = 3
						   )
		return render(request, 'deleted.html', {'name':title})
	else:
		prevUrl = request.REQUEST.get('next', '')
		return render(request, 'confirmation.html', {'message':'Are you sure?','prev_link':prevUrl,'action_link':'/Job/delete/'+str(dbID)+'/'})





#@permission_required('vrcAPP.change_organization')
def modifyOrganization(request,dbID):
	runCleanup()
	organization = Organization.objects.get(id=dbID)
	form = OrganizationForm(request.POST or None,instance=organization)
	if request.method == 'POST':   #If form is being submitted
		if form.is_valid():
			cd = form.cleaned_data
			new_Organization = form.save() #save to database
			LogEntry.objects.log_action(
							user_id = request.user.id or 0,
							content_type_id = 3,
							object_id = new_Organization.id,
							object_repr=new_Organization.name,
							change_message = 'Modified Organization in Database',
							action_flag = 2
						   )
			return viewOrganization(request,dbID) #HttpResponse("Form Valid" + str(cd) + str(new_Organization))
		else:
			return render(request, 'addOrganization.html', {'organization':organization, 'form': form})
	else:
		return render(request, 'addOrganization.html', {'organization':organization, 'form': form})


@permission_required('vrcAPP.View_data')
def viewOrganization(request,dbID,viewNew=False):
	runCleanup()
	organization = Organization.objects.get(id=dbID)
	form = OrganizationForm(instance=organization).disabled()
	jobs = organization.job_set
	return render(request, 'addOrganization.html', {'organization':organization, 'form': form, 'viewNew':viewNew, 'viewOnly':True,'jobs':jobs})
	
	
def viewNewOrganization(request,dbID):
	runCleanup()
	return viewOrganization(request,dbID,viewNew=True)

@permission_required('vrcAPP.delete_Volunteer')
def deleteOrganization(request, dbID):
	runCleanup()
	if request.method == 'POST':   #If form is being submitted
		organization = Organization.objects.get(id=dbID)
		name = organization.name
		organization.delete()
		LogEntry.objects.log_action(
							user_id = request.user.id or 0,
							content_type_id = 3,
							object_id = organization.id,
							object_repr=organization.name,
							change_message = 'Deleted Organization from database',
							action_flag = 3
						   )
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
	if not request.user.has_perm('vrcAPP.Data_Validation'):
		for field in form.fields:
			if form.fields[field].widget.__class__.__name__ == CheckboxInput().__class__.__name__:
				if field not in ['idCheck', 'dataValidation', 'interview', 'safety', 'idbadge', 'maps']:
					form.fields[field].widget.attrs['disabled'] = True
			elif field not in ['job','notes']:
				form.fields[field].widget.attrs['disabled'] = True
				form.fields[field].widget.attrs['readonly'] = True
			
	if request.method == 'POST':   #If form is being submitted
		form.is_valid()
		if(request.user.has_perm('vrcAPP.IDCheck')):
			volunteer.save(update_fields=['idCheck', 'notes'])
			LogEntry.objects.log_action(
							user_id = request.user.id or 0,
							content_type_id = 1,
							object_id = volunteer.id,
							object_repr=volunteer.name,
							change_message = 'Updated ID Check Station for Volunteer',
							action_flag = 2
						   )
		if(request.user.has_perm('vrcAPP.Data_Validation')):
			fieldList = [field.name for field in form]
			for thing in ['idCheck', 'interview', 'safety', 'idbadge', 'maps','job']:
				if thing in fieldList: fieldList.remove(thing)
			volunteer.save(update_fields=fieldList)
			LogEntry.objects.log_action(
							user_id = request.user.id or 0,
							content_type_id = 1,
							object_id = volunteer.id,
							object_repr=volunteer.name,
							change_message = 'Updated Volunteer at Data Validation Station',
							action_flag = 2
						   )
		if(request.user.has_perm('vrcAPP.Interview')):
			volunteer.save(update_fields=['job','interview', 'notes'])
			LogEntry.objects.log_action(
							user_id = request.user.id or 0,
							content_type_id = 1,
							object_id = volunteer.id,
							object_repr=volunteer.name,
							change_message = 'Updated Interview Station and job for Volunteer',
							action_flag = 2
						   )
		if(request.user.has_perm('vrcAPP.Safety')):
			volunteer.save(update_fields=['safety', 'notes'])
			LogEntry.objects.log_action(
							user_id = request.user.id or 0,
							content_type_id = 1,
							object_id = volunteer.id,
							object_repr=volunteer.name,
							change_message = 'Updated Safety Station for Volunteer',
							action_flag = 2
						   )
		if(request.user.has_perm('vrcAPP.IDBadge')):
			volunteer.save(update_fields=['idbadge', 'notes'])
			LogEntry.objects.log_action(
							user_id = request.user.id or 0,
							content_type_id = 1,
							object_id = volunteer.id,
							object_repr=volunteer.name,
							change_message = 'Updated ID Badge Station for Volunteer',
							action_flag = 2
						   )
		if(request.user.has_perm('vrcAPP.Maps')):
			volunteer.save(update_fields=['maps', 'notes'])
			LogEntry.objects.log_action(
							user_id = request.user.id or 0,
							content_type_id = 1,
							object_id = volunteer.id,
							object_repr=volunteer.name,
							change_message = 'Updated Maps Station for Volunteer',
							action_flag = 2
						   )
		return viewVolunteer(request,dbID)
	else:
		return render(request, 'stations.html', {'volunteer':volunteer, 'form': form})
	
def help(request):
	return render(request, 'help.html')
	
#from registration.backends.simple.views import RegistrationView

#class MyRegistrationView(RegistrationView):
#	def get_success_url(self, request, user):
#		return "/"
		
def runCleanup():
	start = datetime.datetime.now()
	volunteers = Volunteer.objects.all()
	jobs = Job.objects.all()
	currentTime = datetime.datetime.now()
	currentTime = currentTime.replace(tzinfo=None)
	for volunteer in volunteers:
		naive = volunteer.created.replace(tzinfo=None)
		if (currentTime - naive).days >=1 and not (volunteer.dataValidation):
			#print('Deleting ' + volunteer.name) 
			#volunteer.delete()
			pass
	for job in jobs:
		debug1 = datetime.datetime.now().date()
		debug2 = job.edate
		initialFull = job.full
		if job.volunteer_set.count() >= job.number:
			job.full = True
			reason = 'Request Fulfilled'
			job.reasonClosed = 0
			job.closedOn = datetime.datetime.now()
		elif job.edate is not None:
			if job.edate < datetime.datetime.now().date():
				job.full = True
				reason = 'Expired'
				job.reasonClosed = 1
				job.closedOn = datetime.datetime.now()
			else:
				job.full = False
				reason = 'No Longer Full'
				job.reasonClosed = None
		else:
			job.full = False
			reason = 'No Longer Full'
			job.reasonClosed = None
		if job.full != initialFull:
			job.save(update_fields=['full','reasonClosed'])
			LogEntry.objects.log_action(
							user_id = 255,
							content_type_id = 2,
							object_id = job.id,
							object_repr=job.title,
							change_message = 'Automatically changed status of job for reason: ' + reason,
							action_flag = 2,
						   )
			print('CLEANUP - CHANGED STATUS OF JOB: ' + job.title + '. Reason: ' + reason)


def serializeAll():
	vols = serializers.serialize("json", Volunteer.objects.all())
	jobs = serializers.serialize("json", Job.objects.all())
	orgs = serializers.serialize("json", Organization.objects.all())
	return (vols + jobs + orgs)

def sendToBackup(s, serialized):
	s.send(serialized)
	response = s.recv(64)
	s.close()
	return response

def connectToBackupDatabase(ip,port):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((ip,port))
	except:
		s = None
	return s


def export(request):
	if request.method == 'POST':
		string = serializeAll()
		s = connectToBackupDatabase(request.POST.get('ip'),int(request.POST.get('port')))
		if s:
			response = sendToBackup(s,string)
		else:
			response = 'failure'
		LogEntry.objects.log_action(
							user_id = request.user.id or 0,
							content_type_id = 0,
							object_id = 0,
							object_repr='Database',
							change_message = 'Attempted export of entire database. Result was a ' + response,
							action_flag = 0,
						   )
		return render(request, 'export.html', {'response':response})
	else:
		return render(request, 'export.html')

