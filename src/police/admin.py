from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django import forms
from .models import *
from django.db import models



class PoliceForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Police
        fields = '__all__'



class PoliceAdmin(admin.ModelAdmin):
    form = PoliceForm

    class Meta:
        model = Police


class CaseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
admin.site.register(Police,PoliceAdmin)
admin.site.register(Ward)
admin.site.register(Contact)
admin.site.register(Criminal)