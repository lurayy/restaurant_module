from django.urls import path
from . import reception_consumer, customer_consumer

websocket_urlpatterns = [
    path('ws/reception/', reception_consumer.ReceptionConsumer),
    path('ws/customer/', customer_consumer.CustomerConsumer)
]