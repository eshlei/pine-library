from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def login_view(request):
	warning=''
	username=''
	password=''
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user != None:
			login(request, user)
			return HttpResponseRedirect(reverse('library:index'))
		else:
			warning='in valid username/password'
	return render(request, 'user/login.html',{'warning':warning, 'usn':username, 'pwd':password})

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('library:index'))

def profile(request):
	return render(request, 'user/profile.html')

def register(request):
	warning=''
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		repeated_password = request.POST['repeated_password']
		if repeated_password == password:
			user=User.objects.create_user(username, '', password)
			login(request,user)
			return HttpResponseRedirect(reverse('library:index'))
		else:
			warning='passwords do not match!'
	return render(request, 'user/register.html', {'warning':warning})