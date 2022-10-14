import threading
import time
import uuid
import datetime
from channels.layers import get_channel_layer
from .models import *
from faker import Faker
from asgiref.sync import async_to_sync
import json
import random

fake = Faker()

class CreateSensorsThread(threading.Thread):

    def __init__(self, total):
        self.total = total
        threading.Thread.__init__(self)

    def run(self):
        try:
            print('Thread Execution Start!')
            channel_layer = get_channel_layer()
            for i in range(self.total):
                acceleration_sensor = Accelaration.objects.create(
                    valueX=random.uniform(-0.09, -0.01),
                    valueY=random.uniform(0.01, 0.09),
                    valueZ=random.uniform(1.01, 1.09),
                    unit=Unit.objects.get(pk=1)
                )
                gyroscope_sensor = Gyroscope.objects.create(
                    valueX=random.uniform(-1.8, -0.2),
                    valueY=random.uniform(12.1, 13),
                    valueZ=random.uniform(12.1, 13),
                    unit=Unit.objects.get(pk=2)
                )
                rotation_sensor = Rotation.objects.create(
                    valueX=random.uniform(0.9, 16.9),
                    valueY=random.uniform(0.01, 4.9),
                    valueZ=random.uniform(-45, 45),
                    unit=Unit.objects.get(pk=3)
                )

                channel_layer = get_channel_layer()
                data = {'date': str(datetime.datetime.now()), 'UUID': str(uuid.uuid4()), 'Touch': 'no touch detected', 'data': [{'acceleration': acceleration_sensor.getJson()}, {'gyroscope': gyroscope_sensor.getJson()}, {'rotation': rotation_sensor.getJson()}]}
                rawdata = Rawdata.objects.create(
                    date = str(datetime.datetime.now()),
                    device = Device.objects.get(pk=1),
                    touch_status = TouchStatus.objects.get(pk=1),
                    acceleration = acceleration_sensor,
                    gyroscope = gyroscope_sensor,
                    rotation =rotation_sensor
                )


                try:
                    trash_id = rawdata.id - 15
                    print(trash_id)
                    Rawdata.objects.filter(id__lte=trash_id).delete()
                    Accelaration.objects.filter(id__lte=acceleration_sensor.id-15).delete()
                    Gyroscope.objects.filter(id__lte=gyroscope_sensor.id-15).delete()
                    Rotation.objects.filter(id__lte=rotation_sensor.id-15).delete()
                except Exception as e:
                    print(e)
                async_to_sync(channel_layer.group_send)(
                    'new_consumer_group', {
                        'type': 'data_sending',
                        'value': json.dumps(data),
                    }
                )
                time.sleep(1)
        except Exception as e:
            print(e)
