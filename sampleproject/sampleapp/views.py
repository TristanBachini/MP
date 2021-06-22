from os import name
from django.db.models.query import QuerySet
from django.db.models.query_utils import select_related_descend
from django.forms.widgets import DateTimeBaseInput
from .models import *
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from .forms import *
from .filters import *

from django.template.loader import get_template
from xhtml2pdf import pisa

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
    shoppingcartform = ShoppingCartForm(
        {"user": request.user.id, "clothing": item.id, "quantity": 1})
    data = {"item": item, "shoppingcartform": shoppingcartform}

    return render(request, 'sampleapp/products.html', data)


def search(request):
    if request.method == "POST":
        searched = request.POST.get('searched')
        items = Item.objects.filter(name__icontains=searched)
        itemsdict = []
        # flag = True
        # if searched == None:
        #     flag = False

        for item in items:
            form = ShoppingCartForm(
                {"user": request.user.id, "clothing": item.id, "quantity": 1}
            )
            itemsdict.append({"item": item, "form": form})
    data = {"itemsdict": itemsdict, "searched": searched}
    return render(request, 'sampleapp/search.html', data)
    # return render(request, 'sampleapp/search.html', {"searched": searched})


def collections(request):
    items = Item.objects.all()
    itemsdict = []

    for item in items:
        form = ShoppingCartForm(
            {"user": request.user.id, "clothing": item.id, "quantity": 1})
        itemsdict.append({"item": item, "form": form})

    data = {"itemsdict": itemsdict}
    return render(request, 'sampleapp/collections.html', data)


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
            form.save()
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

    return render(request, 'sampleapp/login.html')


def aboutus(request):
    return render(request, 'sampleapp/aboutus.html')


def logout_page(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='/login')
def add_to_cart(request):
    if(request.user.is_superuser):
        items = Item.objects.all()
        itemsdict = []

        for item in items:
            form = ShoppingCartForm(
                {"user": request.user.id, "clothing": item.id, "quantity": 1})
            itemsdict.append({"item": item, "form": form})

        data = {"itemsdict": itemsdict}
        return render(request, 'sampleapp/collections.html', data)
    else:
        form = ShoppingCartForm(request.POST)
        print(form)
        if(form.is_valid()):
            quantity = form.cleaned_data.get('quantity')
            itemid = form.cleaned_data.get('clothing')
            print(itemid)
            item = Item.objects.get(name=itemid)

            if(item.stock < quantity):
                messages.error(
                    request, "There is currently not enough stock to fulfill the quantity you have ordered")
                items = Item.objects.all()
                itemsdict = []

                for item in items:
                    form = ShoppingCartForm(
                        {"user": request.user.id, "clothing": item.id, "quantity": 1})
                    itemsdict.append({"item": item, "form": form})

                data = {"itemsdict": itemsdict}
                return render(request, 'sampleapp/collections.html', data)
            else:
                form.save()
                return redirect('/cart')


@login_required(login_url='/login')
def cart(request):
    items = ShoppingCart.objects.filter(user=request.user).order_by('id')
    filter = CartFilter(request.GET, queryset=items)
    items = filter.qs
    cart = []
    cum_price = 0
    item_count = 0
    for item in items:
        cum_price = cum_price + (item.quantity * item.clothing.price)
        item_count = item_count + item.quantity
        form = ShoppingCartForm(
            {"user": item.user.id, "clothing": item.clothing.id, "quantity": item.quantity})
        cart.append({"item": item, "form": form})

    cum_price_decimal = "{:.2f}".format(cum_price)
    cum_price = float(cum_price_decimal)

    data = {"cart": cart, "cum_price": cum_price,
            "item_count": item_count, "filter": filter}
    return render(request, 'sampleapp/cart.html', data)


@login_required(login_url='login')
def update_item(request, pk):
    cartitem = ShoppingCart.objects.get(id=pk)
    cartitemform = ShoppingCartForm(request.POST, instance=cartitem)
    if(cartitemform.is_valid()):

        cartitemform.save()

    return redirect("/cart")


