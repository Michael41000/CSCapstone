"""AuthenticationApp Views

Created by Naman Patwari on 10/4/2016.
"""

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages


from .forms import LoginForm, RegisterForm, UpdateForm, RegisterStudentForm, UpdateStudentForm
from .models import MyUser, Student, Engineer, Professor

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
		"userform": form,
		"page_name" : "Login",
		"button_value" : "Login",
		"links" : ["register"],
	}
	return render(request, 'auth_form.html', context)

def auth_logout(request):
	logout(request)
	messages.success(request, 'Success, you are now logged out')
	return render(request, 'index.html')

def auth_register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/")
		
	userform = RegisterForm(request.POST or None)
	studentform = RegisterStudentForm(request.POST or None)
	if userform.is_valid() and studentform.is_valid():
		new_user = MyUser.objects.create_user(
			email=userform.cleaned_data['email'], 
			password=userform.cleaned_data["password2"], 
			first_name=userform.cleaned_data['firstname'], 
			last_name=userform.cleaned_data['lastname'],
		)
		new_user.contact_info = userform.cleaned_data['contactinfo']
		new_user.about = userform.cleaned_data['about']
		#Also registering students		
		if userform.cleaned_data['usertype'] == 'S':	
			new_user.is_student = True
			new_student = Student(user = new_user)
			new_student.yearsXP = studentform.cleaned_data["yearsXP"]
			new_student.languages = studentform.cleaned_data["languages"]
			new_student.specialties = studentform.cleaned_data["specialties"]
			new_student.save()
		elif userform.cleaned_data['usertype'] == 'E':
			new_user.is_engineer = True
			new_engineer = Engineer(user = new_user)
			new_engineer.save()
		elif userform.cleaned_data['usertype'] == 'P':
			new_user.is_professor = True
			new_professor = Professor(user = new_user)
			new_professor.save()
		new_user.save()
		login(request, new_user);	
		messages.success(request, 'Success! Your account was created.')
		return render(request, 'index.html')

	context = {
		"userform": userform,
		"studentform" : studentform,
		"page_name" : "Register",
		"button_value" : "Register",
		"links" : ["login"],
	}
	return render(request, 'register_form.html', context)

@login_required
def update_profile(request):
	form = UpdateForm(request.POST or None, instance=request.user)
	if form.is_valid():
		form.save()
		messages.success(request, 'Success, your profile was saved!')
		return render(request, 'viewProfile.html')
	context = {
		"userform": form,
		"page_name" : "Update",
		"button_value" : "Update",
		"links" : ["logout"],
	}
	return render(request, 'update_form.html', context)

@login_required
def view_profile(request):
	firstName = request.user.first_name
	lastName = request.user.last_name
	about = request.user.about
	contactinfo = request.user.contact_info
	email = request.user.email

	if request.user.is_student:
		yearsXP = request.user.student.yearsXP
		languages = request.user.student.languages
		specialties = request.user.student.specialties
		context = {
			"firstName" : firstName,
			"lastName": lastName,
			"about": about,
			"contactinfo" : contactinfo,
			"email" : email,
			"yearsXP" : yearsXP,
			"languages" : languages,
			"specialties" : specialties,
			"page_name" : "View",
			"links" : ["logout"],
		}	
		return render(request, 'viewProfile.html', context)

	context = {
		"firstName" : firstName,
		"lastName": lastName,
		"about": about,
		"contactinfo" : contactinfo,
		"email" : email,
		"page_name" : "View",
		"links" : ["logout"],
	}	
	return render(request, 'viewProfile.html', context)
