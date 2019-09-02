from django.contrib import admin
from .models import CustomUser, FoodItem, FoodType, Table, Order, OrderedItem
# Register your models here.
admin.site.register(CustomUser)

admin.site.register(FoodItem)
admin.site.register(FoodType)
admin.site.register(Table)
admin.site.register(Order)
admin.site.register(OrderedItem)
