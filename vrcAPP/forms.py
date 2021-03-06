from django.forms import *
#from django.forms.extras.widgets import SelectDateWidget
from .models import *
from django.forms import CheckboxInput
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
import datetime


class VolunteerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields["job"].queryset = Job.objects.filter(full=False).order_by('id')
        self.fields['name'].required = True
        self.fields['waiver'].required = True
        #self.fields['vancap'].widget.attrs['required'] = False
        #self.fields['vancap'].widget.attrs['disabled'] = True
        #self.fields['vancap'].widget.attrs['placeholder'] = "Capacity & Type"
        rel = {'doctor':('dSpecialty','Specialty'),
                         'nurse':('nSpecialty','Specialty'),
                         'satphone':('satnum','Phone #'),
                         'otherLang':('lang','Language'),
                         'dataEntry':('software','Software'),
                         'functional':('fneeds','Description'),
                         'van':('vancap','Capacity & Type'),
                         'boat':('btype','Capacity & Type'),
                         'rv':('rvtype','Capacity & Type'),
                         'cdl':('cdlnum','Class and License'),
                         'operate':('eqtype','Types'),
                         'truck':('tdescription','Description'),
                         'truck':('tdescription','Description'),
                        }
        
        for field in rel:
            self.fields[field].widget.attrs['onclick'] = "document.getElementById('id_" + rel[field][0] + "').disabled = !this.checked"
            self.fields[rel[field][0]].widget.attrs['disabled'] = True
            self.fields[rel[field][0]].widget.attrs['placeholder'] = rel[field][1]


    birthday = DateField(required=False, widget=SelectDateWidget(years=range(datetime.date.today().year,1900,-1)))
    job = ModelChoiceField(queryset=Job.objects.none(), to_field_name="title", required=False)
    distance = IntegerField(widget=NumberInput(attrs={'type':'range', 'step': '10', 'min': '5', 'max':'2000'}))
    class Meta:
        model = Volunteer
        fields = '__all__'
        exclude = ['picture']
        required = {'name':True}
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
    sdate = DateField(required=False, initial=datetime.date.today, widget=SelectDateWidget(years=range(datetime.date.today().year+2,datetime.date.today().year-2,-1)))
    edate = DateField(required=False, initial=datetime.date.today, widget=SelectDateWidget(years=range(datetime.date.today().year+2,datetime.date.today().year-2,-1)))
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
