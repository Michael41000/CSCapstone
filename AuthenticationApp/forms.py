"""AuthenticationApp Forms

Created by Naman Patwari on 10/4/2016.
"""
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import MyUser, Engineer, Professor, Student

USERTYPES = (
	('S', 'Student'),
	('E', 'Engineer'),
	('P', 'Professor'),
)

class LoginForm(forms.Form):
    email = forms.CharField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class RegisterForm(forms.Form):
	"""A form to creating new users. Includes all the required
	fields, plus a repeated password."""
	email = forms.CharField(label='Email', widget=forms.EmailInput, required=True)
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=True)    

	firstname = forms.CharField(label="First name", widget=forms.TextInput, required=False)
	lastname = forms.CharField(label="Last name", widget=forms.TextInput, required=False)
	
	contactinfo = forms.CharField(label="Contact Info", widget=forms.TextInput, required=False)               

	about = forms.CharField(label="About", widget=forms.TextInput, required=False)               
	usertype = forms.ChoiceField(label="Type", choices=USERTYPES, required=True, initial='Student')

 
	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def clean_email(self):
		email = self.cleaned_data.get("email")
		#Check if email exists before
		try:
			exists = MyUser.objects.get(email=email)
			raise forms.ValidationError("This email has already been taken")
		except MyUser.DoesNotExist:
			return email
		except:
			raise forms.ValidationError("There was an error, please contact us later")

class RegisterStudentForm(forms.Form):
	"""A form to creating new users. Includes all the required
	fields, plus a repeated password."""
	yearsXP = forms.IntegerField(label="Years of Programming Experience", widget=forms.NumberInput, required=False)
	languages = forms.CharField(label="Programming Languages", widget=forms.TextInput, required=False)
	specialties = forms.CharField(label="Specialties", widget=forms.TextInput, required=False)


class UpdateForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.
	"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = MyUser        
		fields = ('email', 'password', 'first_name', 'last_name', 'contact_info', 'about')

	def clean_password(self):            
		return self.initial["password"]        

	def clean_email(self):
		email = self.cleaned_data.get("email")
		#Check is email has changed
		if email == self.initial["email"]:
			return email
		#Check if email exists before
		try:
			exists = MyUser.objects.get(email=email)
			raise forms.ValidationError("This email has already been taken")
		except MyUser.DoesNotExist:
			return email
		except:
 			raise forms.ValidationError("There was an error, please contact us later")

	def clean_first_name(self):
		first_name = self.cleaned_data.get("first_name")
		#Check is email has changed
		if first_name is None or first_name == "" or first_name == '':  
			email = self.cleaned_data.get("email")                               
			return email[:email.find("@")]      
		return first_name
   
class UpdateStudentForm(forms.ModelForm):

	yearsXP = forms.IntegerField(label="Years of Programming Experience", widget=forms.NumberInput, required=False)
	languages = forms.CharField(label="Programming Languages", widget=forms.TextInput, required=False)
	specialties = forms.CharField(label="Specialties", widget=forms.TextInput, required=False)


	
	class Meta:
		model = Student        
		fields = ( 'yearsXP', 'languages', 'specialties')
	
	def clean_yearsXP(self):
		yearsXP = self.cleaned_data.get("yearsXP")
		return yearsXP
	
	def clean_languages(self):
		languages = self.cleaned_data.get("languages")
		return languages

	def clean_specialties(self):
		specialties = self.cleaned_data.get("specialties")
		return specialties

"""Admin Forms"""

class AdminUserCreationForm(forms.ModelForm):
    """A form for Admin to creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)    

    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'last_name')        

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(AdminUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
	"""A form for Admin for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.
	"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = MyUser
		fields = ('email', 'password', 'first_name', 'last_name', 'contact_info', 'about', 'is_active', 'is_admin')
	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]        
