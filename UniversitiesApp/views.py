"""
UniversitiesApp Views

Created by Jacob Dunbar on 11/5/2016.
"""
from django.shortcuts import render

from . import models
from . import forms
from AuthenticationApp.models import Student, Engineer, Professor

def getUniversities(request):
    if request.user.is_authenticated():
        universities_list = models.University.objects.all()
        context = {
            'universities' : universities_list,
        }
        return render(request, 'universities.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        is_member = in_university.members.filter(email__exact=request.user.email)
        is_in_uni = False
        if(request.user.university_set.count() == 1 and is_member):
        	is_in_uni = True
        elif(request.user.university_set.count() == 0):
        	is_in_uni = True
        context = {
            'university' : in_university,
            'userIsMember': is_member,
            'is_in_uni' : is_in_uni,
        }
        return render(request, 'university.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversityForm(request):
    if request.user.is_authenticated():
        return render(request, 'universityform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversityFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.UniversityForm(request.POST, request.FILES)
            if form.is_valid():
                if models.University.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'universityform.html', {'error' : 'Error: That university name already exists!'})
                new_university = models.University(name=form.cleaned_data['name'], 
                                             photo=request.FILES['photo'],  
                                             description=form.cleaned_data['description'],
                                             website=form.cleaned_data['website'])
                new_university.save()
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'universityformsuccess.html', context)
            else:
                return render(request, 'universityform.html', {'error' : 'Error: Photo upload failed!'})
        else:
            form = forms.UniversityForm()
        return render(request, 'universityform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinUniversity(request):
	if request.user.is_authenticated():
		in_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_name)
		in_university.members.add(request.user)
		in_university.save();
		request.user.university_set.add(in_university)
		request.user.save()
		if request.user.is_student == True:
			current_student = Student.objects.get(user=request.user)
			current_student.university = in_university
			current_student.save()
		elif request.user.is_engineer == True:
			current_engineer = Engineer.objects.get(user=request.user)
			current_engineer.almamater = in_university
			current_engineer.save()
		elif request.user.is_professor == True:
			current_professor = Professor.objects.get(user=request.user)
			current_professor.university = in_university
			current_professor.save()
		context = {
			'university' : in_university,
			'userIsMember': True,
			 'is_in_uni' : True,
		}
		return render(request, 'university.html', context)
	return render(request, 'autherror.html')
    
def unjoinUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        in_university.members.remove(request.user)
        in_university.save();
        request.user.university_set.remove(in_university)
        request.user.save()
        context = {
            'university' : in_university,
            'userIsMember': False,
             'is_in_uni'  : True,
        }
        return render(request, 'university.html', context)
    return render(request, 'autherror.html')
    
def getCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		is_member = in_course.members.filter(email__exact=request.user.email)
		context = {
			'university' : in_university,
			'course' : in_course,
			'userInCourse' : is_member,
		}
		return render(request, 'course.html', context)
	return render(request, 'autherror.html')

def courseForm(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		context = {
			'university': in_university,
		}
		return render(request, 'courseform.html', context)
    # render error page if user is not logged in
	return render(request, 'autherror.html')

def addCourse(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = forms.CourseForm(request.POST)
			if form.is_valid():
				in_university_name = request.GET.get('name', 'None')
				in_university = models.University.objects.get(name__exact=in_university_name)
				if in_university.course_set.filter(tag__exact=form.cleaned_data['tag']).exists():
					return render(request, 'courseform.html', {'error' : 'Error: That course tag already exists at this university!'})
				#new_course = models.Course(tag=form.cleaned_data['tag'],
				#						   name=form.cleaned_data['name'],
				#						   description=form.cleaned_data['description'],
				#						   university=in_university)
				new_course = models.Course()
				new_course.tag = form.cleaned_data['tag']
				new_course.name = form.cleaned_data['name']
				new_course.description = form.cleaned_data['description']
				new_course.university = in_university
				new_course.save()
				request.user.course_set.add(new_course)
				in_university.course_set.add(new_course)
				is_member = in_university.members.filter(email__exact=request.user.email)
				new_course.members.add(request.user)
				new_course.save()
				context = {
					'university' : in_university,
					'userIsMember': is_member,
				}
				return render(request, 'university.html', context)
			else:
				return render(request, 'courseform.html', {'error' : 'Undefined Error!'})
		else:
			form = forms.CourseForm()
			return render(request, 'courseform.html')
		# render error page if user is not logged in
	return render(request, 'autherror.html')
		
def removeCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		in_course.delete()
		is_member = in_university.members.filter(email__exact=request.user.email)
		context = {
			'university' : in_university,
			'userIsMember' : is_member,
		}
		return render(request, 'university.html', context)
	# render error page if user is not logged in
	return render(request, 'autherror.html')

def joinCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		other_user_email = request.POST.get('email', 'None')
		try:
			other_user = models.MyUser.objects.get(email=other_user_email)
		except models.MyUser.DoesNotExist:
			return render(request, 'UserNotExist.html')
		if other_user.is_authenticated():
			if other_user.is_student:
				if other_user.university_set.filter(name__exact=in_university_name).count() == 1:
					in_course.members.add(other_user)
					in_course.save()
					other_user.course_set.add(in_course)
					other_user.save()
				context = {
					'university' : in_university,
					'course' : in_course,
					'userInCourse': True,
				}
				return render(request, 'course.html', context)
			return render(request, 'autherror.html')
		return render(request, 'autherror.html')
	return render(request, 'autherror.html')

def unjoinCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		in_course.members.remove(request.user)
		in_course.save();
		request.user.course_set.remove(in_course)
		request.user.save()
		context = {
			'university' : in_university,
			'course' : in_course,
			'userInCourse': False,
		}
		return render(request, 'course.html', context)
	return render(request, 'autherror.html')
