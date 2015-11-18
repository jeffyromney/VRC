from django.forms import *
from django.forms.extras.widgets import SelectDateWidget
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
        self.fields['vancap'].widget.attrs['required'] = False
        self.fields['vancap'].widget.attrs['disabled'] = True
        self.fields['vancap'].widget.attrs['placeholder'] = "Capacity & Type"


    birthday = DateField(required=False, widget=SelectDateWidget(years=range(datetime.date.today().year,1900,-1)))
    job = ModelChoiceField(queryset=Job.objects.none(), to_field_name="title", required=False)#queryset=Job.objects.filter(full=False).order_by('id'), 
    doctor = BooleanField(required=False, widget = CheckboxInput(attrs = {'onclick' : "document.getElementById('id_dSpecialty').disabled = !this.checked"}))
    dSpecialty = CharField(required=False, widget = TextInput(attrs = {'disabled' : "True", 'placeholder' : "Specialty"}))
    nurse = BooleanField(required=False, widget = CheckboxInput(attrs = {'onclick' : "document.getElementById('id_nSpecialty').disabled = !this.checked"}))
    nSpecialty = CharField(required=False, widget = TextInput(attrs = {'disabled' : "True", 'placeholder' : "Specialty"}))
    satphone = BooleanField(required=False, widget = CheckboxInput(attrs = {'onclick' : "document.getElementById('id_satnum').disabled = !this.checked"}))
    satnum = CharField(required=False, widget = TextInput(attrs = {'disabled' : "True", 'placeholder' : "Phone #"}))
    otherLang = BooleanField(required=False, widget = CheckboxInput(attrs = {'onclick' : "document.getElementById('id_lang').disabled = !this.checked"}))
    lang = CharField(required=False, widget = TextInput(attrs = {'disabled' : "True", 'placeholder' : "Language"}))
    dataEntry = BooleanField(required=False, widget = CheckboxInput(attrs = {'onclick' : "document.getElementById('id_software').disabled = !this.checked"}))
    software = CharField(required=False, widget = TextInput(attrs = {'disabled' : "True", 'placeholder' : "Software"}))
    functional = BooleanField(required=False, widget = CheckboxInput(attrs = {'onclick' : "document.getElementById('id_fneeds').disabled = !this.checked"}))
    fneeds = CharField(required=False, widget = TextInput(attrs = {'disabled' : "True", 'placeholder' : "Description"}))
    truck = BooleanField(required=False, widget = CheckboxInput(attrs = {'onclick' : "document.getElementById('id_tdescription').disabled = !this.checked"}))
    tdescription = CharField(required=False, widget = TextInput(attrs = {'disabled' : "True", 'placeholder' : "Description"}))
    van = BooleanField(required=False, widget = CheckboxInput(attrs = {'onclick' : "document.getElementById('id_vancap').disabled = !this.checked"}))
#    vancap = CharField(required=False, widget = NumberInput(attrs = {'disabled' : "True", 'placeholder' : "Capacity & Type"}))
    boat = BooleanField(required=False, widget = CheckboxInput(attrs = {'onclick' : "document.getElementById('id_btype').disabled = !this.checked"}))
    btype = CharField(required=False, widget = TextInput(attrs = {'disabled' : "True", 'placeholder' : "Capacity & Type"}))
    rv = BooleanField(required=False, widget = CheckboxInput(attrs = {'onclick' : "document.getElementById('id_rvtype').disabled = !this.checked"}))
    rvtype = CharField(required=False, widget = TextInput(attrs = {'disabled' : "True", 'placeholder' : "Capacity & Type"}))
    cdl = BooleanField(required=False, widget = CheckboxInput(attrs = {'onclick' : "document.getElementById('id_cdlnum').disabled = !this.checked"}))
    cdlnum = CharField(required=False, widget = TextInput(attrs = {'disabled' : "True", 'placeholder' : "Class and License "}))
    operate = BooleanField(required=False, widget = CheckboxInput(attrs = {'onclick' : "document.getElementById('id_eqtype').disabled = !this.checked"}))
#    eqtype = CharField(required=False, widget = TextInput(attrs = {'disabled' : "True", 'placeholder' : "Types"}))
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
