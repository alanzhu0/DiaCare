import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render
from django.db.models import Q

from .models import User, Food, Produce, FoodChoice, ProduceChoice, ProduceCategory, Doctor, Dietician, Order
from .forms import SignupForm, ScreeningQuestionnaireForm, ProfileForm
from .decorators import active_users_only

logger = logging.getLogger(__name__)


def index(request):
    if request.user.is_authenticated:
        if request.user.active:
            return render(request, 'home.html')
        if request.user.eligible:
            return render(request, 'eligible.html')
        if not request.user.completed_screening_questionnaire:
            return redirect(reverse('screening_questionnaire'))
        return render(request, 'ineligible.html')
    
    # Login
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'The credentials you entered were incorrect. Please try again.'})

        user = authenticate(username=user.email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(reverse('index'))
        return render(request, 'login.html', {'error': 'The credentials you entered were incorrect. Please try again.'})

    return render(request, 'login.html')

@active_users_only
def order_food(request):
    if request.method == 'POST':
        user = request.user
        
        if request.POST.get('order'):
            try:
                order = Order.objects.get(id=request.POST.get('order'))
                messages.success(request, f"Order #{order.number} was updated successfully.")
            except Order.DoesNotExist:
                order = Order.objects.create(user=user)
                order.number = Order.objects.filter(user=user).last().number + 1
                messages.success(request, f"Successfully placed Order #{order.number}.")
        else:
            order = Order.objects.create(user=user)
            order.number = Order.objects.filter(user=user).order_by('number').last().number + 1
            messages.success(request, f"Successfully placed Order #{order.number}.")
                
        order.type = request.POST.get('type')
        order.date_scheduled = request.POST.get('date')
        order.patient_comments = request.POST.get('patient-comments')
        
        # Create Food objects
        Food.objects.filter(order=order).delete()
        for food in FoodChoice.objects.filter(active=True):
            Food.objects.create(order=order, food=food)

        # Create Produce objects
        Produce.objects.filter(order=order).delete()
        for category in ProduceCategory.objects.all():
            produce_list = request.POST.getlist(f"category-{category.id}")
            
            if len(produce_list) > category.maximum_choices:
                return render(request, 'order-food.html', {
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

    if request.GET.get("id"):
        try:
            order = Order.objects.get(id=request.GET.get("id"))
        except Order.DoesNotExist:
            messages.error(request, "Unable to edit order.")
            return redirect(reverse("order_food"))
        
        if order.fulfilled or order.cancelled or order.user != request.user:
            messages.error(request, "Unable to edit order.")
            return redirect(reverse("order_food"))
        
        return render(request, 'order-food.html', {
            "foods": FoodChoice.objects.filter(active=True),
            "produce_categories": ProduceCategory.objects.all(),
            "order": order,
            "order_producechoice_ids": [produce.produce.id for produce in order.produces.all()],
        })

    if Order.objects.filter(user=request.user, date_fulfilled__isnull=True, date_cancelled__isnull=True).exists():
        messages.error(request, "You cannot place an order at this time because you already have an open order.")
        return redirect(reverse("orders"))
    
    return render(request, 'order-food.html', {
        "foods": FoodChoice.objects.filter(active=True),
        "produce_categories": ProduceCategory.objects.all(),
    })  
    
@active_users_only
def cancel_order(request):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=request.POST.get('order'))
        order.date_cancelled = timezone.now()
        order.save()
        messages.success(request, f"Order #{order.number} has been cancelled.")
        return redirect(reverse('orders'))
    if request.GET.get("id"):
        try:
            order = Order.objects.get(id=request.GET.get("id"))
        except Order.DoesNotExist:
            messages.error(request, "Unable to cancel order.")
            return redirect(reverse("orders"))
        
        if order.fulfilled or order.cancelled or order.user != request.user:
            messages.error(request, "Unable to cancel order.")
            return redirect(reverse("orders"))
        return render(request, 'cancel-order.html', {
            "order": order,
        })
    return redirect(reverse('orders'))


@active_users_only
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-number')
    return render(request, 'orders.html', {
        "orders": orders,
        "has_open_order": orders.filter(date_fulfilled__isnull=True, date_cancelled__isnull=True).exists(),
        "last_order": orders.first() if orders.exists() else None,
    })



@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect(reverse('index'))


def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect(reverse('index'))
        return render(request, 'signup.html', {'form': form})
    
    form = SignupForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def screening_questionnaire(request):
    if request.user.active or request.user.completed_screening_questionnaire:
        return redirect(reverse('index'))

    if request.method == 'POST':
        form = ScreeningQuestionnaireForm(request.POST)
        if form.is_valid():
            questionnaire = form.save(commit=False)
            questionnaire.user = request.user
            questionnaire = form.save()
            return redirect(reverse('index'))
        logging.error(form.errors)
        return render(request, 'screening_questionnaire.html', {'form': form})

    form = ScreeningQuestionnaireForm()
    return render(request, 'screening_questionnaire.html', {'form': form})
    
    # if request.method == 'POST':
    #     for thing in request.POST.dict().keys():
    #         val = request.POST.dict().get(thing)

    #         if val == '1':
    #             return render(request, 'login.html', {'message': 'You are eligible for DiaCare! Please sign in with the account you created to continue.'})
    #     request.doctors = Doctor.objects.all()

    #     return render(request, 'signup.html', {'error': 'You do not qualify for the program.'})
    # return render(request, 'questionnaire.html')

@active_users_only
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated profile.")
            return redirect(reverse('profile'))
        print(form.errors)
        return render(request, 'profile.html', {'form': form}) 
    
    form = ProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})