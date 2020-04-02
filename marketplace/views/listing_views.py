from marketplace.common_imports import *
from django.core import serializers
from django.db import transaction

def process_transaction(from_user,to_user,amount):
	from_user_balance = Wallet.objects.get(user=from_user).balance
	print(f"Balance for {from_user} is {from_user_balance}")
	to_user_balance = Wallet.objects.get(user=to_user).balance
	print(f"Balance for {to_user} is {to_user_balance}")
	# Locks the selected entry for update
	with transaction.atomic():
		from_user_wallet = Wallet.objects.select_for_update().get(user=from_user)
		to_user_wallet = Wallet.objects.select_for_update().get(user=to_user)

		if(float(from_user_balance)>=float(amount)):
			from_user_wallet.balance = float(from_user_wallet.balance) - amount
			to_user_wallet.balance = float(to_user_wallet.balance) + amount
			print(f"Transaction of {amount} Complete")
		else:
			return "Insufficient Balance"				

		from_user_wallet.save()
		to_user_wallet.save()

		from_user_balance = Wallet.objects.get(user=from_user).balance
		to_user_balance = Wallet.objects.get(user=to_user).balance

		print(f"Balance for {from_user} is {from_user_balance}")
		print(f"Balance for {to_user} is {to_user_balance}")

		return True


def transfer_item(from_user,to_user,itemName):
	with transaction.atomic():
		from_user_inventory = Inventory.objects.select_for_update().get(user=from_user)
		to_user_inventory = Inventory.objects.select_for_update().get(user=to_user)
		# if (not to_user_inventory.items.filter(itemName=itemName)) and from_user!=to_user and  (from_user_inventory.items.filter(itemName=itemName)):
		item = Item.objects.get(itemName=itemName)
		to_user_inventory.items.add(item)
		from_user_inventory.items.remove(item)
		to_user_inventory.save()
		from_user_inventory.save()
		print(f"Transferred {itemName} from {from_user} to {to_user}")
		return True



def process_sell_order(order, request):
	# Find Buy Order 
	buy_order = BuyOrder.objects.filter(buyPrice__gte=order.sellingPrice).exclude(username=order.username).order_by('listingDate')
	if buy_order:
		buy_order=buy_order[0]
		print("Matching Buy Order Found")
		transfer_item(order.username.username, buy_order.username.username, buy_order.itemID.itemName)
		process_transaction(buy_order.username.username, order.username, float(buy_order.buyPrice))
		print("Processing Transaction")
		print("Deleting Transactions")
		BuyOrder.objects.filter(buyPrice__gte=order.sellingPrice).exclude(username=order.username).order_by('listingDate')[0].delete()
		SellOrder.objects.filter(sellingPrice=order.sellingPrice, username=order.username).order_by('listingDate')[0].delete()

		return True

	return False

def process_buy_order(order, request):
	# Find Buy Order 

	sell_order = SellOrder.objects.filter(sellingPrice__lte=order.buyPrice).exclude(username=order.username).order_by('listingDate')
	if sell_order:
		sell_order=sell_order[0]
		print("Matching Buy Order Found")
		transfer_item(sell_order.username.username, order.username, sell_order.itemID.itemName)
		process_transaction(order.username, sell_order.username.username, float(order.buyPrice))
		print("Processing Transaction")
		SellOrder.objects.filter(sellingPrice__lte=order.buyPrice).exclude(username=order.username).order_by('listingDate')[0].delete()
		BuyOrder.objects.filter(buyPrice=order.buyPrice, username=order.username).order_by('listingDate')[0].delete()

		return True
	return False

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
		with transaction.atomic():
			user = User.objects.get(username=request.user.username)
			user_inventory = Inventory.objects.select_for_update().get(user=request.user.username)
			item = user_inventory.items.get(itemName=sell_thing)
			if item:

				# txn = WalletTransaction()	
				sell_order = SellOrder(itemID=item, sellingPrice=price, username=user)
				user_inventory.items.remove(item)
				user_inventory.save()
				sell_order.save()
				if process_sell_order(sell_order, request):
					messages.info(request,"Matching Buy Order Fulfilled")
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

			# txn = WalletTransaction()	select_for
		with transaction.atomic():
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
		with transaction.atomic():
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
		with transaction.atomic():
			user_balance = Wallet.objects.get(user=request.user.username).balance
			print("Inside")
			# Locks the selected entry for update
			user_inventory = Inventory.objects.select_for_update().get(user=request.user.username)
			user_wallet = Wallet.objects.select_for_update().get(user=request.user.username)

			if not user_inventory.items.filter(itemName=buy_thing):
				item_id = Item.objects.get(itemName=buy_thing)
				if not BuyOrder.objects.filter(itemID=item_id, username=User.objects.get(username=request.user.username)):
					buy_obj = BuyOrder(itemID=item_id, buyPrice=price, username=User.objects.get(username=request.user.username))
					buy_obj.save()
					messages.info(request,"Buy Order Added")
					if process_buy_order(buy_obj, request):
						messages.info(request,"Fulfilled Sell Order")


				else:
					messages.warning(request,"Buy order for item already placed")
				return HttpResponseRedirect(reverse('listings'))			

			else:
				messages.warning(request,"You already own the item")
				return HttpResponseRedirect(reverse('listings'))			
		
	return HttpResponseRedirect(reverse('listings'))

@login_required(login_url='/accounts/login')
def delete_buy_order(request):
	list_thing = request.GET.get('list_thing', None)
	if list_thing:
		with transaction.atomic():
			user_balance = Wallet.objects.get(user=request.user.username).balance
			print("Inside")
			# Locks the selected entry for update
			user_inventory = Inventory.objects.select_for_update().get(user=request.user.username)
			user_wallet = Wallet.objects.select_for_update().get(user=request.user.username)

			BuyOrder.objects.filter(itemID__itemName=list_thing,username=request.user.username).delete()
			messages.info(request,"Buy Order Removed")
			return HttpResponseRedirect(reverse('listings'))			

	return HttpResponseRedirect(reverse('listings'))
