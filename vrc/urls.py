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
    url(r'^Volunteer/view/(\d{1,2})/$', 'vrc.views.view', name='View Volunteer'),
    url(r'^Volunteer/modify/(\d{1,2})/$', 'vrc.views.modify', name='Modify Volunteer'),
    url(r'^Volunteer/delete/(\d{1,2})/$', 'vrc.views.delete', name='Delete Volunteer'),
    url(r'^accounts/login/$',  login),
    url(r'^accounts/logout/$', logout),
    url(r'^accounts/profile/$', 'vrc.views.loginSuccess'),
    url(r'^admin/', include(admin.site.urls)),
)
