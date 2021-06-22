from django.db.models import fields
import django_filters
from django_filters import DateFilter

from .models import *


class CartFilter(django_filters.FilterSet):
    class Meta:
        model = ShoppingCart
        fields = '__all__'
        exclude = ['user', 'date_created']


class OrderFilter(django_filters.FilterSet):

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['user', 'shoppingcart']
