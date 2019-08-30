from django.urls import path
from . import views

urlpatterns = [
    path('',views.reception, name = 'main'),
    path('foodmanager',views.food_manager, name = "Food manager")
]
