from __future__ import unicode_literals

from django.db import models
from AuthenticationApp.models import MyUser
from django.utils.timezone import now

# Create your models here.

class Comment(models.Model):
	idnum = models.IntegerField(null = True)
	user = models.ForeignKey(MyUser, null = True)
	time = models.DateTimeField(default = now)
	comment = models.CharField(max_length=500)
