from django.forms import ModelForm, ModelChoiceField
from .models import *
from django.forms import CheckboxInput
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


class VolunteerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields["job"].queryset = Job.objects.filter(full=False).order_by('id')
    job = ModelChoiceField(queryset=Job.objects.none(), to_field_name="title", required=False)#queryset=Job.objects.filter(full=False).order_by('id'), 
    class Meta:
        model = Volunteer
        fields = '__all__'
        exclude = ['picture']
    def disabled(_self):
        form = _self
        for field in form.fields:
            if form.fields[field].widget.__class__.__name__ == CheckboxInput().__class__.__name__:
                form.fields[field].widget.attrs['disabled'] = True
            else:
                form.fields[field].widget.attrs['readonly'] = True
                form.fields[field].widget.attrs['disabled'] = True
        return form
        
class OrganizationForm(ModelForm):
    #agency = ModelChoiceField(queryset=Organization.objects.all().order_by('id'), to_field_name="name")
    class Meta:
        model = Organization
        #fields = '__all__'
        exclude = ['agency']
    def disabled(_self):
        form = _self
#        form.fields['agency'].widget.attrs['readonly'] = True
        for field in form.fields:
            if form.fields[field].widget.__class__.__name__ == CheckboxInput().__class__.__name__:
                form.fields[field].widget.attrs['disabled'] = True
            else:
                form.fields[field].widget.attrs['readonly'] = True
                form.fields[field].widget.attrs['disabled'] = True
        return form
        
class JobForm(ModelForm):
    class Meta:
        model = Job
        #fields = '__all__'
        exclude = ['full']
    def disabled(_self):
        form = _self
        for field in form.fields:
            if form.fields[field].widget.__class__.__name__ == CheckboxInput().__class__.__name__:
                form.fields[field].widget.attrs['disabled'] = True
            else:
                form.fields[field].widget.attrs['readonly'] = True
                form.fields[field].widget.attrs['disabled'] = True
        return form


#class UserForm(UserChangeForm):
