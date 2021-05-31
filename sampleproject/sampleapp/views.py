from .models import *
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from dal import autocomplete
from .forms import *

# Create your views here.


def homepage(request):
    items = Item.objects.all()
    itemsdict = []

    for item in items:
        form = ShoppingCartForm(
            {"user": request.user.id, "clothing": item.id, "quantity": 1})
        itemsdict.append({"item": item, "form": form})

    data = {"itemsdict": itemsdict}
    return render(request, 'sampleapp/homepage.html', data)


def products(request, pk):
    item = Item.objects.get(id=pk)
    shoppingcartform = ShoppingCartForm({"user": request.user.id, "clothing": item.id, "quantity": 1})
    data = {"item": item, "shoppingcartform":shoppingcartform}

    
    return render(request, 'sampleapp/products.html', data)


def register(request):
    form = UserForm()

    if(request.method == "POST"):
        form = UserForm(request.POST)
        if(form.is_valid()):
            subject = "Vermin registration"
            message = "<h1>Hello " + request.POST.get(
                'username')+", good day!</h1> <br><br>This is to inform you that you have recently signed up with vermin."
            from_email = settings.EMAIL_HOST_USER
            recepient_list = [request.POST.get('email')]

            # send_mail(subject, message, from_email, recepient_list)
            email = EmailMessage(
                subject,
                message,
                from_email,
                recepient_list
            )

            email.content_subtype = 'html'
            email.send()

            print(request.POST.get('email'))
            form.save()
            print(request)
            messages.success(request, "Account was created for " +
                             form.cleaned_data.get("username"))

            return redirect('/login')

    data = {"form": form}
    return render(request, 'sampleapp/register.html', data)


def login_page(request):
    if(request.method == "POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("Login Success.")
            return redirect('/')
        else:
            print("Login Failed.")
            messages.error(request, "Incorrect password or username")

    return render(request, 'sampleapp/login.html')


def aboutus(request):
    return render(request, 'sampleapp/aboutus.html')


def logout_page(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='/login')
def add_to_cart(request):
    if(request.user.is_superuser):
        return render(request,'sampleapp/homepage.html')
    else:
        form = ShoppingCartForm(request.POST)
        print(form)
        if(form.is_valid()):
            form.save()
            return redirect('/cart')


@login_required(login_url='/login')
def cart(request):
    items = ShoppingCart.objects.filter(user=request.user).order_by('id')
    cart = []
    cum_price = 0
    item_count = 0
    for item in items:
        cum_price = cum_price + (item.quantity * item.clothing.price)
        item_count = item_count + item.quantity
        form = ShoppingCartForm(
            {"user": item.user.id, "clothing": item.clothing.id, "quantity": item.quantity})
        cart.append({"item": item, "form": form})

    data = {"cart": cart, "cum_price": cum_price, "item_count": item_count}
    return render(request, 'sampleapp/cart.html', data)


@login_required(login_url='login')
def update_item(request, pk):
    cartitem = ShoppingCart.objects.get(id=pk)
    cartitemform = ShoppingCartForm(instance=cartitem)

    if(request.method == 'POST'):
        cartitem = ShoppingCart.objects.get(id=pk)
        form = ShoppingCartForm(request.POST, instance=cartitem)
        if(form.is_valid()):
            form.save()
            return redirect("/cart")

    data = {"cartitemform": cartitemform}
    return render(request, "sampleapp/updatecartitem.html", data)


@login_required(login_url='login')
def delete_item(request, pk):
    shoppingcart = ShoppingCart.objects.get(id=pk)
    shoppingcart.delete()
    return redirect("/cart")

@login_required(login_url='login')
def purchase_choice(request):
    purchasechoiceform = PurchaseChoiceForm()
    data = {"purchasechoiceform":purchasechoiceform}
    return render(request, "sampleapp/modeofpayment.html",data)

@login_required(login_url='login')
def purchase_step2(request):

    if(request.POST.get('choice')=="3" or request.POST.get('choice')=="2"):
        return render(request, "sampleapp/creditdebit.html")
    if(request.POST.get('choice')=="4"):
        return render(request, "sampleapp/cashondelivery.html")
