from django.http import HttpResponse
from django.template import Template, Context, RequestContext
from django.template.loader import get_template
from django.shortcuts import render
from VRC.forms import *
from django.contrib.auth.decorators import permission_required


@permission_required('VRC.add_volunteer')
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
        return render(request, 'add.html', {'form': form, 'type': "Volunteer"})


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
        return render(request, 'add.html', {'form': form, 'type': "Organization"})

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

#@permission_required('VRC.change_volunteer')
def loginSuccess(request):
    permissions = request.user.get_all_permissions()
    return render(request, 'registration/success.html', {'permissions':permissions})


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



@permission_required('VRC.change_volunteer')
def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        entry_query = get_query(query_string, ['name', 'id','cellPhone', 'dayPhone'])
        
        found_entries = Volunteer.objects.filter(entry_query).order_by('name')

    return render(request,'search.html',
                          { 'query': query_string, 'results': found_entries },
                          context_instance=RequestContext(request))


    
def view(request,dbID):
    volunteer = Volunteer.objects.filter(get_query(dbID, ['id'])).order_by('name')
    volunteer = volunteer.values()
    return render(request, 'view.html', {'volunteer': volunteer})
    
    
    
    
    

