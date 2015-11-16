#from VRC.models import *
from django.db.models import Count
import time

while True:
    volunteers = Volunteer.objects.all()
    jobs = Job.objects.all()
    for volunteer in volunteers:
        if False:
            print(volunteer)
            #volunteer.delete()
    for job in jobs:
        num_assigned = job.volunteer_set.count()
        #job.annotate(num_assigned=Count('volunteer'))
        print(num_assigned)
        if job.volunteer_set.count() >= job.number:
            job.full = True
            print('full')
        else:
            job.full = False
            print('Not Full')
        job.save(update_fields=['full'])
        print(job)
    time.sleep(1)
