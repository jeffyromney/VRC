from django.forms import ModelForm
from .models import *


class VolunteerForm(ModelForm):
    class Meta:
        model = Volunteer
        fields = '__all__'
        
class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'
        
class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
