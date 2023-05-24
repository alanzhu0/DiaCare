from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    
    # User functions
    path('profile', views.profile, name='profile'),
    path('orders/', views.orders, name='orders'),
    path('order-food/', views.order_food, name='order_food'),
    path('cancel-order/', views.cancel_order, name='cancel_order'),
    
    # Signup
    path('signup/', views.signup, name='signup'),
    path('signup/verify-email', views.verify_email, name='verify_email'),
    path('signup/screening-questionnaire', views.screening_questionnaire, name='screening_questionnaire'),
    # Approval process
    path('signup/approve', views.approve_account, name='approve_account'),
    
    # Admin only
    path('download-questionnaire/', views.csv_questionnaire, name='download_questionnaire')
    
]
