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
def mylistings(request):
	context = {
		"balance":float(User.objects.get(username=request.user.username).wallet.balance),
		"items" : get_inventory_items(request.user.username),
		"all_items" : [get_item_details(itm['itemID']) for itm in Item.objects.all().values()],
		"sell" :get_sell_orders(),
		"buy" :get_buy_orders(),
		}

	return render(request, "marketplace/listings.html",context)


#  Depriciated 

# @login_required(login_url='/accounts/login')
# def table(request):
#     object_list = User.objects.get(username=request.user.username).inventory.items.all()
#     json = serializers.serialize('json', object_list)
#     return HttpResponse(json, content_type='application/json')

@login_required(login_url='/accounts/login')
def sell(request):
	sell_thing = request.GET.get('sell_thing', None)
	price = request.GET.get('price', 0)
	
	
	if sell_thing:
		# Locks the selected entry for update
		user = User.objects.get(username=request.user.username)
		user_inventory = Inventory.objects.select_for_update().get(user=request.user.username)
		item = user_inventory.items.get(itemName=sell_thing)
		if item:

			# txn = WalletTransaction()	
			sell_order = SellOrder(itemID=item, sellingPrice=price, username=user)
			user_inventory.items.remove(item)
			user_inventory.save()
			sell_order.save()
			messages.info(request,"Item listed on the community market")
			return HttpResponseRedirect(reverse('listings'))	

		else:
			messages.warning(request,"You don't own the item or game")
			return HttpResponseRedirect(reverse('listings'))	

	else:
		messages.warning(request,"You don't own the item or game")
		return HttpResponseRedirect(reverse('listings'))			
		

	return HttpResponseRedirect(reverse('listings'))

@login_required(login_url='/accounts/login')
def delete_inv(request):
	delete_thing = request.GET.get('delete_thing', None)	
	if delete_thing:
		# Locks the selected entry for update
		# item = Item.objects.get(itemName=delete_thing)

			# txn = WalletTransaction()	
		user = User.objects.get(username=request.user.username)
		user_inventory = Inventory.objects.select_for_update().get(user=request.user.username)
		user_wallet = Wallet.objects.select_for_update().get(user=request.user.username)
		print(delete_thing)
		item = Item.objects.get(itemName=delete_thing)


		del_order = SellOrder.objects.filter(itemID__itemName=delete_thing,username=request.user.username).delete()
		
		user_inventory.items.add(item)
		# user_inventory.items.remove(item)
	
		print(del_order)
		messages.info(request,"Listing Deleted")
		return HttpResponseRedirect(reverse('listings'))	

	else:
		messages.warning(request,"You don't own the item or game")
		return HttpResponseRedirect(reverse('listings'))			
		

	return HttpResponseRedirect(reverse('listings'))



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

@login_required(login_url='/accounts/login')
def buy_order(request):
	buy_thing = request.GET.get('list_thing', None)
	price = request.GET.get('price', None)
	print("Started",buy_thing)
	if buy_thing:
		user_balance = Wallet.objects.get(user=request.user.username).balance
		print("Inside")
		# Locks the selected entry for update
		user_inventory = Inventory.objects.select_for_update().get(user=request.user.username)
		user_wallet = Wallet.objects.select_for_update().get(user=request.user.username)

		if not user_inventory.items.filter(itemName=buy_thing):
			item_id = Item.objects.get(itemName=buy_thing)
			buy_obj = BuyOrder(itemID=item_id, buyPrice=price, username=User.objects.get(username=request.user.username))
			buy_obj.save()
			messages.info(request,"Buy Order Added")
			return HttpResponseRedirect(reverse('listings'))			

		else:
			messages.warning(request,"You already own the item")
			return HttpResponseRedirect(reverse('listings'))			
		
	return HttpResponseRedirect(reverse('listings'))

@login_required(login_url='/accounts/login')
def delete_buy_order(request):
	list_thing = request.GET.get('list_thing', None)
	if list_thing:
		user_balance = Wallet.objects.get(user=request.user.username).balance
		print("Inside")
		# Locks the selected entry for update
		user_inventory = Inventory.objects.select_for_update().get(user=request.user.username)
		user_wallet = Wallet.objects.select_for_update().get(user=request.user.username)

		BuyOrder.objects.filter(itemID__itemName=list_thing,username=request.user.username).delete()
		messages.info(request,"Buy Order Removed")
		return HttpResponseRedirect(reverse('listings'))			

	return HttpResponseRedirect(reverse('listings'))
