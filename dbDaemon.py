from VRC.models import *
from django.db.models import Count
import time

while True:
    volunteers = Volunteer.objects.all()
    jobs = Job.objects.all()
    for volunteer in volunteers:
        if False:
            pass
            #volunteer.delete()
    for job in jobs:
        if job.volunteer_set.count() >= job.number:
            job.full = True
        else:
            job.full = False
        job.save(update_fields=['full'])
    time.sleep(1)