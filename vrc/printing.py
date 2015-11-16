from VRC.models import *

def printVolunteer(ID):
    volunteer = Volunteer.objects.get(id=ID)
    print(volunteer)
    print(volunteer.job)
    print(volunteer.job.agency.contact)
    return(1)




def printJob(ID):
    return(1)
