from marketplace.common_imports import *
from django.core import serializers


@login_required(login_url='/accounts/login')
def market(request):
	context = {
		"balance":float(User.objects.get(username=request.user.username).wallet.balance),
		"items" : get_inventory_items(request.user.username),
		}
	return render(request, "marketplace/market.html",context)

@login_required(login_url='/accounts/login')
def table(request):
    object_list = User.objects.get(username=request.user.username).inventory.items.all()
    json = serializers.serialize('json', object_list)
    return HttpResponse(json, content_type='application/json')


