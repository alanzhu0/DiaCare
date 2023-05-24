from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('orders/', views.orders, name='orders'),
    path('order-food/', views.order_food, name='order_food'),
    path('cancel-order/', views.cancel_order, name='cancel_order'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('signup/verify-email', views.verify_email, name='verify_email'),
    path('signup/screening-questionnaire', views.screening_questionnaire, name='screening_questionnaire'),
    path('profile', views.profile, name='profile'),
    path('downloads/', views.csv_questionnaire, name='questionnaire')
    
]
