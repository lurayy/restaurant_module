from django.shortcuts import render
from django.http import HttpResponse
import json

def order(request):
    return HttpResponse("order")

def menu(request):
    pass

def reception(request):
    return render(request, 'ReceptionModule/reception.html', {'room_name_json':"room1"})