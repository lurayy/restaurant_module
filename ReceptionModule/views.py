from django.shortcuts import render
from django.http import HttpResponse
import json
from ApiModule.models import Order, OrderedItem
from django.db.models import Q
from django.core import serializers
from .forms import FoodTypeForm
from ApiModule.models import FoodItem, FoodType

def reception(request):
    response_json = {'orders':[]} 
    orders = Order.objects.filter(state="PENDING").order_by('timestamp')[:20]
    for order in orders:
        json_order = {'id':order.id,'state':str(order.state), 'timestamp': str(order.timestamp), 'table_number':str(order.table_number),'is_paid':str(order.is_paid), 'paid_price':int(order.paid_price), 'ordered_item':{'name':[], 'price':[], 'quantity':[]}}
        ordered_items = OrderedItem.objects.filter(order = order)
        for ordered_item in ordered_items:
            json_order['ordered_item']['name'].append(str(ordered_item.food_item.name))
            json_order['ordered_item']['price'].append(str(ordered_item.food_item.price))
            json_order['ordered_item']['quantity'].append(str(ordered_item.quantity))
        response_json['orders'].append(json_order)
    return render(request, 'ReceptionModule/reception.html', {'data':response_json})



def food_manager(request):
    if request.method == "POST":
        json_str = request.body.decode(encoding='UTF-8')
        data = json.loads(json_str)
        food_item = FoodItem.objects.get(name = str(data['food_name']))
        if (int(data['value']) == 0 ):
            food_item.is_active = False
            food_item.save()
        else:
            food_item.is_active = True
            food_item.save()
        return HttpResponse("Good boi")
    else:
        Food = FoodItem.objects.all()
        food_list = {}
        Foodtype = FoodType.objects.all()
        for typename in Foodtype:
            food_list[str(typename.food_type)] = {'name':[], 'price':[], 'is_active':[]}
        for f in Food :
            food_list[str(f.food_type)]['name'].append(str(f.name))
            food_list[str(f.food_type)]['price'].append(str(f.price))
            food_list[str(f.food_type)]['is_active'].append(int(f.is_active))
            
        return render(request, 'ReceptionModule/food_manager.html', {'data':json.dumps(food_list)})

