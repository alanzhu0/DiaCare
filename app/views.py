import logging
from datetime import datetime, time, timedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render
from django.core import serializers
from . models import feed
import json

from .models import User, Food, Produce, FoodChoice, ProduceChoice, ProduceCategory, Doctor, Dietician, Order

logger = logging.getLogger(__name__)


def base_layout(request):
    template = 'app/base.html'
    return render(request, template)


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
                
        order.type = request.POST.get('type')
        order.date_scheduled = request.POST.get('date')
        
        # Create Food objects
        for food in FoodChoice.objects.filter(active=True):
            Food.objects.create(order=order, food=food)

        # Create Produce objects
        for category in ProduceCategory.objects.all():
            produce_list = request.POST.getlist(f"category-{category.id}")
            
            if len(produce_list) > category.maximum_choices:
                return render(request, 'food.html', {
                    "foods": FoodChoice.objects.filter(active=True),
                    "produce_categories": ProduceCategory.objects.all(),
                    "error": f"Too many produce choices selected for {category.name}."
                })
            
            for produce_id in produce_list:
                try:
                    produce_id = int(produce_id)
                    produce_choice = ProduceChoice.objects.get(id=produce_id)
                    Produce.objects.create(order=order, produce=produce_choice)
                except (ValueError, ProduceChoice.DoesNotExist):
                    continue
        order.save()
        return redirect(reverse('orders'))

    return render(request, 'food.html', {
        "foods": FoodChoice.objects.filter(active=True),
        "produce_categories": ProduceCategory.objects.all(),
    })


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
            request.doctors = Doctor.objects.all()
            request.dieticians = Dietician.objects.all()

            return render(request, 'signup.html', {'error': 'User already exists.'})
        except User.DoesNotExist:
            pass

        user = User.objects.create(
            email=email,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            gender=request.POST.get('gender'),
            address=request.POST.get('address'),
            doctor=Doctor.objects.get(id=request.POST.get('doctor')),
            dietician=Dietician.objects.get(id=request.POST.get('dietician')),
            password=make_password(password),
        )
        user.save()
        
        request.user = user
        return redirect(reverse('disclaimer'))

        #auth_login(request, user)

    request.doctors = Doctor.objects.all()
    request.dieticians = Dietician.objects.all()
    
    return render(request, 'signup.html')


def disclaimer(request):
    if request.user.is_authenticated:
        return redirect(reverse('questionnaire'))
    if request.method == 'POST':
        disclaimerval = request.POST.get('disclaimerval')
        if disclaimerval == 'no':
            request.doctors = Doctor.objects.all()

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

            if val == '1':
                return render(request, 'login.html', {'message': 'You are eligible for DiaCare! Please sign in with the account you created to continue.'})
        request.doctors = Doctor.objects.all()

        return render(request, 'signup.html', {'error': 'You do not qualify for the program.'})
    return render(request, 'questionnaire.html')
