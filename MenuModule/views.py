from django.shortcuts import render
from ApiModule.models import FoodItem, FoodType
import json 


def menu(request):
    Food = FoodItem.objects.all()
    food_list = {}
    Foodtype = FoodType.objects.all()
    for typename in Foodtype:
        food_list[str(typename.food_type)] = {'name':[], 'price':[]}
    for f in Food :
        if(f.is_active):
            food_list[str(f.food_type)]['name'].append(str(f.name))
            food_list[str(f.food_type)]['price'].append(str(f.price))
    return render(request, 'MenuModule/menu.html', {'data':json.dumps(food_list)})
