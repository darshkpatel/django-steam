from marketplace.common_imports import *
from django.db import transaction

@login_required(login_url='/accounts/login')
@transaction.atomic
def index(request):
    buy_game = request.GET.get('buy_game', None)
    
    if buy_game:
        game = Game.objects.get(name=buy_game)
        user_balance = Wallet.objects.get(user=request.user.username).balance

        if user_balance<game.price:
            messages.warning(request,"Insufficient funds in your wallet")
            return HttpResponseRedirect(reverse('games'))
            
        # Locks the selected entry for update
        user_inventory = Inventory.objects.select_for_update().get(user=request.user.username)
        user_wallet = Wallet.objects.select_for_update().get(user=request.user.username)

        if game in user_inventory.games.all():
            messages.warning(request,"You already own the game")
            return HttpResponseRedirect(reverse('games'))


        user_wallet.balance = user_wallet.balance - game.price
        user_inventory.games.add(game)


        #Commits to DB
        user_inventory.save()
        user_wallet.save(update_fields=['balance'])


        messages.info(request,"Game has been added to your inventory")
        return HttpResponseRedirect(reverse('games'))

            


        


    context = {
        "games" : get_games()
    }

    return render(request, "marketplace/games.html", context)
