from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
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
