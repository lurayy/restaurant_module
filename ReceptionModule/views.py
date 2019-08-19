from django.shortcuts import render
from django.http import HttpResponse
import json
from ApiModule.models import Order, OrderedItem
from django.db.models import Q
from django.core import serializers

def order(request):
    return HttpResponse("order")

def menu(request):
    pass

def reception(request):
    response_json = {'orders':[]} 
    orders = Order.objects.filter(state="PENDING").order_by('timestamp')[:20]
    for order in orders:
        json_order = {'id':order.id,'state':str(order.state), 'timestamp': str(order.timestamp), 'table_number':str(order.table_number),'paid_price':int(order.paid_price), 'ordered_item':{'name':[], 'price':[], 'quantity':[]}}
        ordered_items = OrderedItem.objects.filter(order = order)
        for ordered_item in ordered_items:
            json_order['ordered_item']['name'].append(str(ordered_item.food_item.name))
            json_order['ordered_item']['price'].append(str(ordered_item.food_item.price))
            json_order['ordered_item']['quantity'].append(str(ordered_item.quantity))
        response_json['orders'].append(json_order)
    print(response_json)
    return render(request, 'ReceptionModule/reception.html', {'data':response_json})