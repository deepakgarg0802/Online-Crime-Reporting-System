from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import datetime

t = datetime.datetime.now()
t = str(t.year) + '/' + str(t.month) + '/' + str(t.day)


def evidence_upload_location(instance,filename):
    return 'anonymous/%s/%s/%s' % ( t ,  instance.anonymous_tip.id, filename)

class AnonymousUser(User):
    pass

    class Meta:
        verbose_name = 'Anonymous User'

    def __str__(self):
        return self.username


class AnonymousTip(models.Model):
    title = models.CharField(max_length=80, blank=False)
    description = models.TextField()
    userid = models.ForeignKey(AnonymousUser,null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    incident_time = models.DateField()
    updated = models.DateTimeField(auto_now=True)
    upload_evidence = models.BooleanField(blank = True)
    stay_in_touch = models.BooleanField(blank = True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
    
        return reverse("atip_detail",kwargs={"id":self.id})
    

class Evidence(models.Model):
        image1 = models.ImageField(upload_to=evidence_upload_location, blank = True)
        image2 =  models.ImageField(upload_to=evidence_upload_location, blank = True)
        doc =  models.FileField(upload_to=evidence_upload_location, blank = True)
        video =  models.FileField(upload_to=evidence_upload_location, blank = True)
        anonymous_tip = models.ForeignKey(AnonymousTip,null=True,blank=True)

        def __str__(self):
            return str(self.id)
