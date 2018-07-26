from django.db import models
from django.urls import reverse
from citizen.models import Citizen
from police.models import Ward
import datetime

t = datetime.datetime.now()
t = str(t.year) + '/' + str(t.month) + '/' + str(t.day)


def evidence_upload_location(instance,filename):
    return '%s/%s/%s' % ( t ,  instance.case.id, filename)

class CaseCategory(models.Model):
    name = models.CharField(max_length=80, blank=False)

    class Meta:
        verbose_name_plural = 'Crime Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("cbc",kwargs={"id":self.id})


class CyberCaseCategories(models.Model):
    name = models.CharField(max_length=80, blank=False)

    class Meta:
        verbose_name_plural = 'Cyber Crime Categories'

    def __str__(self):
        return self.name


class Evidence(models.Model):
    case = models.ForeignKey('Case', blank = True, null = True)
    evidence = models.FileField(upload_to=evidence_upload_location)
    timestamp = models.DateTimeField(auto_now_add=True)


class Witness(models.Model):
    name=models.CharField(max_length=100, blank=False)
    adhaar_id=models.CharField(max_length=20, blank=False)
    bahmashah_id=models.CharField(max_length=20, blank=True)
    contact=models.CharField(max_length=20, blank=False)
    case = models.ForeignKey('Case', null=True)
    def get_absolute_url(self):
        return reverse("person_detail",kwargs={"id":self.bahmashah_id})    


class Case(models.Model):
    title = models.CharField(max_length=80, blank=False)
    case_categories = models.ForeignKey(CaseCategory,null=True,blank=True)
    cyber_case_categories = models.ForeignKey(CyberCaseCategories,null=True,blank=True)
    description = models.TextField()
    reg_from_loc = models.CharField(max_length=255, blank=False)
    userid = models.ForeignKey(Citizen,null=True)
    ward_id = models.ForeignKey(Ward)
    incident_time = models.DateField()
    approved=models.NullBooleanField()
    solved=models.NullBooleanField()

    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        if self.approved==True:
            app=1
        else:
            app=0
        return reverse("case_detail",kwargs={"id":self.id,"approved":app})

    def get_absolute_url1(self):

        return reverse("user_case_detail",kwargs={"id":self.id})


#
# select_category = (
#     ('TAR', 'Theft and Robbery'),
#     ('B', 'Burglary'),
#     ('PR', 'Offence against Property'),
#     ('SO', 'Sexual offence'),
#     ('MVO', 'Motor vehicle offence'),
#     ('FD', 'Forced disappearance'),
#     ('P', 'Piracy'),
#     ('SS', 'Sexual slavery'),
#     ('CL', 'Child labour'),
#     ('DRC', 'Drug related case'),
#     ('K', 'Kidnapping'),
#     ('FI', 'False Imprisonment'),
#     ('MC', 'Murder Case'),
#     ('O', 'other'),
# )
