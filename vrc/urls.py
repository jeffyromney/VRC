from django.conf.urls import patterns, include, url
from vrc import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'vrc.views.welcome', name='welcome'),
    url(r'^addVolunteer/$', 'vrc.views.addVolunteer', name='addVolunteer'),
    url(r'^addOrganization/$', 'vrc.views.addOrganization', name='addOrganization'),
    url(r'^addJob/$', 'vrc.views.addJob', name='addJob'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
