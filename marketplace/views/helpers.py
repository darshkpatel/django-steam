from marketplace.models import *
from datetime import datetime

""" 
ToDo: 
    - Put Raw Queries for Review

"""

def get_game_name(id):
    """
        Mostly Depriciated. 
    """
    return Game.objects.get(name=id).name


def get_inventory_items(username):
    inventory_items = list(User.objects.get(username=username).inventory.items.all().values())
    for item in inventory_items:
        item.update({'gameName': item['gameID_id']})
    return inventory_items


def get_item_details(itemID):
    item_codes = {'FN':'Factory New',
                    'FT':'Field Tested',
                    'BS':'Battle Scarred'}
    details = {
        'itemCondition': item_codes[list(Item.objects.filter(itemID=itemID).values())[0]['itemCondition']],
        'itemGame': list(Item.objects.filter(itemID=itemID).values())[0]['gameID_id'],
        'itemName': list(Item.objects.filter(itemID=itemID).values())[0]['itemName']
        }
    return details


def get_sell_orders():
    item_codes = {'FN':'Factory New',
                    'FT':'Field Tested',
                    'BS':'Battle Scarred'}
    sell_orders = list(SellOrder.objects.all().values())
    for order in sell_orders:
        order.update(get_item_details(order['itemID_id']))
        order.update({'listingDate': order['listingDate'].strftime('%D at %T')})
        order.update({'sellingPrice': str(order['sellingPrice'])})
        # order.update({'itemCondition': item_codes[order['itemCondition']]})
    return sell_orders

def get_buy_orders():
    item_codes = {'FN':'Factory New',
                    'FT':'Field Tested',
                    'BS':'Battle Scarred'}
    buy_orders = list(BuyOrder.objects.all().values())
    for order in buy_orders:
        order.update(get_item_details(order['itemID_id']))
        order.update({'listingDate': order['listingDate'].strftime('%D at %T')})
        order.update({'buyPrice': str(order['buyPrice'])})
        # order.update({'itemCondition': item_codes[order['itemCondition']]})
    return buy_orders

def get_games():
    games = Game.objects.all().values()
    for game in games:
        game.update( {'price': float(game['price'])} )
        game.update({'releaseDate': game['releaseDate'].strftime('%d %B %Y') })
    return games