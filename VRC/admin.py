from django.contrib import admin
from .models import *
# Register your models here.

class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    pass
class JobAdmin(admin.ModelAdmin):
    list_display = ('title',)
    pass
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    pass

admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Organization, OrganizationAdmin)

