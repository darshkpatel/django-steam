from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, MaxLengthValidator
from datetime import date
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    dob = models.DateField(null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    recovery_email = models.EmailField()
    username = models.CharField(max_length=25, unique=True, primary_key=True)
class Game(models.Model):
    name = models.CharField(unique=True, max_length=40)
    price = models.DecimalField(default=0.0, decimal_places=1, max_digits=5)
    gameID = models.AutoField(primary_key=True)
    timesBought = models.IntegerField(default=0)
    releaseDate = models.DateField(default=date.today)
    description = models.TextField()
    ageRating = models.IntegerField(default=7)
    stars = models.DecimalField(validators=[MaxValueValidator(5), MinValueValidator(0)], max_digits=1, decimal_places=1)
class GameReview(models.Model):
    review = models.ForeignKey('Review', on_delete=models.CASCADE)
    gameID = models.ForeignKey('Game', on_delete=models.CASCADE)
    class Meta:
         unique_together = ('review', 'gameID')
class GameTags(models.Model):
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    gameID = models.ForeignKey('Game', on_delete=models.CASCADE)
    class Meta:
         unique_together = ('tag', 'gameID')

class DLC(models.Model):
    DLCid = models.AutoField(primary_key=True)
    name = models.TextField(unique=True)
    ageRating = models.IntegerField(default=7)
    stars = models.DecimalField(validators=[MaxValueValidator(5), MinValueValidator(0)], max_digits=1, decimal_places=1)
    reviews = models.ForeignKey('Review', on_delete=models.CASCADE)
    tags = models.ForeignKey('Tag', on_delete=models.CASCADE)
    timesBought = models.IntegerField(default=0)

class gameDLC(models.Model):
    gameID = models.ForeignKey('Game', on_delete=models.CASCADE)
    DLCid = models.ForeignKey('DLC', on_delete=models.CASCADE)
    class Meta:
         unique_together = ('gameID', 'DLCid')
class DLCReview(models.Model):
    review = models.ForeignKey('Review', on_delete=models.CASCADE)
    DLCid = models.ForeignKey('DLC', on_delete=models.CASCADE)
    class Meta:
         unique_together = ('review', 'DLCid')

class DLCTags(models.Model):
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    DLCid = models.ForeignKey('DLC', on_delete=models.CASCADE)
    class Meta:
         unique_together = ('tag', 'DLCid')

class Item(models.Model):
    itemID = models.AutoField(primary_key=True)
    gameID = models.ForeignKey('Game', on_delete=models.CASCADE)
    newItemPrice = models.DecimalField(default=0.0, decimal_places=1, max_digits=5)
    itemDescription = models.TextField(validators=[MinLengthValidator(5)])
    itemName = models.TextField(unique=True)
    CONDITION_CHOICES = [
    ('FN', 'Factory New'),
    ('FT', 'Field Tested'),
    ('BS', 'Battle Scarred'),
]
    itemCondition = models.CharField(choices=CONDITION_CHOICES, max_length=2, default='FN')
    photoLocation = models.FilePathField(default="./images/items/", allow_folders=True)

class Review(models.Model):
    reviewId = models.AutoField(primary_key=True)
    username = models.ForeignKey('Profile', on_delete=models.CASCADE)
    reviewText = models.TextField(validators=[MinLengthValidator(5)])

class Tag(models.Model):
    tagId = models.AutoField(primary_key=True)
    tag = models.TextField(validators=[MaxLengthValidator(10)])

class Transaction(models.Model):
    credited_to = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='creditor')
    debited_from = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='debitor')
    amount = models.DecimalField(default=0.0, decimal_places=1, max_digits=5)
    transactionID = models.AutoField(primary_key=True)
class Wallet(models.Model):
    foreignKey = models.OneToOneField('User', on_delete=models.CASCADE, unique=True)
    balance = models.DecimalField(default=0.0, decimal_places=1, max_digits=5)
    transactions = models.ManyToManyField(Transaction, through='WalletTransaction')


class WalletTransaction(models.Model):
    transactionID = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    WalletID = models.ForeignKey('Wallet', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    CONDITION_CHOICES = [
    ('CR', 'Credit'),
    ('DR', 'Debit'),
    ]
    transactionType = models.CharField(choices=CONDITION_CHOICES, max_length=2)


class Inventory(models.Model):
    Profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    isPublic = models.BinaryField(default=1)
    items = models.ManyToManyField('Item')
    games = models.ManyToManyField('Game')

class SellOrder(models.Model):
    itemID = models.ForeignKey('Item', on_delete=models.CASCADE)
    listingDate = models.DateTimeField(auto_now_add=True)
    sellingPrice = models.DecimalField(default=0.0, decimal_places=1, max_digits=5)
    username = models.ForeignKey('Profile', on_delete=models.CASCADE)
    sellorderID = models.AutoField(primary_key=True)
class BuyOrder(models.Model):
    itemID = models.ForeignKey('Item', on_delete=models.CASCADE)
    listingDate = models.DateTimeField(auto_now_add=True)
    buyPrice = models.DecimalField(default=0.0, decimal_places=1, max_digits=5)
    username = models.ForeignKey('Profile', on_delete=models.CASCADE)
    BuyID = models.AutoField(primary_key=True)

class FullfilledOrder(models.Model):
    buyorder = models.ForeignKey('BuyOrder', on_delete=models.CASCADE)
    sellOrder = models.ForeignKey('SellOrder', on_delete=models.CASCADE)
    fulfillmentDate = models.DateTimeField(auto_now_add=True)
    fulfillmentPrice = models.DecimalField(default=0.0, decimal_places=1, max_digits=5)

