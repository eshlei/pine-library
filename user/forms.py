from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
	username = forms.CharField(label='username')
	password = forms.CharField(label='password', widget=forms.PasswordInput)