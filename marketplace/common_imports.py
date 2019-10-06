from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from marketplace.views.helpers import *
from marketplace.forms import UsersRegisterForm
from marketplace.forms import UsersLoginForm
from marketplace.models import Game,User,Wallet