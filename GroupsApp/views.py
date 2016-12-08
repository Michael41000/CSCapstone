"""GroupsApp Views
Created by Naman Patwari on 10/10/2016.
"""
from django.shortcuts import render

from . import models
from . import forms
from CommentsApp.models import Comment

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

    
