from django.db import models
#from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator

# Create your models here.
    
class Organization(models.Model):
    name = models.CharField(blank=True, null=True, max_length=50)
    contact = models.CharField(blank=True, null=True, max_length=40)
    address = models.CharField(blank=True, null=True, max_length=80)
    phone = models.CharField(blank=True, null=True, max_length=18, validators=[RegexValidator(r'^(\+?\d{1,2}[\s.,-\/\\*]?)?\(?\d{3}\)?[\s.,-\/\\*]?\d{3}[\s.,-\/\\*]?\d{4}$','Enter a valid Phone Number','Invalid Phone Number')], )
    ext = models.IntegerField(blank=True, null=True, max_length=3)
    
    def __unicode__(self):
        return self.name

class Job(models.Model):
    title = models.CharField(max_length=40)
    tdate = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    sdate = models.DateField(blank=True, null=True, )
    edate = models.DateField(blank=True, null=True, )
    event =  models.CharField(blank=True, null=True, max_length=50)
    agency = models.ForeignKey(Organization, blank=True, null=True)
    duties = models.CharField(blank=True, null=True, max_length=500)
    weight = models.IntegerField(blank=True, null=True, )
    drive = models.BooleanField(blank=True)
    number = models.IntegerField(blank=True, null=True, )
    whenneeded = models.CharField(blank=True, null=True, max_length=80)
    age = models.IntegerField(blank=True, null=True, max_length=2)
    skills = models.CharField(blank=True, null=True, max_length=200)
    other = models.CharField(blank=True, null=True, max_length=500)
    reasonClosed = models.IntegerField(blank=True,null=True)
    full = models.BooleanField(default=False)
    closedOn = models.DateTimeField(blank=True,null=True)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        permissions = (
            ("Phone_Bank", "Phone_Bank"),
        )
    
#    agencies (tdate, sdate, edate, event, agency, title, contact, address, phone, ext, duties, weight, drive, number, whenNeeded, age, skills, other)

class Volunteer(models.Model):
    name = models.CharField(blank=True, null=True, max_length=30, verbose_name="Name")
    address = models.CharField(blank=True, null=True, max_length=50, verbose_name="Street Address")
    city = models.CharField(blank=True, null=True, max_length=60, verbose_name="City")
    state_province = models.CharField(blank=True, null=True, max_length=30, verbose_name="State or Province")
    zip_code = models.CharField(blank=True, null=True, max_length=5, verbose_name="ZIP Code")
    country = models.CharField(blank=True, null=True, max_length=50, verbose_name="Country")
    email = models.EmailField(blank=True, null=True, verbose_name="Email Address")
    birthday = models.DateField(blank=True, null=True, verbose_name="Birth Date")
    job = models.ForeignKey(Job,blank=True, null=True, verbose_name="Assigned Job")
    dayPhone = models.CharField(blank=True, null=True, max_length=18, validators=[RegexValidator(r'^(\+?\d{1,2}[\s.,-\/\\*]?)?\(?\d{3}\)?[\s.,-\/\\*]?\d{3}[\s.,-\/\\*]?\d{4}$','Enter a valid Phone Number','Invalid Phone Number')], )
    cellPhone = models.CharField(blank=True, null=True, max_length=18, validators=[RegexValidator(r'^(\+?\d{1,2}[\s.,-\/\\*]?)?\(?\d{3}\)?[\s.,-\/\\*]?\d{3}[\s.,-\/\\*]?\d{4}$','Enter a valid Phone Number','Invalid Phone Number')], )
    emergencyContact =  models.CharField(blank=True, null=True, max_length=30, verbose_name="Emergency Contact")
    relationship =  models.CharField(blank=True, null=True, max_length=30, verbose_name="Relationship")
    emergencyPhone = models.CharField(blank=True, null=True, max_length=18, validators=[RegexValidator(r'^(\+?\d{1,2}[\s.,-\/\\*]?)?\(?\d{3}\)?[\s.,-\/\\*]?\d{3}[\s.,-\/\\*]?\d{4}$','Enter a valid Phone Number','Invalid Phone Number')], )
    occupation = models.CharField(blank=True, null=True, max_length=30, verbose_name="Occupation")
    employer = models.CharField(blank=True, null=True, max_length=30, verbose_name="Employer")
    resident = models.BooleanField(blank=True, verbose_name="Year-round Resident")
    monthsAvailable = models.CharField(blank=True, null=True, max_length=50, verbose_name="Months Available")
    limitations = models.CharField(blank=True, null=True, max_length=30, verbose_name="Limitations")
    distance = models.PositiveIntegerField(blank=True, null=True, verbose_name="Distance willing to travel (miles)")
    county = models.BooleanField(blank=True, verbose_name="This County")
    neighbor = models.BooleanField(blank=True, verbose_name="A Neighboring County")
    instate = models.BooleanField(blank=True, verbose_name="Anywhere in the State")
    us = models.BooleanField(blank=True, verbose_name="Anywhere in the US")
    affiliatedAgency = models.CharField(blank=True, null=True, max_length=30, verbose_name="Affiliated Agency")
    skillsTraining = models.CharField(blank=True, null=True, max_length=250, verbose_name="Special Skills and/or Disaster Training")
    doctor = models.BooleanField(blank=True, verbose_name="Doctor")
    dSpecialty = models.CharField(blank=True, null=True, max_length=30, verbose_name="Specialty")
    nurse = models.BooleanField(blank=True, verbose_name="Nurse")
    nSpecialty = models.CharField(blank=True, null=True, max_length=30, verbose_name="Specialty")
    emt = models.BooleanField(blank=True, verbose_name="Emergency Medical Cert.")
    mental = models.BooleanField(blank=True, verbose_name="Mental Health Counseling")
    vet = models.BooleanField(blank=True, verbose_name="Vetrinarian")
    vetTech = models.BooleanField(blank=True, verbose_name="Vetrinary Technician")
    cbHam = models.BooleanField(blank=True, verbose_name="CB/ham Operator")
    hotline = models.BooleanField(blank=True, verbose_name="Hotline Operator")
