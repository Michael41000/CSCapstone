"""AuthenticationApp Views

Created by Naman Patwari on 10/4/2016.
"""

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages


from .forms import LoginForm, RegisterStudentForm, RegisterEngineerForm, UpdateForm
from .models import MyUser, Student, Engineer

# Auth Views

def auth_login(request):
	form = LoginForm(request.POST or None)
	next_url = request.GET.get('next')
	if next_url is None:
		next_url = "/"
	if form.is_valid():
		email = form.cleaned_data['email']
		password = form.cleaned_data['password']
		user = authenticate(email=email, password=password)
		if user is not None:
			messages.success(request, 'Success! Welcome, '+(user.first_name or ""))
			if user.is_student == True:
				print "Is Student"
			elif user.is_engineer == True:
				print "Is Engineer"
			elif user.is_professor == True:
				print "Is Professor"

			login(request, user)
			return HttpResponseRedirect(next_url)
		else:
			messages.warning(request, 'Invalid username or password.')
			
	context = {
		"form": form,
		"page_name" : "Login",
		"button_value" : "Login",
		"links" : ["register"],
	}
	return render(request, 'auth_form.html', context)

def auth_logout(request):
	logout(request)
	messages.success(request, 'Success, you are now logged out')
	return render(request, 'index.html')

def auth_register_student(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/")
		
	form = RegisterStudentForm(request.POST or None)
	if form.is_valid():

		new_user = MyUser.objects.create_user(
			email=form.cleaned_data['email'], 
			password=form.cleaned_data["password2"], 
			first_name=form.cleaned_data['firstname'], 
			last_name=form.cleaned_data['lastname'],
		)
		new_user.is_student = True
		new_user.save()	
		#Also registering students		
		new_student = Student(user = new_user)
		new_student.yearsXP = form.cleaned_data["yearsXP"]
		new_student.languages = form.cleaned_data["languages"]
		new_student.specialties = form.cleaned_data["specialties"]
		new_student.save()
		login(request, new_user);	
		messages.success(request, 'Success! Your Student account was created.')
		return render(request, 'index.html')

	context = {
		"form": form,
		"page_name" : "Register",
		"button_value" : "Register",
		"links" : ["login"],
	}
	return render(request, 'auth_form.html', context)

@login_required
def update_profile(request):
	form = UpdateForm(request.POST or None, instance=request.user)
	if form.is_valid():
		form.save()
		messages.success(request, 'Success, your profile was saved!')

	context = {
		"form": form,
		"page_name" : "Update",
		"button_value" : "Update",
		"links" : ["logout"],
	}
	return render(request, 'auth_form.html', context)

def auth_register_engineer(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/")
		
	form = RegisterEngineerForm(request.POST or None)
	if form.is_valid():

		new_user = MyUser.objects.create_user(email=form.cleaned_data['email'], 
			password=form.cleaned_data["password2"], 
			first_name=form.cleaned_data['firstname'], last_name=form.cleaned_data['lastname'])
		new_user.is_engineer = True	
		new_user.save()
		#Also registering engineer	
		new_engineer = Engineer(user = new_user)
		new_engineer.almamater = form.cleaned_data["almamater"]
		new_engineer.about = form.cleaned_data["about"]
		new_engineer.contactinfo = form.cleaned_data["contactinfo"]
		new_engineer.save()
		login(request, new_user);	
		messages.success(request, 'Success! Your Engineer account was created.')
		return render(request, 'index.html')

	context = {
		"form": form,
		"page_name" : "Register",
		"button_value" : "Register",
		"links" : ["login"],
	}
	return render(request, 'auth_form.html', context)


