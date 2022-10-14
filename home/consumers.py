from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
import json



class TestConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = "test_consumer"
        self.room_group_name = "test_consumer_group"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        self.send(text_data=json.dumps({'status': 'connected from django channels'}))

    def receive(self, text_data):
        print(text_data)
        self.send(text_data=json.dumps({'status': 'Chào mừng bạn đến với bình nguyên vô tận'}))

    def disconnect(self, *args, **kwargs):
        print("disconnected!")

    def send_notification(self, event):
       print('send_notification')
       data = json.loads(event.get('value'))
       self.send(text_data=json.dumps({'status': 'Deceted save!', 'data': data}))
       print('send_notification')



class NewConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.room_name = 'new_consumer'
        self.room_group_name = 'new_consumer_group'

        await(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.send(text_data=json.dumps({'status': 'Connected from json websocket consumer'}))

    async def receive(self, text_data):
        print(text_data)
        await self.send(text_data=json.dumps({'status': 'We got you!'}))

    async def disconnect(self, *args, **kwargs):
        print("disconnected!")

    async def send_notification(self, event):
        data = json.loads(event.get('value'))
        await self.send(text_data=json.dumps({'status': 'Deceted change!', 'data': data}))
