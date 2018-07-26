from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models

from .models import Case, CaseCategory, CyberCaseCategories, Evidence,Witness


class CaseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
admin.site.register(Case,CaseAdmin)
admin.site.register(CaseCategory)
admin.site.register(CyberCaseCategories)
admin.site.register(Evidence)
admin.site.register(Witness)

