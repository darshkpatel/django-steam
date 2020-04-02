from marketplace.common_imports import *
from django.core import serializers


@login_required(login_url='/accounts/login')
def market(request):
	context = {
		"balance":float(User.objects.get(username=request.user.username).wallet.balance),
		"items" : get_inventory_items(request.user.username),
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
def buy(request):
	buy_thing = request.GET.get('buy_thing', None)
	price = float(request.GET.get('price', None))
	seller = request.GET.get('seller', None)


	if buy_thing:
		with transaction.atomic():
			user_balance = Wallet.objects.get(user=request.user.username).balance

			# Locks the selected entry for update
			user_inventory = Inventory.objects.select_for_update().get(user=request.user.username)
			buyer_wallet = Wallet.objects.select_for_update().get(user=request.user.username)
			seller_wallet = Wallet.objects.select_for_update().get(user=seller)

			if not user_inventory.items.filter(itemName=buy_thing) and seller!=request.user.username:

				#Transaction process

				#Debit buyer, credit seller 
				if(float(user_balance)>=float(price)):
					buyer_wallet.balance = float(buyer_wallet.balance) - price
					seller_wallet.balance = float(seller_wallet.balance) + price

					item = Item.objects.get(itemName=buy_thing)
					user_inventory.items.add(item)

					SellOrder.objects.filter(itemID__itemName=buy_thing,username=seller).delete()


					buyer_wallet.save(update_fields=['balance'])
					seller_wallet.save(update_fields=['balance'])

					

				else:
					messages.warning(request,"Insufficient Balance")
					return HttpResponseRedirect(reverse('market'))			

				#Remove Sell Order

				messages.warning(request,"Bought")
				return HttpResponseRedirect(reverse('market'))			
			else:
				messages.warning(request,"You already own the item or You're the seller")
				return HttpResponseRedirect(reverse('market'))	
		
	return HttpResponseRedirect(reverse('market'))
