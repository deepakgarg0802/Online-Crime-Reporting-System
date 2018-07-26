from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Citizen(User):
    contact = models.CharField(max_length=11)
    aadhaar  = models.CharField(max_length=12,null=True,blank=True)
    bhamashah = models.CharField(max_length=12,null=True,blank=True)
    birth_date = models.DateField(null = True)

    class Meta:
        verbose_name = 'Citizen'

    def __str__(self):
        return self.username


    def get_absolute_url(self):
        return reverse("person_detail",kwargs={"id":self.bhamashah})

