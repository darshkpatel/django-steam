from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .helpers import *
from .forms import UsersRegisterForm
from .forms import UsersLoginForm
from .models import Game,User,Wallet
# Create your views here.

@login_required(login_url='/accounts/login')
def index(request):
	context = {
		"balance":float(User.objects.get(username=request.user.username).wallet.balance),
		"inventory" : get_inventory(request.user.username)
		}
	return render(request, "marketplace/home.html",context)

@login_required(login_url='/accounts/login')
def games(request):
	context = {
		"games" : get_games()
	}
	return render(request, "marketplace/games.html", context)

def login_view(request):
	form = UsersLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username = username, password = password)
		login(request, user)
		return redirect("/")
	return render(request, "accounts/form.html", {
		"form" : form,
		"title" : "Login",
	})


def register_view(request):
	form = UsersRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save()
		password = form.cleaned_data.get("password")	
		user.set_password(password)
		user.save()
		new_user = authenticate(username = user.username, password = password)
		login(request, new_user)
		return redirect("/login/")
	return render(request, "accounts/form.html", {
		"title" : "Register",
		"form" : form,
	})
 
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")