import logging
from datetime import datetime, time, timedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .models import User, Food, Produce, FoodChoice, ProduceChoice, ProduceCategory, Doctor, Dietician, Order


import logging

logger = logging.getLogger('scope.name')

file_log_handler = logging.FileHandler('logfile.log')
logger.addHandler(file_log_handler)

stderr_log_handler = logging.StreamHandler()
logger.addHandler(stderr_log_handler)
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
logger.debug('This is a debug message')


def index(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    return redirect(reverse('login'))


@login_required
def home(request):
    context = {
        
    }
    return render(request, 'home.html', context)


@login_required
def food(request):
    if request.method == 'POST':
        user = request.user
        order = Order.objects.create(user=user)
        produces = request.POST.get('produce')
        
        # Create Food objects
        for food in FoodChoice.objects.filter(active=True):
            Food.objects.create(order=order, food=food) 
            
        # Create Produce objects
        for produce_id in produces:
            produce = get_object_or_404(ProduceChoice, id=produce_id)
            Produce.objects.create(order=order, produce=produce)
        
    return render(request, 'food.html')


@login_required
def orders(request):
    return render(request, 'orders.html', {"orders": Order.objects.filter(user=request.user)})


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'User does not exist.'})

        user = authenticate(username=user.email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(reverse('home'))
        return render(request, 'login.html', {'error': 'Invalid credentials.'})
    
    return render(request, 'login.html')


@login_required
def logout(request):
    auth_logout(request)
    return redirect(reverse('login'))


def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse('disclaimer'))

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            return render(request, 'signup.html', {'error': 'User already exists.'})
        except User.DoesNotExist:
            pass

        user = User.objects.create(
            email=email, 
            first_name=request.POST.get('first_name'), 
            last_name=request.POST.get('last_name'), 
            gender=request.POST.get('gender'),
            address=request.POST.get('address'),
            password=make_password(password),
        )
        user.save()
        user = authenticate(username=user.email, password=password)
        #auth_login(request, user)
        request.user = user

        return redirect(reverse('disclaimer'))
    return render(request, 'signup.html')


def disclaimer(request):
    if request.user.is_authenticated:
        return redirect(reverse('questionnaire'))
    if request.method == 'POST':
        disclaimerval = request.POST.get('disclaimerval')
        if disclaimerval == 'no':
            return render(request, 'signup.html', {'error': 'Please accept the disclaimer to sign up.'})
        else:
            return redirect(reverse('questionnaire'))
    
    
    
    return render(request, 'disclaimer.html')


def questionnaire(request):
    logging.error("jeresfddfre")
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    if request.method == 'POST':
        for thing in request.POST.dict().keys():

            val = request.POST.dict().get(thing)
            
            print(thing)
            logging.error(request.POST)

            logging.error(request.POST.dict().keys())
            logging.error("thing: " + thing)
            logging.error("val: " + val)
            logging.error("jerere")

            if val == '1':
                user = request.user
                auth_login(request, user)
                return redirect(reverse('home'))

                
           
        return render(request, 'signup.html', {'error': 'You do not qualify for the program.'})

        return redirect(reverse('home'))
    return render(request, 'questionnaire.html')
