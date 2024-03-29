from django import forms
from django.db import models
from django.db.models import fields
from django.forms import ModelForm, TextInput, PasswordInput, CharField, HiddenInput, NumberInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from django.forms.widgets import Select
from .models import *


class UserForm(UserCreationForm):
    attrs = {'class': 'form-control', 'id': 'floatingInput',
             'placeholder': 'Enter Password', 'required': True}
    password1 = CharField(widget=PasswordInput(attrs=attrs))
    password2 = CharField(widget=PasswordInput(attrs=attrs))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First name', 'aria-label': 'First name', 'required': True}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name', 'aria-label': 'Last name', 'required': True}),
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'aria-label': 'Username', 'required': True}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'aria-label': 'Email', 'required': True}),

        }


class ShoppingCartForm(ModelForm):
    class Meta:
        model = ShoppingCart
        fields = "__all__"
        widgets = {
            'user':  HiddenInput(attrs={'type': 'hidden'}),
            'clothing':  HiddenInput(attrs={'type': 'hidden'}),
            'quantity': NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'size': Select(attrs={'class': 'form-control', 'min': '1'})
        }

class PromoForm(ModelForm):
    class Meta:
        model = Promo
        fields = "__all__"
        widgets = {
            'promo': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'aria-label': 'Email'}),
            'off':  HiddenInput(attrs={'type': 'hidden'})
        }


class PurchaseChoiceForm(ModelForm):
    class Meta:
        model = PurchaseChoice
        fields = "__all__"
        widgets = {
            "choice": Select(attrs={'class': 'form-control', 'min': '1'})
        }


class CreditCardForm(ModelForm):
    class Meta:
        model = CreditCard
        fields = "__all__"
        widgets = {
            'cardnumber': NumberInput(attrs={'class': 'form-control', 'id': 'cardNum', 'placeholder': 'Card Number', 'aria-label': 'Card Number'}),
            'cardpin': NumberInput(attrs={'class': 'form-control', 'id': 'cardPin', 'placeholder': 'Pin', 'aria-label': 'Pin'}),
            "cardmonth": Select(attrs={'class': 'form-control', 'id': 'cardMonth', 'placeholder': 'Month', 'aria-label': 'Month'}),
            "cardyear": Select(attrs={'class': 'form-control', 'id': 'cardYear', 'placeholder': 'Year', 'aria-label': 'Year'}),
        }


class BillingAddressForm(ModelForm):
    class Meta:
        model = Address
        fields = "__all__"
        widgets = {
            'city': TextInput(attrs={'class': 'form-control', 'id': 'city', 'placeholder': 'Ex: Paranaque city', 'aria-label': 'Email', 'required': True}),
            'region': Select(attrs={'class': 'form-control', 'id': 'region', 'placeholder': '', 'aria-label': 'Email', 'required': True}),
            'street1': TextInput(attrs={'class': 'form-control', 'id': 'street1', 'placeholder': 'Ex:  123 Moon Street, West Village, Barangay Moon,', 'aria-label': 'Email', 'required': True}),
            'street2': TextInput(attrs={'class': 'form-control', 'id': 'street1', 'placeholder': 'Block No. Lot No.', 'aria-label': 'Email', 'required': True}),
            'postcode': TextInput(attrs={'class': 'form-control', 'id': 'postcode', 'placeholder': 'Ex: 1707', 'aria-label': 'Email', 'required': True}),
        }


class ShippingAddressForm(ModelForm):
    class Meta:
        model = Address
        fields = "__all__"
        widgets = {
            'city': TextInput(attrs={'class': 'form-control', 'id': 'city', 'placeholder': 'Ex: Paranaque city', 'aria-label': 'Email', 'required': True}),
            'region': Select(attrs={'class': 'form-control', 'id': 'region', 'placeholder': '', 'aria-label': 'Email', 'required': True}),
            'street1': TextInput(attrs={'class': 'form-control', 'id': 'street1', 'placeholder': 'Ex:  123 Moon Street, West Village, Barangay Moon,', 'aria-label': 'Email', 'required': True}),
            'street2': TextInput(attrs={'class': 'form-control', 'id': 'street2', 'placeholder': 'Block No. Lot No.', 'aria-label': 'Email', 'required': True}),
            'postcode': TextInput(attrs={'class': 'form-control', 'id': 'postcode', 'placeholder': 'Ex: 1707', 'aria-label': 'Email', 'required': True}),
        }


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
        widgets = {
            'user':  HiddenInput(attrs={'type': 'hidden'}),
            'shoppingcart':  HiddenInput(attrs={'type': 'hidden'}),
            'date_ordered':  HiddenInput(attrs={'type': 'hidden'}),
            'quantity':  HiddenInput(attrs={'type': 'hidden'}),
            'price':  HiddenInput(attrs={'type': 'hidden'}),
        }
