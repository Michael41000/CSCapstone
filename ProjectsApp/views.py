"""ProjectsApp Views

Created by Harris Christiansen on 10/02/16.
"""
from django.shortcuts import render

from . import models
from . import forms
from .forms import UpdateProjectForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def getBookmarks(request):
	from AuthenticationApp.models import ProjectTwo
	bookmarks_list = request.user.bookmarks.all()
		
	return render(request, 'bookmarks.html', {
        'bookmarks': bookmarks_list,
    })
    
def getProjects(request):
	projects_list = models.Project.objects.all()
	return render(request, 'projects.html', {
        'projects': projects_list,
    })
    
def addBookmark(request):
	from AuthenticationApp.models import ProjectTwo	
	if request.user.is_authenticated():
		in_name = request.GET.get('name', 'None')
		proj = models.Project.objects.get(name__exact=in_name)
		proj2 = ProjectTwo.objects.get(name__exact=in_name)
		is_bookmarked = True
		
		request.user.bookmarks.add(proj2)
			
		context = {
				'project' : proj,
				'is_bookmarked': is_bookmarked
			}
		return render(request, 'project.html', context)
		# render error page if user is not logged in
	return render(request, 'autherror.html')

def deleteBookmark(request):
	from AuthenticationApp.models import ProjectTwo	
	if request.user.is_authenticated():
		in_name = request.GET.get('name', 'None')
		proj = models.Project.objects.get(name__exact=in_name)
		proj2 = ProjectTwo.objects.get(name__exact=in_name)
		is_bookmarked = False
		
		request.user.bookmarks.remove(proj2)
			
		context = {
				'project' : proj,
				'is_bookmarked': is_bookmarked
			}
		return render(request, 'project.html', context)
		# render error page if user is not logged in
	return render(request, 'autherror.html')

def getProject(request):
	from AuthenticationApp.models import ProjectTwo
	if request.user.is_authenticated():
		in_name = request.GET.get('name', 'None')
		proj = models.Project.objects.get(name__exact=in_name)
		proj2 = ProjectTwo.objects.get(name__exact=in_name)
		is_bookmarked = False
		print(request.user.bookmarks.filter(name__exact=in_name).exists())
		if request.user.bookmarks.filter(name__exact=in_name).exists():
			is_bookmarked = True
		
		context = {
				'project' : proj,
				'is_bookmarked': is_bookmarked
			}
		return render(request, 'project.html', context)
		# render error page if user is not logged in
	return render(request, 'autherror.html')

def getProjectForm(request):
        if request.user.is_authenticated():
                return render(request, 'projectform.html')
        else:
                # render error page if user is not logged in
                return render(request, 'autherror.html')
        
def getProjectFormSuccess(request):
	from AuthenticationApp.models import ProjectTwo
        if request.user.is_authenticated():
                if request.method == 'POST':
                        form = forms.ProjectForm(request.POST)
                        if form.is_valid():
                                if models.Project.objects.filter(name__exact=form.cleaned_data['name']).exists():
                                        return render(request, 'projectform.html', {'error' : 'Error: That Project name already exists!'})
                                new_project = models.Project(name=form.cleaned_data['name'], description=form.cleaned_data['description'], langs=form.cleaned_data['langs'], yearsXP=form.cleaned_data['yearsXP'],specialty=form.cleaned_data['specialty'])
                                temp = ProjectTwo(name=form.cleaned_data['name'], description=form.cleaned_data['description'], langs=form.cleaned_data['langs'], yearsXP=form.cleaned_data['yearsXP'],specialty=form.cleaned_data['specialty'])
                                new_project.save();
                                temp.save();
                                context = {
                                        'name' : form.cleaned_data['name'],
                                        'description' : form.cleaned_data['description'],
                                        'langs' : form.cleaned_data['langs'],
                                        'yearsXP' : form.cleaned_data['yearsXP'],
                                        'specialty' : form.cleaned_data['specialty'],
                                        }
                                return render(request, 'projectformsuccess.html', context)
                else:
                        form = forms.ProjectForm()
                return render(request, 'projectform.html')
        return render(request, 'autherror.html')

@login_required
def update_project(request):
	pname = request.GET.get('name')
	data = {'name', 'description', 'langs', 'yearsXP', 'specialty'}
	newdata = models.Project.objects.raw('SELECT * FROM Projectsapp_Project', translations=data)
	
	form = UpdateProjectForm(request.POST or None, instance=request.user)
	if form.is_valid():
		form.save()
		messages.success(request, 'Success, your project was updated!')

	context = {
		"form": form,
		"page_name" : "Update",
		"button_value" : "Update",
		"links" : ["logout"],
	}
	return render(request, 'project_auth_form.html', context)

def deleteProject(request):
	if request.user.is_authenticated():
		in_name = request.GET.get('name', 'None')
		project_obj = models.Project.objects.get(name__exact=in_name)
		project_obj.delete()
		return render(request, 'projectdeletesuccess.html')
	return render(request, 'autherror.html')
