from django.db import models
from ApiModule.models import Order,FoodItem, CustomUser

# Create your models here.
class OrderChange(models.Model):
    order = models.ForeignKey(Order, on_delete = models.PROTECT)
    change_on = models.CharField(max_length = 200)
    changed_from = models.CharField(max_length = 200)
    changed_to = models.CharField(max_length = 200)
    changed_by = models.ForeignKey(CustomUser, on_delete = models.PROTECT)

class FoodItemChange(models.Model):
    food = models.ForeignKey(FoodItem, on_delete = models.PROTECT)
    change_on = models.CharField(max_length = 200)
    changed_from = models.CharField(max_length = 200)
    changed_to = models.CharField(max_length = 200)
    changed_by = models.ForeignKey(CustomUser, on_delete = models.PROTECT)
