from .models import *

def get_game_name(id):
    return Game.objects.get(gameID=id).name

def get_inventory(username):

    inventory_items = list(User.objects.get(username=username).inventory.items.all().values())
    for item in inventory_items:
        item.update({'gameName': get_game_name(item['gameID_id'])})
    return inventory_items

