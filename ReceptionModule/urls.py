from django.urls import path
from . import views

urlpatterns = [
    path('',views.reception, name = 'main'),
    path('login',views.login_view, name = "login"),
    path('logout',views.user_logout, name= "logout"),
    path('foodmanager',views.food_manager, name = "Food manager"),
]
