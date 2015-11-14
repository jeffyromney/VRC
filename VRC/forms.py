from django.forms import ModelForm, ModelChoiceField
from .models import *


class VolunteerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields["job"].queryset = Job.objects.filter(full=False).order_by('id')
    job = ModelChoiceField(queryset=Job.objects.none(), to_field_name="title", required=False)#queryset=Job.objects.filter(full=False).order_by('id'), 
    class Meta:
        model = Volunteer
        fields = '__all__'
        
class OrganizationForm(ModelForm):
    agency = ModelChoiceField(queryset=Organization.objects.all().order_by('id'), to_field_name="name")
    class Meta:
        model = Organization
        fields = '__all__'
        
class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
