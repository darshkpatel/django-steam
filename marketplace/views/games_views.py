from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from marketplace.common_imports import *

@login_required(login_url='/accounts/login')
def index(request):
	context = {
		"games" : get_games()
	}
	messages.warning(request,"Test")
	return render(request, "marketplace/games.html", context)
