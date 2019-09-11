from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_view, name = "login view"),
    path('register',views.user_registration, name = "new user registration"),
    path('logout',views.user_logout, name = "new user registration"),
]
