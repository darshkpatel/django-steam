from .models import *
from datetime import datetime

""" 
ToDo: 
    - Put Raw Queries for Review

"""

def get_game_name(id):
    return Game.objects.get(gameID=id).name

def get_inventory(username):

    inventory_items = list(User.objects.get(username=username).inventory.items.all().values())
    for item in inventory_items:
        item.update({'gameName': get_game_name(item['gameID_id'])})
    return inventory_items

def get_games():
    games = Game.objects.all().values()
    for game in games:
        game.update( {'price': float(game['price'])} )
        game.update({'releaseDate': game['releaseDate'].strftime('%d %B %Y') })
    return games