from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.deletion import CASCADE
from django.db.models.fields import Field
from django.db.models.fields.related import ForeignKey

# Create your models here.


class Type(models.Model):
    type = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.type

class Size(models.Model):
    size = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.size


class Item(models.Model):
    name = models.CharField(max_length=100, null=True)
    item_type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True)
    price = models.IntegerField( null=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

class PurchaseSelect(models.Model):
    choice = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.choice 

class PurchaseChoice(models.Model):
    choice = models.ForeignKey(PurchaseSelect,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.choice 

class ShoppingCart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    clothing = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(
        null=True, validators=[MinValueValidator(1)])
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + "'s shopping cart"

class Month(models.Model):
    month = models.IntegerField(null=True, validators=[MinValueValidator(1),MaxValueValidator(12)])

    def __str__(self):
        return str(self.month)

class Day(models.Model):
    day = models.IntegerField(null=True, validators=[MinValueValidator(1),MaxValueValidator(31)])

    def __str__(self):
        return str(self.day)

class Year(models.Model):
    year = models.IntegerField(null=True, validators=[MinValueValidator(2021),MaxValueValidator(2040)])

    def __str__(self):
        return str(self.year)

class CreditCard(models.Model):
    cardnumber = models.BigIntegerField(null=True)
    cardpin = models.IntegerField(null=True, validators=[MinValueValidator(100),MaxValueValidator(999)])
    cardmonth = models.ForeignKey(Month,null=True, on_delete=models.CASCADE)
    cardday = models.ForeignKey(Day,null=True, on_delete=models.CASCADE)
    cardyear = models.ForeignKey(Year,null=True, on_delete=models.CASCADE)

class Region(models.Model):
    region = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.region

class Address(models.Model):
    city = models.CharField(max_length=100, null=True)
    region = models.ForeignKey(Region, on_delete=CASCADE,null=True)
    street1 = models.CharField(max_length=200, null=True,)
    street2 = models.CharField(max_length=200, null=True, blank=True)
    postcode = models.CharField(max_length=10,  null=True, blank=True)


