from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_panel, name = "Main admin Panel"),
    path('user/register',views.user_registration, name = "new user registration"),
    path('user/manage', views.user_manager, name = "User manager"),
]
