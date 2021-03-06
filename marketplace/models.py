from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, MaxLengthValidator
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class User(AbstractUser):
    dob = models.DateField(null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    recovery_email = models.EmailField()
    username = models.CharField(max_length=25, unique=True, primary_key=True)

class Game(models.Model):
    name = models.CharField(unique=True, max_length=40, primary_key=True)
    price = models.DecimalField(default=0.0, decimal_places=1, max_digits=5)
    timesBought = models.IntegerField(default=0)
    releaseDate = models.DateField(default=date.today)
    description = models.TextField()
    ageRating = models.IntegerField(default=7)
    def __str__(self):
        return self.name
    
class GameReview(models.Model):
    review = models.ForeignKey('Review', on_delete=models.CASCADE, primary_key=True)
    name = models.ForeignKey('Game', on_delete=models.CASCADE)
    stars = models.DecimalField(validators=[MaxValueValidator(5), MinValueValidator(0)], max_digits=2, decimal_places=1)
    class Meta:
         unique_together = ('review', 'name')


class GameTags(models.Model):
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    gameID = models.ForeignKey('Game', on_delete=models.CASCADE)
    class Meta:
         unique_together = ['tag', 'gameID']

class DLC(models.Model):
    name = models.CharField(unique=True, max_length=50, primary_key=True)
    ageRating = models.IntegerField(default=7)
    description = models.TextField()

    # stars = models.DecimalField(validators=[MaxValueValidator(5), MinValueValidator(0)], max_digits=2, decimal_places=1)
    # reviews = models.ForeignKey('Review', on_delete=models.CASCADE)
    # tags = models.ForeignKey('Tag', on_delete=models.CASCADE)
    def __str__(self):
        return self.name
class gameDLC(models.Model):
    gameID = models.ForeignKey('Game', on_delete=models.CASCADE)
    DLCid = models.ForeignKey('DLC', on_delete=models.CASCADE)
    timesBought = models.IntegerField(default=0)
    class Meta:
         unique_together = ('gameID', 'DLCid')
    def __str__(self):
        return self.DLCid.name
class DLCReview(models.Model):
    review = models.ForeignKey('Review', on_delete=models.CASCADE, primary_key=True)
    DLCname = models.ForeignKey('DLC', on_delete=models.CASCADE)
    stars = models.DecimalField(validators=[MaxValueValidator(5), MinValueValidator(0)], max_digits=2, decimal_places=1, null=False)
    compatibility = models.DecimalField(validators=[MaxValueValidator(5), MinValueValidator(0)], max_digits=2, decimal_places=1, null=True)

    class Meta:
         unique_together = ['review', 'DLCname']

class DLCTags(models.Model):
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    DLCid = models.ForeignKey('DLC', on_delete=models.CASCADE)
    class Meta:
         unique_together = (('tag', 'DLCid'),)

class Item(models.Model):
    itemID = models.AutoField(primary_key=True)
    gameID = models.ForeignKey('Game', on_delete=models.CASCADE)
    newItemPrice = models.DecimalField(default=0.0, decimal_places=1, max_digits=5)
    itemDescription = models.TextField(validators=[MinLengthValidator(5)])
    itemName = models.CharField(unique=True, max_length=50)
    CONDITION_CHOICES = [
    ('FN', 'Factory New'),
    ('FT', 'Field Tested'),
    ('BS', 'Battle Scarred'),
    ]
    itemCondition = models.CharField(choices=CONDITION_CHOICES, max_length=2, default='FN')
    # photoLocation = models.FilePathField(default="./images/items/", allow_folders=True)
    def __str__(self):
        return self.itemName
class Review(models.Model):
    reviewId = models.AutoField(primary_key=True)
    username = models.ForeignKey('User', on_delete=models.CASCADE)
    reviewText = models.TextField(validators=[MinLengthValidator(5)])
    time = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    tagId = models.AutoField(primary_key=True)
    tag = models.CharField(validators=[MaxLengthValidator(10)], max_length=20)
    def __str__(self):
        return self.tag
class Transaction(models.Model):
    credited_to = models.ForeignKey('User', on_delete=models.CASCADE, related_name='creditor')
    debited_from = models.ForeignKey('User', on_delete=models.CASCADE, related_name='debitor')
    amount = models.DecimalField(default=0.0, decimal_places=1, max_digits=5)
    transactionID = models.AutoField(primary_key=True)
class Wallet(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, unique=True, primary_key=True)
    balance = models.DecimalField(default=0.0, decimal_places=1, max_digits=30)
    transactions = models.ManyToManyField(Transaction, through='WalletTransaction')
    def __str__(self):
        return self.user.username
# Create wallet for user when user is created
@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_wallet(sender, instance, **kwargs):
    instance.wallet.save()

class Inventory(models.Model):
# Create Inventory for user when user is created
    user = models.OneToOneField('User', on_delete=models.CASCADE, unique=True, primary_key=True)
    isPublic = models.BooleanField(default=True)
    items = models.ManyToManyField('Item')
    games = models.ManyToManyField('Game')
    def __str__(self):
        return "Inventory: " + self.user.username
    
@receiver(post_save, sender=User)
def create_inventory(sender, instance, created, **kwargs):
    if created:
        Inventory.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_inventory(sender, instance, **kwargs):
    instance.inventory.save()
 
class WalletTransaction(models.Model):
    transactionID = models.OneToOneField('Transaction', on_delete=models.CASCADE, primary_key=True)
    WalletUser = models.ForeignKey('Wallet', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    CONDITION_CHOICES = [
    ('CR', 'Credit'),
    ('DR', 'Debit'),
    ]
    transactionType = models.CharField(choices=CONDITION_CHOICES, max_length=2)



class SellOrder(models.Model):
    itemID = models.ForeignKey('Item', on_delete=models.CASCADE)
    listingDate = models.DateTimeField(auto_now_add=True)
    sellingPrice = models.DecimalField(default=0.0, decimal_places=1, max_digits=5)
    username = models.ForeignKey('User', on_delete=models.CASCADE)
    sellorderID = models.AutoField(primary_key=True)
class BuyOrder(models.Model):
    itemID = models.ForeignKey('Item', on_delete=models.CASCADE)
    listingDate = models.DateTimeField(auto_now_add=True)
    buyPrice = models.DecimalField(default=0.0, decimal_places=1, max_digits=5)
    username = models.ForeignKey('User', on_delete=models.CASCADE)
    BuyID = models.AutoField(primary_key=True)

class FullfilledOrder(models.Model):
    buyorder = models.ForeignKey('BuyOrder', on_delete=models.CASCADE)
    sellOrder = models.ForeignKey('SellOrder', on_delete=models.CASCADE)
    fulfillmentDate = models.DateTimeField(auto_now_add=True)
    fulfillmentPrice = models.DecimalField(default=0.0, decimal_places=1, max_digits=5)

