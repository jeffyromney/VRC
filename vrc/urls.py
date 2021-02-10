from django.conf.urls import include, url, static
from vrc import views
from utils import views
from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.views import LoginView, LogoutView
import vrc.settings

urlpatterns = [
    # Examples:
    url(r'^$', 'vrc.views.welcome', name='Welcome to VRC'),
    url(r'^addVolunteer/$', 'vrc.views.addVolunteer', name='Add Volunteer'),
    url(r'^addOrganization/$', 'vrc.views.addOrganization', name='Add Organization'),
    url(r'^addJob/$', 'vrc.views.addJob', name='Add Job'),
    url(r'^search/$', 'vrc.views.search', name='Search'),
    url(r'^help/$', 'vrc.views.help', name='VRC-Help'),
    url(r'^export/$', 'vrc.views.export', name='Data Export'),
    
    url(r'^Volunteer/view/(\d{1,2})/$', 'vrc.views.viewVolunteer', name='View Volunteer'),
    url(r'^Volunteer/viewNew/(\d{1,2})/$', 'vrc.views.viewNewVolunteer', name='Volunteer Added'),
    url(r'^Volunteer/modify/(\d{1,2})/$', 'vrc.views.modifyVolunteer', name='Modify Volunteer'),
    url(r'^Volunteer/delete/(\d{1,2})/$', 'vrc.views.deleteVolunteer', name='Delete Volunteer'),
    url(r'^Volunteer/print/(\d{1,2})/$', 'vrc.views.printVolunteer', name='Print Volunteer'),
    
    url(r'^Job/view/(\d{1,2})/$', 'vrc.views.viewJob', name='View Job'),
    url(r'^Job/viewNew/(\d{1,2})/$', 'vrc.views.viewNewJob', name='Job Added'),
    url(r'^Job/modify/(\d{1,2})/$', 'vrc.views.modifyJob', name='Modify Job'),
    url(r'^Job/delete/(\d{1,2})/$', 'vrc.views.deleteJob', name='Delete Job'),
    url(r'^Job/print/(\d{1,2})/$', 'vrc.views.printJob', name='Print Job'),
    
    url(r'^Organization/view/(\d{1,2})/$', 'vrc.views.viewOrganization', name='View Organization'),
    url(r'^Organization/viewNew/(\d{1,2})/$', 'vrc.views.viewNewOrganization', name='Organization Added'),
    url(r'^Organization/modify/(\d{1,2})/$', 'vrc.views.modifyOrganization', name='Modify Organization'),
    url(r'^Organization/delete/(\d{1,2})/$', 'vrc.views.deleteOrganization', name='Delete Organization'),
    
    url(r'^Stations/(\d{1,2})/$', 'vrc.views.Stations', name='Stations'),
    url(r'^accounts/login/$',  LoginView),
    url(r'^accounts/logout/$', LogoutView, {'next_page': '/accounts/loggedOut/'}),
    url(r'^accounts/profile/$', 'vrc.views.loginSuccess'),
    url(r'^accounts/loggedOut/$', 'vrc.views.loggedOut'),

    url(r'^api/sync_vrc/$', 'utils.views.sync_vrc'),
    url(r'^api/sync_mobile/$', 'utils.views.sync_mobile'),
    url(r'^api/spoof/$', 'utils.views.spoofSync'),
#    url(r'^accounts/register/$', views.MyRegistrationView.as_view(), name='registration_register'),
#    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    
    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
#    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
