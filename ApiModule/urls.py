from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.get_order, name = "get order"),
]
