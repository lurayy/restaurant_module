from django.contrib import admin
from .models import CustomUser, R_Manager, R_Staff, FoodItem, FoodType, Table, Order, OrderedItem
# Register your models here.
admin.site.register(CustomUser)

admin.site.register(R_Manager)
admin.site.register(R_Staff)
admin.site.register(FoodItem)
admin.site.register(FoodType)
admin.site.register(Table)
admin.site.register(Order)
admin.site.register(OrderedItem)