@login_required(login_url='login')
def delete_item(request, pk):
    shoppingcart = ShoppingCart.objects.get(id=pk)
    shoppingcart.delete()
    return redirect("/cart")


@login_required(login_url='login')
def purchase_choice(request):
    purchasechoiceform = PurchaseChoiceForm()
    data = {"purchasechoiceform": purchasechoiceform}
    return render(request, "sampleapp/modeofpayment.html", data)


@login_required(login_url='login')
def purchase_step2(request):

    choice = request.POST.get('choice')
    # select = PurchaseSelect.objects.get(pk=choice)

    if(choice == "16" or choice == "17"):
        creditcardform = CreditCardForm()
        billingaddressform = BillingAddressForm()
        shippingaddressform = ShippingAddressForm()
        data = {"creditcardform": creditcardform, "billingaddressform":
                billingaddressform, "shippingaddressform": shippingaddressform}
        return render(request, "sampleapp/creditdebit.html", data)
    if(choice == "18"):
        shippingaddressform = ShippingAddressForm()
        data = {"shippingaddressform": shippingaddressform}
        return render(request, "sampleapp/cashondelivery.html", data)


@login_required(login_url='login')
def finalize(request):
    promocode = request.POST.get('promocode')
    promo = Promo.objects.filter(promo=promocode)
    discountpercent = 0
    if(promo):
        discountpercent = float(promo[0].off)
    else:
        promocode = "None"
    billingaddressform = BillingAddressForm(request.POST)
    shippingaddressform = ShippingAddressForm(request.POST)
    creditcardform = CreditCardForm(request.POST)
    if(shippingaddressform.is_valid() and billingaddressform.is_valid() and creditcardform.is_valid()):
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

        cum_price += 50
        cum_price_decimal = "{:.2f}".format(cum_price)
        cum_price = float(cum_price_decimal)
        discount = cum_price*discountpercent
        cum_price -= discount

        region = str(shippingaddressform.cleaned_data.get('region'))
        regionbill = str(billingaddressform.cleaned_data.get('region'))
        cardnumber = str(creditcardform.cleaned_data.get('cardnumber'))[-4:]

        shippingaddress = shippingaddressform.cleaned_data.get('street2') + " " + shippingaddressform.cleaned_data.get(
            'street1') + ", " + shippingaddressform.cleaned_data.get('city') + ", " + region + ", " + shippingaddressform.cleaned_data.get('postcode')
        billingaddress = billingaddressform.cleaned_data.get('street2') + " " + billingaddressform.cleaned_data.get(
            'street1') + ", " + billingaddressform.cleaned_data.get('city') + ", " + regionbill + ", " + billingaddressform.cleaned_data.get('postcode')
        data = {"cart": cart, "cum_price": cum_price, "item_count": item_count,
                "shippingaddress": shippingaddress, "billingaddress": billingaddress, "cardnumber": cardnumber, "promocode": promocode, "discount": discount}

        return render(request, "sampleapp/finalize.html", data)
    elif(request.method == "GET"):

        subject = "Order Details"
        message = "<h1>Hello " + request.user.username + \
            ", good day!</h1> <br><br>Here is a summary of your order:"
        from_email = settings.EMAIL_HOST_USER
        recepient_list = [request.user.email]

        email = EmailMessage(
            subject,
            message,
            from_email,
            recepient_list
        )

        email.content_subtype = 'html'
        pdf = generate_pdf(request).getvalue()
        email.attach("receipt.pdf", pdf, 'application/pdf')
        email.send()
        items = ShoppingCart.objects.filter(user=request.user).order_by('id')
        for item in items:
            order = OrderForm({"user": request.user.id, "shoppingcart": item.clothing.name, "date_ordered": datetime.date.today(),
                               "quantity": item.quantity, "price": item.clothing.price})
            if(order.is_valid()):
                order.save()

        for item in items:
            stockitem = Item.objects.get(name=item.clothing)
            stockitem.stock = stockitem.stock - item.quantity
            stockitem.save()
            item.delete()

        items = Item.objects.all()
        itemsdict = []

        for item in items:
            form = ShoppingCartForm(
                {"user": request.user.id, "clothing": item.id, "quantity": 1})
            itemsdict.append({"item": item, "form": form})

        messages.success(request, "Your order was successfully placed")
        data = {"itemsdict": itemsdict}
        return render(request, 'sampleapp/homepage.html', data)
    elif(shippingaddressform.is_valid()):
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

        cum_price += 50
        cum_price_decimal = "{:.2f}".format(cum_price)
        cum_price = float(cum_price_decimal)
        discount = cum_price*discountpercent
        cum_price -= discount

        region = str(shippingaddressform.cleaned_data.get('region'))
        shippingaddress = shippingaddressform.cleaned_data.get('street2') + " " + shippingaddressform.cleaned_data.get(
            'street1') + ", " + shippingaddressform.cleaned_data.get('city') + ", " + region + ", " + shippingaddressform.cleaned_data.get('postcode')

        data = {"cart": cart, "cum_price": cum_price,
                "item_count": item_count, "shippingaddress": shippingaddress, "promocode": promocode, "discount": discount}

        return render(request, 'sampleapp/finalizecod.html', data)

    else:
        purchasechoiceform = PurchaseChoiceForm()
        data = {"purchasechoiceform": purchasechoiceform}
        return render(request, "sampleapp/modeofpayment.html", data)


