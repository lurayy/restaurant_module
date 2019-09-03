from channels.generic.websocket import WebsocketConsumer
import json 
from asgiref.sync import async_to_sync
from ApiModule.models import Order, OrderedItem, FoodItem, FoodType, CustomUser
from django.db.models import Q
from django.contrib.auth.decorators import login_required

GROUP_NAME = 'reception'

class ReceptionConsumer(WebsocketConsumer):

    def send_group_response(self,response):
        async_to_sync (self.channel_layer.group_send)(
            GROUP_NAME,
            {
                'type': 'staff_message',
                'message': response,
            }
        )
    
    def staff_message(self,event):
        print("send staff")
        message = event['message']
        print(message)
        async_to_sync (self.send(text_data = json.dumps({
            'message':message
        })))
   
    def send_reply_response(self,message):
        async_to_sync (self.send(text_data = json.dumps({
            'message':message
        })))
    
    def connect(self):
        async_to_sync (self.channel_layer.group_add)(
            GROUP_NAME,
            self.channel_name
        )
        print("Connecting Incommnig")
        self.accept()
        print(self.channel_name)
        print("Connection Accepted")
    
    def disconnect(self, close_code):
        async_to_sync (self.channel_layer.group_discard)(
            GROUP_NAME,
            self.channel_name
        )
    
    # send state = True to make things paid 
    def update_order(self,order_id,state):
        response_json = {'type':"update", 'success':1, 'message' : "Order Successfully updated"}
        state = str(state).lower()
        try:
            order = Order.objects.get(id = int(order_id))
            if (str(state) == "done"):
                order.state = "DONE"
                order.save()
            elif (str(state) == "canceled"):
                order.state = "CANCELED"
                order.save()
            elif (str(state) == "pending"):
                order.state = "PENDING"
                order.save()
            elif (str(state) == "paid"):
                order.is_paid = True
                order.save()
            elif (str(state) == "unpaid"):
                order.is_paid = False
                order.save()
            else:
                response_json['success'] = 0
                response_json['message'] = "Error Updating Order state. Invalid State"
        except:
            response_json['success'] = 0
            response_json['message'] = "Error Updating Order state. Invalid Order Id. Cannot Retrive Order"
        if (response_json['success']):
            # since only state is updated
            updated_order = {'id':int(order.id), 'state':str(order.state), 'is_paid':order.is_paid}
            response_json['updated_order'] = updated_order
            self.send_group_response(response_json)
        else:
            self.send_reply_response(response_json)
            
    def get_order(self, data ):
        response = {'type': 'get_order_response', 'orders':[]}
        x = int(data['start'])
        y = int(data['end'])
        if (str(data['state'])== "ALL"):
            orders = Order.objects.all().order_by('-timestamp')[x:y]
        elif (str(data['state']) == "UNPAID"):
            orders = Order.objects.filter(~Q(state = "CANCELED")).filter(is_paid = False)
        else:
            orders = Order.objects.filter(state = str(data['state'])).order_by('-timestamp')[x:y]
        for order in orders:
            json_order = {'id':order.id,'is_paid':str(order.is_paid), 'state':str(order.state), 'timestamp': str(order.timestamp), 'table_number':str(order.table_number),'paid_price':int(order.paid_price), 'ordered_item':{'name':[], 'price':[], 'quantity':[]}}
            ordered_items = OrderedItem.objects.filter(order = order)
            for ordered_item in ordered_items:
                json_order['ordered_item']['name'].append(str(ordered_item.food_item.name))
                json_order['ordered_item']['price'].append(str(ordered_item.food_item.price))
                json_order['ordered_item']['quantity'].append(str(ordered_item.quantity))
            response['orders'].append(json_order)
        self.send_reply_response(response)
        
    def receive(self, text_data):        
        data = json.loads(text_data)
        if (str(data["type"]) == "update"):
            self.update_order(data['order_id'],data['state'])
        elif str(data["type"] == "get"):
            self.get_order(data)
            


        #get order , get_by = date, search_by_id,   
        # elif (str(data['type']) == 'get'):
        #     self.get_order(data['order_type'])




    
    # def get_order(self,data):
    #     response = {'type':'getOrderResponse','state':data['state'], 'order': []}
    #     orders = Order.objects.filter(
    #         state = data['state']
    #     )
    #     for order in orders:
    #         order_items = OrderedItem.objects.filter(
    #             order = order
    #         )
    #         food_items = []
    #         for order_item in order_items:
    #             food_item = {
    #                 'food_name': order_item.food_item.name,
    #                 'food_price': order_item.food_item.price,
    #                 'qunatity': order_item.quantity,
    #             }
    #             food_items.append(food_item)
    #         response['order'].append({
    #             'id': order.id,
    #             'timestamp': str(order.timestamp),
    #             'table_number':order.table_number,
    #             'food_item': food_items
    #         })
    #     self.send_response(response)
    
    # def set_order(self,data):
    #     pass

    # def modify_order(self,data):
    #     pass
    
    # def handle_error(self,data):
    #     pass

    # def get_menu(self):
    #     response = {"type":"getMenuResponse", "food_type": [], "food_items": []}
    #     food_items = FoodItem.objects.all()
    #     food_types = FoodType.objects.all()
    #     for food_item in food_items:
    #         if food_item.is_active:
    #             response["food_items"].append({"id": food_item.id,
    #                                         "food_type": food_item.food_type.food_type,
    #                                         "name": food_item.name,
    #                                         "price": float(food_item.price),
    #                                         # "image": str(product.image)
    #                                         })
    #     for food_type in food_types:
    #         response["food_type"].append({"id": food_type.id,
    #                                        "name": food_type.food_type
    #                                        })
    #     self.send_response(response)
    

   
    #imporvise this code make it adapt
    # def order(data):
    #     #data is send as a set of arrays wrapped in a dict.
    #     #eg. data = {type: "setOrder", table_number: 2,order:[{food_code:2,quantity:3},{food_code:1,quantity:3},{food_code:3,quantity:1}]}
    #     response = {}
    #     response['type'] = "order_response"
    #     table_number = data['table_number']
    #     ordered_food_items = data['order']
    #     current_order = Order.objects.create(table_number = table_number)
    #     for x in ordered_food_items:
    #         try:
    #             food_item = FoodItem.objects.get(code = int(x['food_code']))
    #             print("good food")
    #         except:
    #             #write a proper failure action
    #             response['']
    #         OrderedItem.objects.create(order = current_order,food_item = food_item,quantity = int(x['quantity']))
    #         # total_cost = int(food_item.price)*x['quantity']+total_cost
        
    # def connect(self):
    #     print("connect")
    #     self.accept()

    # def disconnect(self, close_code):
    #     pass

    # def receive(self,text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #     self.send(text_data= json.dumps({'message': message}))
        
