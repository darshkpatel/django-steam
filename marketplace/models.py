from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, MaxLengthValidator
from datetime import date
# Create your models here.
class User(models.Model):
    dob = models.DateField()
    first_name = models.TextField(max_length=50)
    last_name = models.TextField(max_length=50)
    email = models.EmailField()
    recovered_email = models.EmailField()
    username = models.TextField(max_length=25, unique=True, primary_key=True)
    # waller_id = models.ForeignKey
class Game(models.Model):
    name = models.TextField(unique=True)
    price = models.DecimalField(default=0.0, decimal_places=1, max_digits=5)
    gameID = models.AutoField(primary_key=True)
    timesBought = models.IntegerField(default=0)
    releaseDate = models.DateField(default=date.today)
    description = models.TextField()
    ageRating = models.IntegerField(default=7)
    stars = models.DecimalField(validators=[MaxValueValidator(5), MinValueValidator(0)], max_digits=1, decimal_places=1)
class GameReview(models.Model):
    reviews = models.ForeignKey('Review', on_delete=models.CASCADE)
    gameID = models.ForeignKey('Game', on_delete=models.CASCADE)
class GameTags(models.Model):
    tags = models.ForeignKey('Tag', on_delete=models.CASCADE)
    gameID = models.ForeignKey('Game', on_delete=models.CASCADE)

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

class DLCReview(models.Model):
    reviews = models.ForeignKey('Review', on_delete=models.CASCADE)
    DLCid = models.ForeignKey('DLC', on_delete=models.CASCADE)

class DLCTags(models.Model):
    tags = models.ForeignKey('Tag', on_delete=models.CASCADE)
    DLCid = models.ForeignKey('DLC', on_delete=models.CASCADE)

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
    username = models.ForeignKey('User', on_delete=models.CASCADE)
    reviewText = models.TextField(validators=[MinLengthValidator(5)])

class Tag(models.Model):
    tagId = models.AutoField(primary_key=True)
    tag = models.TextField(validators=[MaxLengthValidator(10)])





    