"""GroupsApp Forms

Created by Naman Patwari on 10/10/2016.
"""
from django import forms

class GroupForm(forms.Form):
    name = forms.CharField(label='Name', max_length=30)
    description = forms.CharField(label='Description', max_length=300)
<<<<<<< HEAD

class GroupUserForm(forms.Form):
    email = forms.CharField(label='Email', max_length=50)
=======
>>>>>>> 9751b6324c9d8b2f18e6d8d3ea540a5f385ca993
