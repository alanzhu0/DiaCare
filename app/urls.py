from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('orders/', views.orders, name='orders'),
    path('order-food/', views.order_food, name='order_food'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    
    path('disclaimer/', views.disclaimer, name='disclaimer'),
    path('questionnaire/', views.questionnaire, name='questionnaire'),
]
