from .models import *
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import *

# Create your views here.

def homepage(request):
    shopitems=ShopItem.objects.all()
    data = {"shopitems":shopitems}
    return render(request, 'sampleapp/homepage.html',data)

def register(request):
    form = UserForm()
    

    if(request.method=="POST"):
        form = UserForm(request.POST)
        if(form.is_valid()):
            form.save()
            messages.success(request,"Account was created for "+ form.cleaned_data.get("username"))
            return redirect('/login')

    data = {"form":form}
    return render(request, 'sampleapp/register.html',data)

def login_page(request):
    if(request.method=="POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            print("Login Success.")
            return redirect('/')
        else:
            print("Login Failed.")
            messages.error(request,"Incorrect password or username")
    
    return render(request, 'sampleapp/login.html')

def aboutus(request):
    return render(request, 'sampleapp/aboutus.html')

def logout_page(request):
    logout(request)
    return redirect('/login')

