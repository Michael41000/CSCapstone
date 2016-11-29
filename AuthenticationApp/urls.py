"""AuthenticationApp URL Configuration

Created by Naman Patwari on 10/4/2016.
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login$', views.auth_login, name='Login'),
    url(r'^logout$', views.auth_logout, name='Logout'),
    url(r'^registerStudent$', views.auth_register_student, name='RegisterStudent'),
	url(r'^update$', views.update_profile, name='UpdateProfile'),    
	url(r'^registerEngineer$', views.auth_register_engineer, name='RegisterEngineer'),
]
