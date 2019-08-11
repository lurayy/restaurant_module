from django.urls import path
from . import views

urlpatterns = [
    path('order/', views.order, name = "get and post order"),

    path('menu/', views.menu, name = "get menu"),
]
