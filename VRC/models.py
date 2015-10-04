from django.db import models

# Create your models here.
    
class Organization(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)

class Job(models.Model):
    title = models.CharField(max_length=40)
    organization = models.ForeignKey(Organization)
    description = models.CharField(max_length = 500)

class Volunteer(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    email = models.EmailField()
    birthday = models.DateField()
    job = models.ForeignKey(Job,blank=True, null=True)