#    cphone = models.BooleanField(blank=True, verbose_name="")
    satphone = models.BooleanField(blank=True, verbose_name="Satellite Phone")
    satnum = models.CharField(blank=True, null=True, max_length=30, verbose_name="#")
    publicRelations = models.BooleanField(blank=True, verbose_name="Public Relations")
    webpage = models.BooleanField(blank=True, verbose_name="Web Page Design")
    publicSpeaker = models.BooleanField(blank=True, verbose_name="Public Speaker")
    french = models.BooleanField(blank=True, verbose_name="French")
    german = models.BooleanField(blank=True, verbose_name="German")
    italian = models.BooleanField(blank=True, verbose_name="Italian")
    spanish = models.BooleanField(blank=True, verbose_name="Spanish")
    russian = models.BooleanField(blank=True, verbose_name="Russian")
    creole = models.BooleanField(blank=True, verbose_name="Creole")
    otherLang = models.BooleanField(blank=True, verbose_name="Other")
    lang = models.CharField(blank=True, null=True, max_length=30, verbose_name="Languages")
    clerical = models.BooleanField(blank=True, verbose_name="Clerical-filing, copying")
    dataEntry = models.BooleanField(blank=True, verbose_name="Data Entry")
    software = models.CharField(blank=True, null=True, max_length=30, verbose_name="Software")
    receptionist = models.BooleanField(blank=True, verbose_name="Phone Receptionist")
    food = models.BooleanField(blank=True, verbose_name="Food")
    elderly = models.BooleanField(blank=True, verbose_name="Assistance to elderly")
    childCare = models.BooleanField(blank=True, verbose_name="Child Care")
    spiritual = models.BooleanField(blank=True, verbose_name="Spiritual Counseling")
    social = models.BooleanField(blank=True, verbose_name="Social Work")
    searchRescue = models.BooleanField(blank=True, verbose_name="Search and Rescue")
    autoRepair = models.BooleanField(blank=True, verbose_name="Auto repair/towing")
    traffic = models.BooleanField(blank=True, verbose_name="Traffic Control")
    crimeWatch = models.BooleanField(blank=True, verbose_name="Crime watch")
    animalRescue = models.BooleanField(blank=True, verbose_name="Animal Rescue")
    animalCare = models.BooleanField(blank=True, verbose_name="Animal Care")
    runner = models.BooleanField(blank=True, verbose_name="Runner")
    functional = models.BooleanField(blank=True, verbose_name="Functional needs support")
    fneeds = models.CharField(blank=True, null=True, max_length=30, verbose_name="")
    damage = models.BooleanField(blank=True, verbose_name="Damage Assesment")
    metal = models.BooleanField(blank=True, verbose_name="Metal Construction")
    wood = models.BooleanField(blank=True, verbose_name="Wood Construction")
    block = models.BooleanField(blank=True, verbose_name="Block Construction")
    plumbing = models.BooleanField(blank=True, verbose_name="Plumbing")
    electric = models.BooleanField(blank=True, verbose_name="Electrical")
    roofing = models.BooleanField(blank=True, verbose_name="Roofing")
    car = models.BooleanField(blank=True, verbose_name="Car")
    minivan = models.BooleanField(blank=True, verbose_name="Minivan")
    van = models.BooleanField(blank=True, verbose_name="Maxi-van")
    vancap = models.IntegerField(blank=True, null=True, verbose_name="Capacity")
    atv = models.BooleanField(blank=True, verbose_name="ATV")
    offRoad = models.BooleanField(blank=True, verbose_name="Own off-road veh/4WD")
    truck = models.BooleanField(blank=True, verbose_name="Own Truck")
    tdescription = models.CharField(blank=True, null=True, max_length=100, verbose_name="Description")
    boat = models.BooleanField(blank=True, verbose_name="Own Boat")
    btype = models.CharField(blank=True, null=True, max_length=30, verbose_name="Capacity & Type")
    cdl = models.BooleanField(blank=True, verbose_name="Commercial Driver License")
    cdlnum = models.CharField(blank=True, null=True, max_length=30, verbose_name="Class & Number")
    rv = models.BooleanField(blank=True, verbose_name="Camper/RV")
    rvtype = models.CharField(blank=True, null=True, max_length=30, verbose_name="Capacity & Type")
    wheelchair = models.BooleanField(blank=True, verbose_name="Wheelchair Transport")
    loading = models.BooleanField(blank=True, verbose_name="Loading/Shipping")
    sorting = models.BooleanField(blank=True, verbose_name="Sorting/Packing")
    cleanup = models.BooleanField(blank=True, verbose_name="Cleanup")
    operate = models.BooleanField(blank=True, verbose_name=" Operate Equipment")
    eqtype = models.CharField(blank=True, null=True, max_length=30, verbose_name="Types")
    supervising = models.BooleanField(blank=True, verbose_name="Have Experience Supervising Others")
    chainsaw = models.BooleanField(blank=True, verbose_name="Chainsaw")
    backhoe = models.BooleanField(blank=True, verbose_name="Backhoe")
    generator = models.BooleanField(blank=True, verbose_name="Generator")
    othereq = models.CharField(blank=True, null=True, max_length=30, verbose_name="Other")
