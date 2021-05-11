from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Item(models.Model):
    name = models.CharField (max_length=100, null=True)
    price = models.FloatField()
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name
    

class ShoppingCart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity=models.IntegerField(null=True,validators=[MinValueValidator(1)])
    date_created = models.DateTimeField(auto_now_add=True, null=True)

class ShopItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.item.name