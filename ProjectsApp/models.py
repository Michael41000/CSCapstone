"""ProjectsApp Models

Created by Harris Christiansen on 10/02/16.
"""
from django.db import models
from django.core.validators import MaxValueValidator
from CompaniesApp.models import Company
from django.utils.timezone import now

class Project(models.Model):

    name = models.CharField(max_length=200) 
    description = models.CharField(max_length=10000)
    created_at = models.DateTimeField('date created', default=now, blank=True)
    #updated_at = models.DateTimeField('date updated', default=now, blank=True)

    # TODO Task 3.5: Add field for company relationship
    # TODO Task 3.5: Add fields for project qualifications (minimum required: programming language, years of experience, speciality)
    langs = models.CharField(max_length=1000, default='None')
    yearsXP = models.IntegerField(validators=[MaxValueValidator(10)], default='1')
    specialty = models.CharField(max_length=1000, default='None')
    companyRelationship = models.OneToOneField(Company, null=True);

    def __str__(self):
        return self.name
