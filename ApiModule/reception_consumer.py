from channels.generic.websocket import WebsocketConsumer
import json 
from asgiref.sync import async_to_sync
from ApiModule.models import Order, OrderedItem, FoodItem, FoodType, CustomUser

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
    
    def receive(self, text_data):        
        data = json.loads(text_data)
        print(data)

    
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
        

