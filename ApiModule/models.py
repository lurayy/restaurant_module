from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid

class CustomUser(AbstractUser):
    is_rmanager = models.BooleanField(default=False)
    is_rstaff = models.BooleanField(default=True)

    uuid = models.UUIDField(unique = True, default = uuid.uuid4)
    
    def __str__(self):
        return self.first_name + self.last_name


class Table(models.Model):
    table_number = models.PositiveIntegerField(unique = True, null=True)
    uuid = models.UUIDField(unique = True,default = uuid.uuid4)
    
    def __str__(self):
        return str(self.table_number)    


class R_Manager(CustomUser):
    REQUIRED_FIELDS = ('user',)
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE, primary_key = True, related_name = "R_Manager", unique = True)
    contact_number = models.CharField(blank = True, max_length  =  14)

    def save(self, *args, **kwargs):
        self.user.is_rmanager = True
        self.user.is_rstaff = True
        super().save(*args, **kwargs)


class R_Staff(CustomUser):
    REQUIRED_FIELDS = ('user',)
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE, primary_key = True, related_name = "R_Staff", unique = True)
    contact_number = models.CharField(blank = True, max_length  =  14)

    def save(self, *args, **kwargs):
        self.user.is_rmanager = False
        self.user.is_rstaff = True
        super().save(*args, **kwargs)


def foodtype_directory_path(instance, filename):
    return 'foodtype/type_{0}/{0}'.format(instance.name)

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

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        if self.state == "DONE":
            self.is_paid = True
        super().save(*args, **kwargs)

class OrderedItem(models.Model):
    order = models.ForeignKey(Order,on_delete= models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete = models.CASCADE)
    quantity = models.IntegerField()

# def send_ordered_item (sender, instance,**kwargs):
#     print(instance)
#     print("this")

# post_save.connect(send_ordered_item, sender=OrderedItem)