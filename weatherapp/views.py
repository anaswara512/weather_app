from django.shortcuts import render,redirect
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth import logout,authenticate,login
import requests
import datetime
import os
from dotenv import load_dotenv
load_dotenv()
from django.contrib.auth.decorators import login_required
# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken')
            print('email already taken')
            return redirect('signup')
        
        if password==confirm_password:
            user=CustomUser.objects.create_user(
            email=email,
            username=username,
            password=password,   
            )
    

            print('created')
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('signin')
        messages.error(request, 'Email is already taken')
    return render(request,'signup.html')

def signin_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print(user)
        if user:
            login(request, user)
            return redirect('weather')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('signin')
    return render(request, 'signin.html')


def logout_view(request):
    logout(request)
    return redirect('signin')

def home_view(request):
    return render(request,'home.html')


@login_required(login_url='signin')
def weather(request):
    if 'city' in request.POST:
        city=request.POST.get('city')
    else:
        city='calicut'
    APP_ID=os.getenv('APP_ID')
    url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={APP_ID}"
    PARAMS= {'units':'metric'}

    try:
        data = requests.get(url ,params=PARAMS).json()
        description=data['weather'][0]['description']
        icon=data['weather'][0]['icon']
        temp=data['main']['temp']
        day= datetime.date.today()

        return render(request, 'weather.html',{
            'description':description,
            'icon':icon,
            'temp':temp,
            'day':day,
            'city': city,
            'exception_occured':False,
        })
    except KeyError:
        exception_occured =True
        messages.error(request,'Entered data is not available to API')
        day= datetime.date.today()
        
    return render(request,'weather.html',{
        'description':'clear sky',
        'icon':'01d',
        'temp':25,
        'day':day,
        'city': 'calicut',
        'exception_occured':exception_occured,
    })
        # set_password
# create
# create_user