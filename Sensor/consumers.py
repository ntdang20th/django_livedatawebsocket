from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
import json


class SensorConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.room_name = 'sensor_consumer'
        self.room_group_name = 'sensor_consumer_group'

        await(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({'status': 'Connected from JW SensorConsumer!'}))

    async def receive(self, text_data):
        await self.send(text_data=json.dumps({'status': 'We got you!'}))

    async def disconnect(self, *args, **kwargs):
        print("Disconnected!")

    async def send_rawdata(self, event):
        data = json.loads(event.get('value'))
        await self.send(text_data=json.dumps({'data': data}))
