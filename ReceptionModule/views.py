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
    orders_json = {'orders':[]} 
    # orders = Order.objects.filter(state = "PENDING").order_by('timestamp')[:20].values('id','state','timestamp','table_number')
    orders = Order.objects.filter(state="PENDING").order_by('timestamp')[:20]
    print(orders)
    for order in orders:
        # food_items = 
        # ser_order = serializers.serialize('json',[order,])
        orders_json['orders'].append(order)
    print(orders_json)
    return render(request, 'ReceptionModule/reception.html', {'data':orders_json})