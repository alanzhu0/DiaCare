import logging
from django.conf import settings
import csv
from django import http


from collections import OrderedDict
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render
from django.db.models import Q

from datetime import datetime, timedelta


from .models import User, Food, Produce, FoodChoice, ProduceChoice, ProduceCategory, Doctor, Dietician, Order, EmailVerificationLink, ScreeningQuestionnaire
from .forms import SignupForm, ScreeningQuestionnaireForm, ProfileForm
from .decorators import active_users_only
from .helpers import send_email

logger = logging.getLogger(__name__)


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


################ AUTHENTICATION ################

@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect(reverse('index'))

def index(request):
    if request.user.is_authenticated:
        if request.user.active:
            return render(request, 'home.html')
        if not request.user.email_verified:
            return redirect(reverse('verify_email'))
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


################ SIGNUP ################

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


def verify_email(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to verify your email address. Please login and click the verification link again.")
        return redirect(reverse('index'))
    
    if request.user.email_verified:
        return redirect(reverse('index'))
    
    if request.GET.get("token"):
        try:
            verification_link = EmailVerificationLink.objects.get(token=request.GET.get("token"), valid=True, user=request.user)
        except EmailVerificationLink.DoesNotExist:
            messages.error(request, "Invalid verification link.")
            return render(request, 'verify_email.html')
        request.user.email_verified = True
        request.user.save()
        verification_link.valid = False
        verification_link.save()
        
        messages.success(request, "Your email address has been verified.")
        return redirect(reverse('index'))
    
    if request.GET.get("resend") or not EmailVerificationLink.objects.filter(user=request.user).exists():
        if EmailVerificationLink.objects.filter(
            user=request.user, 
            valid=True, 
            time_created__gte=timezone.now()-timedelta(minutes=1)
        ).exists():
            messages.error(request, "Please wait a few minutes before requesting another verification email.")
            return render(request, 'verify_email.html')
        
        EmailVerificationLink.objects.filter(user=request.user).delete()
        verification_link = EmailVerificationLink.objects.create(user=request.user, email=request.user.email)
        
        send_email(
            "Children's National Food Pharmacy App: Verify your email address",
            f"""
            Hi {request.user.first_name},
            
            You recently signed up for the Children's National Food Pharmacy App. If this was you, please click the link below to verify your email address:
            {settings.MY_HOST}{reverse('verify_email')}?token={verification_link.token}
            
            If you did not sign up for the Food Pharmacy App, please ignore this email.
            
            Thank you,
            Food Pharmacy App Team
            Children's National Hospital
            111 Michigan Avenue NW, Washington, DC.
            www.childrensnational.org
            """,
            request.user.email,
        )
        
        messages.success(request, "Sent verification email.")
    
    return render(request, 'verify_email.html')
    
    



def csv_questionnaire(request):
    dict_list = []
    
    for s in ScreeningQuestionnaire.objects.all():
        answers = s.QUESTION_OBJS
        answer_dict = OrderedDict()
        answer_dict["Name"] = s.user.first_name + " " + s.user.last_name
        answer_dict["Email"] = s.user.email
        answer_dict["Date"] = s.date_completed.strftime("%Y-%m-%d %H:%M:%S")
        for question in s.QUESTION_STRS:
            answer = getattr(s, question)
            answer_dict[s.QUESTION_STR_TO_OBJ_MAP.get(question).verbose_name] = dict(s.QUESTION_STR_TO_OBJ_MAP.get(question).get_choices(question)).get(answer)
            # if answer.choice:
            #     answer_dict[question] = answer.
            # elif answer.answer:
            #     answer_dict[question] = answer.answer
            # elif answer.clear_vote:
            #     answer_dict[question] = "Cleared"
            # else:
            #     answer_dict[question] = "None"
            # logger.error()
            logger.error(dict(s.QUESTION_STR_TO_OBJ_MAP.get(question).get_choices(question)))
            # logger.error(answer.verbose_name)
            # answer_dict[answer.verbose_name] = str(answer.choices)
            # # logger.error(answer.get_choices(answer))
            # logger.error(answer.choice)

            
        dict_list.append(answer_dict)

    response = http.HttpResponse(content_type="text/csv")
    w = csv.DictWriter(response, dict_list[0].keys())
    w.writeheader()
    w.writerows(dict_list)
    return response





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
    return render(request, 'screening_questionnaire.html', {'form': form})
