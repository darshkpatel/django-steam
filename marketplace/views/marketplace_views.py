from marketplace.common_imports import *
from django.core import serializers



def process_buy_order(order):
	pass

def process_sell_order(order):
	pass

def log_order(order):
	pass

def find_matching_sell(order):
	pass

def find_matching_buy(order):
	pass



@login_required(login_url='/accounts/login')
def market(request):
	context = {
		"balance":float(User.objects.get(username=request.user.username).wallet.balance),
		"items" : get_inventory_items(request.user.username),
		"games" : list(User.objects.get(username=request.user.username).inventory.games.all().values('description','name')),
		"sell" :get_sell_orders(),
		"buy" :get_buy_orders(),
		}

	return render(request, "marketplace/market.html",context)


#  Depriciated 

# @login_required(login_url='/accounts/login')
# def table(request):
#     object_list = User.objects.get(username=request.user.username).inventory.items.all()
#     json = serializers.serialize('json', object_list)
#     return HttpResponse(json, content_type='application/json')

@login_required(login_url='/accounts/login')
def sell(request):
	sell_thing = request.GET.get('sell_thing', None)
	
	
	if sell_thing:
		user_balance = Wallet.objects.get(user=request.user.username).balance
		# Locks the selected entry for update
		user_inventory = Inventory.objects.select_for_update().get(user=request.user.username)
		user_wallet = Wallet.objects.select_for_update().get(user=request.user.username)

		if (list(user_inventory.games.filter(name=sell_thing).values())) or (list(user_inventory.Items.filter(name=sell_thing).values())):
			
			return HttpResponseRedirect(reverse('market'))			

		else:
			messages.warning(request,"You don't own the item or game")
			return HttpResponseRedirect(reverse('market'))			
		

	return HttpResponseRedirect(reverse('market'))



@login_required(login_url='/accounts/login')
def buy(request):
	buy_thing = request.GET.get('buy_thing', None)


	if buy_thing:
		user_balance = Wallet.objects.get(user=request.user.username).balance

		# Locks the selected entry for update
		user_inventory = Inventory.objects.select_for_update().get(user=request.user.username)
		user_wallet = Wallet.objects.select_for_update().get(user=request.user.username)

		if (buy_thing not in user_inventory.games.all()) or (buy_thing not in user_inventory.items.all()):
			pass
		else:
			messages.warning(request,"You already own the item or game")
			return HttpResponseRedirect(reverse('market'))			
		
	return HttpResponseRedirect(reverse('market'))
