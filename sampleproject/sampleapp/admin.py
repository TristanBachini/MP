from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Item)
admin.site.register(ShoppingCart)
admin.site.register(Type)
admin.site.register(Size)
admin.site.register(PurchaseSelect)
admin.site.register(Month)
admin.site.register(Year)
admin.site.register(Region)
admin.site.register(Order)
admin.site.register(Promo)