@login_required(login_url='login')
def confirm_cod(request):
    subject = "Order Details"
    message = "<h1>Hello " + request.user.username + \
        ", good day!</h1> <br><br>Here is a summary of your order:"
    from_email = settings.EMAIL_HOST_USER
    recepient_list = [request.user.email]

    email = EmailMessage(
        subject,
        message,
        from_email,
        recepient_list
    )

    email.content_subtype = 'html'
    pdf = generate_pdf_cod(request).getvalue()
    email.attach("receipt.pdf", pdf, 'application/pdf')
    email.send()

    items = ShoppingCart.objects.filter(user=request.user).order_by('id')
    for item in items:
        order = OrderForm({"user": request.user.id, "shoppingcart": item.clothing.name, "date_ordered": datetime.date.today(),
                           "quantity": item.quantity, "price": item.clothing.price})
        if(order.is_valid()):
            order.save()

    for item in items:
        stockitem = Item.objects.get(name=item.clothing)
        stockitem.stock = stockitem.stock - item.quantity
        stockitem.save()
        item.delete()

    items = Item.objects.all()
    itemsdict = []

    for item in items:
        form = ShoppingCartForm(
            {"user": request.user.id, "clothing": item.id, "quantity": 1})
        itemsdict.append({"item": item, "form": form})

    messages.success(request, "Your order was successfully placed")
    data = {"itemsdict": itemsdict}
    return render(request, 'sampleapp/homepage.html', data)


def generate_pdf_cod(request):
    template_path = 'sampleapp/receiptcod.html'
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
    cum_price += 50
    shippingaddress = request.GET.get('ship')
    discount = request.GET.get('discount')
    cum_price_decimal = "{:.2f}".format(cum_price)
    cum_price = float(cum_price_decimal)
    discountprice = float(discount)
    cum_price -= discountprice

    content = {"cart": cart, "cum_price": cum_price,
               "item_count": item_count, "shippingaddress": shippingaddress, "discount": discount}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="receiptcod.pdf'
    template = get_template(template_path)
    html = template.render(content)
    pdf = pisa.CreatePDF(html, dest=response)

    if not pdf.err:
        return response


@login_required(login_url='login')
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('id')
    filter = OrderFilter(request.GET, queryset=orders)
    orders = filter.qs

    data = {"orders": orders, "filter": filter}
    return render(request, 'sampleapp/history.html', data)


# ERROR 404 PAGE
def error_404_view(request, exception):
    return render(request, 'sampleapp/404.html')
