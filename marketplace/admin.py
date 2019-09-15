from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Game)
admin.site.register(User)
admin.site.register(GameReview)
admin.site.register(GameTags)
admin.site.register(DLC)
admin.site.register(gameDLC)
admin.site.register(DLCReview)
admin.site.register(DLCTags)
admin.site.register(Item)
admin.site.register(Review)
admin.site.register(Tag)
admin.site.register(Transaction)
admin.site.register(WalletTransaction)
admin.site.register(Inventory)
admin.site.register(Wallet)
admin.site.register(SellOrder)
admin.site.register(BuyOrder)
admin.site.register(FullfilledOrder)