#    cnum = models.CharField(blank=True, null=True, max_length=30, verbose_name="Cell Phone Number")
#    equipment = models.CharField(blank=True, null=True, max_length=30, verbose_name="Equipment")
    notes = models.TextField(blank=True, null=True, max_length=350, verbose_name="Notes")
    waiver = models.BooleanField(blank=True, verbose_name="Waiver Signed")
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    idCheck = models.BooleanField(blank=True, verbose_name="ID Check Station")
    dataValidation = models.BooleanField(blank=True, verbose_name="Data Check Station")
    interview = models.BooleanField(blank=True, verbose_name="Interview Station")
    safety = models.BooleanField(blank=True, verbose_name="Safety Station")
    idbadge = models.BooleanField(blank=True, verbose_name="ID Station")
    maps = models.BooleanField(blank=True, verbose_name="Map Station")
    picture = models.ImageField(upload_to='volunteers')
    
    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ("View_data", "Can search and view user's data"),
            ("Safety", "Safety Station"),
            ("IDBadge", "ID Badge station"),
            ("IDCheck", "ID Check station"),
            ("Data_Validation", "Validation station"),
            ("Interview", "Interview station"),
            ("Maps", "Maps station"),
        )
    
    
#    volunteers (name,bday, dayPhone, email, cellPhone, street, city, state, ZIP, emergencyContact, relationship, emergencyPhone, occupation, employer, resident, monthsAvail, limitations, county, neighbor, instate, us, affiliatedAgency, skillsTraining,doctor, nurse, emt, vet, vettech, cbham, hotline, cphone, satphone, publicRelations, webPage, publicSpeaker, french, german, italian, spanish, russian, creole, otherLang, clerical, dataEntry, receptionist, food, elderly, childCare, spiritual, social, searchRescue, autoRepair, traffic, crimeWatch, animalRescue, animalCare, runner, functional, damage, metal, wood, block, plumbing, electric, roofing, car, minivan, van, atv, offRoad, truck, boat, cdl, rv, wheelchair, loading, sorting, cleanup, operate, supervising, chainsaw, backhoe, generator, othereq, dSpecialty, nSpecialty, cnum, satnum, lang, software, fneeds, vancap, tdescription, btype, cdlnum, rvtype, eqtype, equipment, notes, waiver,created)
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
