from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

import inspect, os



class StaffPosition(models.Model):
    position = models.CharField(max_length = 200)

    def __str__(self):
        return(self.position)

class CustomUser(AbstractUser):
    is_rmanager = models.BooleanField(default=False)
    is_rstaff = models.BooleanField(default=True)
    phone_number = models.CharField(blank = True, max_length  =  14)
    emp_id = models.UUIDField(unique = True, default = uuid.uuid4().hex, max_length=7)
    position = models.ForeignKey(StaffPosition, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.first_name + self.last_name

    def get_emp_id(self):
        return (str(self.emp_id)[5:11].upper())


class Table(models.Model):
    table_number = models.PositiveIntegerField(unique = True, null=True)
    uuid = models.UUIDField(unique = True,default = uuid.uuid4)
    
    def __str__(self):
        return str(self.table_number)    


def foodtype_directory_path(instance, filename):
    return 'foodtype/type_{0}/{0}'.format(instance.food_type)

class FoodType(models.Model):
    food_type = models.CharField(max_length = 200,null = True)
    description = models.TextField(null=True, blank = True)
    image = models.ImageField(null = True, upload_to = foodtype_directory_path, blank = True)


    def __str__(self):
        return str(self.food_type)


def user_directory_path(instance, filename):
    return 'fooditem/food_{0}/{0}'.format(instance.name)

class FoodItem(models.Model):
    name = models.CharField(max_length = 200)
    food_type = models.ForeignKey(FoodType, on_delete = models.CASCADE,null = True)
    price = models.PositiveIntegerField(default = 100)
    is_active = models.BooleanField(default= True)
    image = models.ImageField(null= True, upload_to = user_directory_path, blank = True)
    description = models.TextField(null = True, blank = True)
    last_modified = models.DateField(auto_now = True)
    def __str__(self):
        return self.name



class Order(models.Model):
    STATES = (
        ('DONE', "Done"),
        ('PENDING', "Pending"),
        ('CANCELED', "Canceled")
    )
    state = models.CharField(max_length=8, choices=STATES, default='PENDING')
    timestamp = models.DateTimeField(default=timezone.now)
    table_number = models.ForeignKey(Table, on_delete = models.SET_NULL, null = True)
    paid_price = models.PositiveIntegerField(default = 0)
    is_paid = models.BooleanField(default= False)
    last_modified = models.DateField(auto_now = True)

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        if self.state == "DONE":
            self.is_paid = True
        super().save(*args, **kwargs)


# @receiver(post_save, sender=Order)
# def change_log_pre(sender, instance, **kwargs):
#     print("sender=",sender)
#     print("instance",instance)
#     print("kwrgs",kwargs)

# def change_log_post(sender, instance, **kwargs):
#     print("post_save")
#     print("sender=",sender)
#     print("instance",instance)
#     print("kwrgs",kwargs)



# pre_save.connect(change_log_pre, sender = Order)
# post_save.connect(change_log_post, sender = Order)


class OrderedItem(models.Model):
    order = models.ForeignKey(Order,on_delete= models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete = models.CASCADE)
    quantity = models.IntegerField()

# def send_ordered_item (sender, instance,**kwargs):
#     print(instance)
#     print("this")

# post_save.connect(send_ordered_item, sender=OrderedItem)