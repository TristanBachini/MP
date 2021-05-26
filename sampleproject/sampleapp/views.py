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
    # shopitems=ShopItem.objects.all()
    # data = {"shopitems":shopitems}

    items = Item.objects.all()
    itemsdict = []
    
    for item in items:
        form = ShoppingCartForm({"user": request.user.id, "clothing": item.id, "quantity": 1})
        itemsdict.append({"item": item, "form": form})

    data = {"itemsdict": itemsdict}
    return render(request, 'sampleapp/homepage.html', data)

def add_to_cart(request):
    form = ShoppingCartForm(request.POST)
    print(form)
    if( form.is_valid() ):
        form.save()
        return redirect('/cart')
    



def register(request):
    form = UserForm()

    if(request.method == "POST"):
        form = UserForm(request.POST)
        if(form.is_valid()):
            subject = "Vermin registration"
            message = "<h1>Hello " + request.POST.get('username')+", good day!</h1> <br><br>This is to inform you that you have recently signed up with vermin"
            from_email = settings.EMAIL_HOST_USER
            recepient_list = [request.POST.get('email')]

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
def cart(request):
    items = ShoppingCart.objects.filter(user=request.user).order_by('id')
    cart = []
    cum_price = 0
    item_count = 0
    for item in items:
        cum_price = cum_price + (item.quantity * item.clothing.price)
        item_count = item_count + item.quantity
        form = ShoppingCartForm({"user": item.user.id, "clothing": item.clothing.id, "quantity": item.quantity})
        cart.append({"item":item, "form": form})

    data = {"cart": cart, "cum_price": cum_price, "item_count": item_count}
    return render(request, 'sampleapp/cart.html', data)

@login_required(login_url='login')
def update_item(request,pk):
    cartitem = ShoppingCart.objects.get(id=pk)
    cartitemform = ShoppingCartForm(instance=cartitem)

    if(request.method=='POST'):
        cartitem = ShoppingCart.objects.get(id=pk)
        form =  ShoppingCartForm(request.POST, instance=cartitem)
        if(form.is_valid()):
            form.save()
            return redirect("/cart")

    data = {"cartitemform": cartitemform}
    return render(request, "sampleapp/updatecartitem.html",data)


@login_required(login_url='login')
def delete_item(request,pk):
    shoppingcart = ShoppingCart.objects.get(id=pk)
    shoppingcart.delete()
    return redirect("/cart")


