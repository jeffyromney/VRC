from django.conf.urls import patterns, include, url
from vrc import views
from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'vrc.views.welcome', name='welcome'),
    url(r'^addVolunteer/$', 'vrc.views.addVolunteer', name='addVolunteer'),
    url(r'^addOrganization/$', 'vrc.views.addOrganization', name='addOrganization'),
    url(r'^addJob/$', 'vrc.views.addJob', name='addJob'),
    url(r'^search/$', 'vrc.views.search', name='Search'),
    
    url(r'^Volunteer/view/(\d{1,2})/$', 'vrc.views.viewVolunteer', name='View Volunteer'),
    url(r'^Volunteer/viewNew/(\d{1,2})/$', 'vrc.views.viewNewVolunteer', name='Volunteer Added'),
    url(r'^Volunteer/modify/(\d{1,2})/$', 'vrc.views.modifyVolunteer', name='Modify Volunteer'),
    url(r'^Volunteer/delete/(\d{1,2})/$', 'vrc.views.deleteVolunteer', name='Delete Volunteer'),
    
    url(r'^Job/view/(\d{1,2})/$', 'vrc.views.viewJob', name='View Job'),
    url(r'^Job/viewNew/(\d{1,2})/$', 'vrc.views.viewNewJob', name='Job Added'),
    url(r'^Job/modify/(\d{1,2})/$', 'vrc.views.modifyJob', name='Modify Job'),
    url(r'^Job/delete/(\d{1,2})/$', 'vrc.views.deleteJob', name='Delete Job'),
    
    url(r'^Organization/view/(\d{1,2})/$', 'vrc.views.viewOrganization', name='View Organization'),
    url(r'^Organization/viewNew/(\d{1,2})/$', 'vrc.views.viewNewOrganization', name='Organization Added'),
    url(r'^Organization/modify/(\d{1,2})/$', 'vrc.views.modifyOrganization', name='Modify Organization'),
    url(r'^Organization/delete/(\d{1,2})/$', 'vrc.views.deleteOrganization', name='Delete Organization'),
    
    url(r'^StationsCheck/(\d{1,2})/$', 'vrc.views.StationsCheck', name='StationsCheck'),
    url(r'^accounts/login/$',  login),
    url(r'^accounts/logout/$', logout, {'next_page': '/accounts/loggedOut/'}),
    url(r'^accounts/profile/$', 'vrc.views.loginSuccess'),
    url(r'^accounts/loggedOut/$', 'vrc.views.loggedOut'),
    url(r'^admin/', include(admin.site.urls)),
)
