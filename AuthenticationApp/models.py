"""AuthenticationApp Models

Created by Naman Patwari on 10/4/2016.
"""

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator

# Create your models here.
class ProjectTwo(models.Model):
	name = models.CharField(max_length=200) 
	description = models.CharField(max_length=10000)
	#created_at = models.DateTimeField('date created', default=now, blank=True)
    #updated_at = models.DateTimeField('date updated', default=now, blank=True)
	langs = models.CharField(max_length=1000)
	yearsXP = models.IntegerField(validators=[MaxValueValidator(10)], null=True)
	specialty = models.CharField(max_length=1000)
	
class MyUserManager(BaseUserManager):
	def create_user(self, email=None, password=None, first_name=None, last_name=None):
		if not email:
			raise ValueError('Users must have an email address')

		#We can safetly create the user
		#Only the email field is required
		user = self.model(email=email)
		user.set_password(password)
		user.first_name = first_name
		user.last_name = last_name

		#If first_name is not present, set it as email's username by default
		if first_name is None or first_name == "" or first_name == '':
			user.first_name = email[:email.find("@")]            
        
		user.save(using=self._db)
		return user

	def create_superuser(self, email=None, password=None, first_name=None, last_name=None):
		user = self.create_user(email, password=password, first_name=first_name, last_name=last_name)
		user.is_admin = True
		user.save(using=self._db)
		return user


class MyUser(AbstractBaseUser):

	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True,
	)

	first_name = models.CharField(
		max_length=120,
		null=True,
		blank=True,
	)    

	last_name = models.CharField(
		max_length=120,
		null=True,
		blank=True,
	)

	contact_info = models.CharField(
		max_length=120,
		null=True,
		blank=True,
	)

	about = models.CharField(
		max_length=120,
		null=True,
		blank=True,
	)
	
	bookmarks = models.ManyToManyField(ProjectTwo);

    # #New fields 	
	is_student = models.BooleanField(default=False,)
	is_professor = models.BooleanField(default=False,)
	is_engineer = models.BooleanField(default=False,)
	

	is_active = models.BooleanField(default=True,)
	is_admin = models.BooleanField(default=False,)

	objects = MyUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	def get_full_name(self):        
		return "%s %s" %(self.first_name, self.last_name)

	def get_short_name(self):        
		return self.first_name

	def __str__(self):              #Python 3
		return self.email

	def __unicode__(self):           # Python 2
		return self.email

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):        
		return True

        
	@property
	def is_staff(self):
		return self.is_admin
    
#     def new_user_reciever(sender, instance, created, *args, **kwargs):
#     	if created:   
     
# Going to use signals to send emails
# post_save.connect(new_user_reciever, sender=MyUser)
             

class Student(models.Model):
	from UniversitiesApp.models import University
	
	user = models.OneToOneField(
		MyUser,
		on_delete=models.CASCADE,
		primary_key=True)

	university = models.ForeignKey(University, on_delete=models.CASCADE, null=True)
	
	yearsXP = models.IntegerField(
		null=True,
		blank=True,
	)
    
	languages = models.CharField(
		max_length=120,
		null=True,
		blank=True,
	)
    
	specialties = models.CharField(
		max_length=120,
		null=True,
		blank=True,
	)
    
	def get_full_name(self):        
		return "%s %s" %(self.user.first_name, self.user.last_name)

	def get_short_name(self):        
		return self.user.first_name
        
	def get_yearsXP(self):
		return self.yearsXP
        
	def get_languages(self):
		return self.languages
        
	def get_specialties(self):
		return self.specialties

	def __str__(self):              #Python 3
		return self.user.email

	def __unicode__(self):           # Python 2
		return self.user.email

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):        
		return True


	@property
	def is_staff(self):
		return False

class Engineer(models.Model):
	from UniversitiesApp.models import University
	
	user = models.OneToOneField(
		MyUser,
		on_delete=models.CASCADE,
		primary_key=True)

	almamater = models.ForeignKey(University, on_delete=models.CASCADE, null=True)

	projects = models.ManyToManyField(ProjectTwo)

	def get_full_name(self):        
		return "%s %s" %(self.user.first_name, self.user.last_name)

	def get_short_name(self):        
		return self.user.first_name

	def __str__(self):              #Python 3
		return self.user.email

	def __unicode__(self):           # Python 2
		return self.user.email

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):        
		return True


	@property
	def is_staff(self):
		return False
		
	

class Professor(models.Model):
	from UniversitiesApp.models import University
	
	user = models.OneToOneField(
		MyUser,
		on_delete=models.CASCADE,
		primary_key=True)

	university = models.ForeignKey(University, on_delete=models.CASCADE, null=True)

	def get_full_name(self):        
		return "%s %s" %(self.user.first_name, self.user.last_name)

	def get_short_name(self):        
		return self.user.first_name

	def __str__(self):              #Python 3
		return self.user.email

	def __unicode__(self):           # Python 2
		return self.user.email

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):        
		return True


	@property
	def is_staff(self):
		return False
