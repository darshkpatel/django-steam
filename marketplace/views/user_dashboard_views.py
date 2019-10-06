from marketplace.common_imports import *
# Create your views here.

@login_required(login_url='/accounts/login')
def index(request):
	context = {
		"balance":float(User.objects.get(username=request.user.username).wallet.balance),
		"items" : get_inventory_items(request.user.username),
		"games" : list(User.objects.get(username=request.user.username).inventory.games.all().values('description','name'))
		}
	return render(request, "marketplace/home.html",context)


