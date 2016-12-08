"""ProjectsApp URL Configuration

Created by Harris Christiansen on 10/02/16.
"""
from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^project/all$', views.getProjects, name='Projects'),
	url(r'^bookmarks/all$', views.getBookmarks, name='Bookmarks'),
	url(r'^project$', views.getProject, name='Project'),
	url(r'^project/addbookmark$', views.addBookmark, name='Add Bookmark'),
	url(r'^project/deletebookmark$', views.deleteBookmark, name='Delete Bookmark'),
	url(r'^project/form$', views.getProjectForm, name='ProjectForm'),
	url(r'^project/formsuccess$', views.getProjectFormSuccess, name='ProjectFormSuccess'),
	url(r'^project/update?$', views.update_project, name='UpdateProjectForm'),
	url(r'^project/delete?$', views.deleteProject, name='ProjectDelete')
]
