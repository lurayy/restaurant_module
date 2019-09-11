from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_panel, name = "Main admin Panel"),
    path('manage_user',views.manage_user, name="Mange exsisting user"),
    path('manage_user/<str:id>',views.user_profile, name = "show book info"),
]
