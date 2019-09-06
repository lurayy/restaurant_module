from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_view, name = "login view"),
    path('logout',views.user_logout, name = "new user registration"),
]
