from django.shortcuts import render
from django.http import HttpResponse
from ApiModule.models import FoodItem, FoodType, Table, Order, OrderedItem
import json 


def menu(request):
    Food = FoodItem.objects.all()
    food_list = {}
    Foodtype = FoodType.objects.all()
    for typename in Foodtype:
        food_list[str(typename.food_type)] = {'name':[], 'price':[],'image_url':[],'description':[]}
    for f in Food :
        if(f.is_active):
            food_list[str(f.food_type)]['name'].append(str(f.name))
            food_list[str(f.food_type)]['image_url'].append(str(f.image))
            food_list[str(f.food_type)]['description'].append(str(f.description))
            food_list[str(f.food_type)]['price'].append(str(f.price))
    return render(request, 'MenuModule/menu.html', {'data':json.dumps(food_list)})

