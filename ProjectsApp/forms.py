"""ProjectsApp Forms

Created by Naman Patwari on 10/10/2016.
"""
from django import forms
from django.core.validators import MaxValueValidator
from .models import Project

class ProjectForm(forms.Form):
    name = forms.CharField(label='Name', max_length=30)
    description = forms.CharField(label='Description', max_length=300)
    langs = forms.CharField(label='langs', max_length=1000)
    yearsXP = forms.IntegerField(label='yearsXP', validators=[MaxValueValidator(10)])
    specialty = forms.CharField(label='specialty', max_length=1000)
    
class UpdateProjectForm(forms.ModelForm):
	"""A form for updating projects."""
	class Meta:
		model = Project        
		fields = ('name', 'description', 'langs', 'yearsXP', 'specialty')
    
	def clean_projectname(self):
		projectname = self.cleaned_data.get("name")
		#Check is project name has changed
		if projectname == self.initial["name"]:
		    return projectname
		#Check if project name exists before
		try:
		    exists = Projects.objects.get(name=name)
		    raise forms.ValidationError("This project name has already been taken!")
		except Projects.DoesNotExist:
		    return email
		except:
		    raise forms.ValidationError("There was an error, please contact us later")
