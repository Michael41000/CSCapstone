"""GroupsApp Views
Created by Naman Patwari on 10/10/2016.
"""
from django.shortcuts import render

from . import models
from . import forms
from CommentsApp.models import Comment
from ProjectsApp.models import Project

def getGroups(request):
    if request.user.is_authenticated():
        groups_list = models.Group.objects.all()
        context = {
            'groups' : groups_list,
        }
        return render(request, 'groups.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        is_member = in_group.members.filter(email__exact=request.user.email)
        context = {
            'group' : in_group,
            'userIsMember': is_member,
        }
        return render(request, 'group.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupForm(request):
    if request.user.is_authenticated():
        return render(request, 'groupform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.GroupForm(request.POST)
            if form.is_valid():
                if models.Group.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'groupform.html', {'error' : 'Error: That Group name already exists!'})
                new_group = models.Group(name=form.cleaned_data['name'], description=form.cleaned_data['description'])
                new_group.save()
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'groupformsuccess.html', context)
        else:
            form = forms.GroupForm()
        return render(request, 'groupform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinGroup(request):
    if request.user.is_authenticated():
    	print request.user
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.members.add(request.user)
        in_group.save();
        request.user.group_set.add(in_group)
        request.user.save()
        context = {
            'group' : in_group,
            'userIsMember': True,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')

def joinGroupUser(request):
    if request.user.is_authenticated():
        print request.user
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        other_user_email = request.POST.get('email', 'None')
        print other_user_email
        try:
            other_user = models.MyUser.objects.get(email=other_user_email)
        except models.MyUser.DoesNotExist:
            return render(request, 'UserNotExist.html')
        if other_user.is_authenticated():
            if other_user.is_student:
                in_group.members.add(other_user)
                in_group.save();
                other_user.group_set.add(in_group)
                other_user.save()
            context = {
                'group' : in_group,
                'userIsMember': True,
            }
            return render(request, 'group.html', context)
        return render(request, 'autherror.html')
    return render(request, 'autherror.html')

def unjoinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.members.remove(request.user)
        in_group.save();
        request.user.group_set.remove(in_group)
        request.user.save()
        context = {
            'group' : in_group,
            'userIsMember': False,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')
    
def addGroupComment(request):
	if request.user.is_authenticated():
		in_name = request.GET.get('name', 'None')
		in_group = models.Group.objects.get(name__exact=in_name)
		if request.method == 'POST':
			form = forms.CommentForm(request.POST)
			if form.is_valid():
				new_comment = Comment(user=request.user)
				new_comment.comment = form.cleaned_data['comment']
				new_comment.idnum = in_group.comments.count() + 1
				new_comment.save()
				in_group.comments.add(new_comment)
				comments_list = in_group.comments.all()
				is_member = in_group.members.filter(email__exact=request.user.email)
				context = {
					'comments' : comments_list,
					'group' : in_group,
					'userIsMember' : is_member,
				}
				return render(request, 'group.html', context)
			else:
				form = forms.CommentForm()
	return render(request, 'autherror.html')
	
def deleteGroup(request):
	if request.user.is_authenticated():
		in_name = request.GET.get('name', 'None')
		in_group = models.Group.objects.get(name__exact=in_name)
		in_group.delete()
		return render(request, 'groupdeletesuccess.html')
	return render(request, 'autherror.html')

def deleteComment(request):
	if request.user.is_authenticated():
		in_name = request.GET.get('name', 'None')
		in_group = models.Group.objects.get(name__exact=in_name)
		idnum = request.GET.get('idnum', 'None')
		comment = in_group.comments.filter(idnum = idnum)
		comment.delete()
		is_member = in_group.members.filter(email__exact=request.user.email)
		context = {
					'group' : in_group,
					'userIsMember' : is_member,
				}
		return render(request, 'group.html', context)
	return render(request, 'autherror.html')
	
def recommendedProjects(request):
	if request.user.is_authenticated():
		in_name = request.GET.get('name', 'None')
		in_group = models.Group.objects.get(name__exact=in_name)
		totalYearsXP = 0
		totalLanguages = []
		totalSpecialties = []
		for e in in_group.members.all():
			print e.first_name
			print e.student.yearsXP
			print e.student.languages
			print e.student.specialties
			totalYearsXP += e.student.yearsXP
			totalLanguages.append(e.student.languages.split(','))
			totalSpecialties.append(e.student.specialties.split(','))

		totalLanguagesCleaned = sum(totalLanguages, [])
		totalLanguagesCleaned = [x.strip(' ') for x in totalLanguagesCleaned]
		totalLanguagesSet = list(set(totalLanguagesCleaned))
		totalSpecialtiesCleaned = sum(totalSpecialties, [])
		totalSpecialtiesCleaned = [x.strip(' ') for x in totalSpecialtiesCleaned]
		totalSpecialtiesSet = list(set(totalSpecialtiesCleaned))

		
		print totalYearsXP
		print totalLanguagesSet
		print totalSpecialtiesSet

		recommendedProjects = []	
		for e in Project.objects.all():
			print e.name
			print e.yearsXP
			print e.specialty
			specialtyList = []
			specialtyList.append(e.specialty.split(','))
			specialtyList = sum(specialtyList, [])
			specialtyList = [x.strip(' ') for x in specialtyList]
			langsList = []
			langsList.append(e.langs.split(','))
			langsList = sum(langsList, [])
			langsList = [x.strip(' ') for x in langsList]
			print langsList
			print specialtyList
			if totalYearsXP >= e.yearsXP and bool(set(specialtyList) & set(totalSpecialtiesSet)) and bool(set(totalLanguagesSet) & set(langsList)):
				recommendedProjects.append(e)

		
		#Run through all the users and parse their years of experience, programming languages, and specialties.
		#Look at the projects and see which ones fit the best. 
		print "RecommendedProjects"
		print recommendedProjects
		context = {
					'group' : in_group,
					'projects' : recommendedProjects,
					
				}
		return render(request, 'recommendedProjects.html', context)
	return render(request, 'autherror.html')

    
