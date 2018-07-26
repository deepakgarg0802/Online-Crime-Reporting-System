from django.contrib.auth import authenticate
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import *


class UsersLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UsersLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            "name":"username",
            "placeholder":"Username"})
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            "name":"password",
            "placeholder":"Password"})

    def clean(self, *args, **keyargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username = username, password = password)
            if not user:
                raise forms.ValidationError(_("Invalid Credentials"))

        return super(UsersLoginForm, self).clean(*args, **keyargs)



class criminal_form(forms.ModelForm):
    class Meta:
        model=Criminal
        fields="__all__"
       
    def __init__(self, *args, **kwargs):
        super(criminal_form, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            "name":"name"})
        self.fields['father_name'].widget.attrs.update({
            'class': 'form-control',
            "name":"father_name"})

        self.fields['age'].widget.attrs.update({
            'class': 'form-control',
            "name":"age"})
        self.fields['caste'].widget.attrs.update({
            'class': 'form-control',
            "name":"caste"})
        self.fields['ward'].widget.attrs.update({
            'class': 'form-control',
            "name":"ward"})
        self.fields['birth_mark_desc'].widget.attrs.update({
            'class': 'form-control',
            "name":"birth_mark_desc"})
        self.fields['height'].widget.attrs.update({
            'class': 'form-control',
            "name":"height"})
        self.fields['complexion'].widget.attrs.update({
            'class': 'form-control',
            "name":"complexion"})        
        self.fields['eyes'].widget.attrs.update({
            'class': 'form-control',
            "name":"eyes"})  

# name = models.CharField(max_length=255, blank=False)

#     father_name = models.CharField(max_length=255)
#     age = models.IntegerField(max_length=255)
#     caste = models.CharField(max_length=255)
#     ward=models.ForeignKey(null=True)
#     birth_mark_desc=models.TextArea()
#     height=models.CharField(max_length=255)
#     complexion=models.CharField(max_length=255)
#     eyes=models.CharField(max_length=255)
