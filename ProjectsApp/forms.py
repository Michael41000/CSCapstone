"""ProjectsApp Forms

Created by Naman Patwari on 10/10/2016.
"""
from django import forms
from django.core.validators import MaxValueValidator

class ProjectForm(forms.Form):
    name = forms.CharField(label='Name', max_length=30)
    description = forms.CharField(label='Description', max_length=300)
    langs = forms.CharField(label='langs', max_length=1000)
    yearsXP = forms.IntegerField(label='yearsXP', validators=[MaxValueValidator(10)])
    specialty = forms.CharField(label='specialty', max_length=1000)
