from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
import datetime
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def is_agent(views_func):
	def wrapper_func(request, *args, **kwargs):

		user_is_agent=request.user.groups.filter(name="agent").exists()
		user_is_admin=request.user.is_superuser

		if not request.user.is_authenticated:
			return redirect('user_signin')
		elif user_is_agent or user_is_admin :
			return views_func(request, *args, **kwargs)
		else:
			return render(request,'User/access_forbiden.html')

	return wrapper_func

def is_RH(views_func):
	def wrapper_func(request, *args, **kwargs):

		user_is_agent=request.user.groups.filter(name="RESSOURCES HUMAINES").exists()
		user_is_admin=request.user.is_superuser

		if not request.user.is_authenticated:
			return redirect('user_signin')
		elif user_is_agent or user_is_admin :
			return views_func(request, *args, **kwargs)
		else:
			return render(request,'User/access_forbiden.html')

	return wrapper_func

def is_MG(views_func):
	def wrapper_func(request, *args, **kwargs):

		user_is_agent=request.user.groups.filter(name="MOYENS GENERAUX").exists()
		user_is_admin=request.user.is_superuser

		if not request.user.is_authenticated:
			return redirect('user_signin')
		elif user_is_agent or user_is_admin :
			return views_func(request, *args, **kwargs)
		else:
			return render(request,'User/access_forbiden.html')

	return wrapper_func


def is_admin(views_func):
	def wrapper_func(request, *args, **kwargs):

		user_is_admin=request.user.is_superuser

		if not request.user.is_authenticated:
			return redirect('user_signin')
		elif user_is_admin :
			return views_func(request, *args, **kwargs)
		else:
			return render(request,'User/access_forbiden.html')

	return wrapper_func

