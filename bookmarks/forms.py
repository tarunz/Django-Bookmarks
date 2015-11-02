from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
#model for the user registration form
class RegistrationForm(forms.Form):
	username=forms.CharField(label="Username",max_length=30)
	email=forms.EmailField(label="Email*")
	password1=forms.CharField(
		label="Password",
		widget=forms.PasswordInput()
		)
	password2=forms.CharField(
		label="Password (Again)",
		widget=forms.PasswordInput()
		)

	def clean_password2(self):
		if 'password1' in self.cleaned_data:
			password1=self.cleaned_data['password1']
			password2=self.cleaned_data['password2']
			if password2==password1:
				return password2
		raise forms.ValidationError("Passwords do not match.")

	def clean_username(self):
		username=self.cleaned_data['username']
		if not re.search(r'^\w+$',username):
			raise forms.VaidationError('''Username can only contain  
				alphanumeric characters or underscore.''')
		try:
			User.objects.get(username=username)
		except ObjectDoesNotExist:
			return username
		raise forms.ValidationError("Username already taken.")
	def clean_email(self):
		if 'email' in self.cleaned_data:
			email=self.cleaned_data['email']
			try:
				User.objects.get(email=email)
			except ObjectDoesNotExist:
				return email
			raise forms.ValidationError("Email already exists.")
			raise forms.ValidationError("Enter valid email. ")

class BookmarkSaveForm(forms.Form):
	url=forms.URLField(
		label="URL",
		widget=forms.TextInput(attrs={'size':64}),
		)
	title=forms.CharField(
		label="Title",
		widget=forms.TextInput(attrs={'size':64})
		)
	tags=forms.CharField(
		label="Tags",
		required=False,
		widget=forms.TextInput(attrs={'size':64})
		)