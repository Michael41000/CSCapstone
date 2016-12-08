"""GroupsApp URL

Created by Naman Patwari on 10/10/2016.
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^group/all$', views.getGroups, name='Groups'),
	url(r'^group/form$', views.getGroupForm, name='GroupForm'),
    url(r'^group/formsuccess$', views.getGroupFormSuccess, name='GroupFormSuccess'),
    url(r'^group/join$', views.joinGroup, name='GJoin'),
    url(r'^group/joinUser$', views.joinGroupUser, name='GJoin'),
    url(r'^group/unjoin$', views.unjoinGroup, name='GUnjoin'),
    url(r'^group$', views.getGroup, name='Group'),
    url(r'^group/groupaddcomment$', views.addGroupComment, name='GroupComment'),
    url(r'^group/delete$', views.deleteGroup, name='GroupDelete'),
    url(r'^group/deletecomment$', views.deleteComment, name='CommentDelete'),
    url(r'^group/recommendations$', views.recommendedProjects, name='CommentDelete'),
]
