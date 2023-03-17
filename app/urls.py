from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('orders/', views.orders, name='orders'),
    path('food/', views.food, name='food'),
    path('base_layout/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    
    path('disclaimer/', views.disclaimer, name='disclaimer'),
    path('questionnaire/', views.questionnaire, name='questionnaire'),
]
