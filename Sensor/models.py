import json
import datetime
from django.db import models
from django.contrib.auth.models import User

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Device(models.Model):
    dv_name = models.CharField(max_length=100)
    description = models.TextField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.dv_name

    def toJSON(self):
        data = {'dv_name': self.dv_name,
                'description': self.description,
                'is_active': self.is_active}
        return json.dumps(data)

class Unit(models.Model):
    unit_name = models.CharField(default='', max_length=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.unit_name


class Accelaration(models.Model):
    valueX = models.FloatField(default=0)
    valueY = models.FloatField(default=0)
    valueZ = models.FloatField(default=0)
    sensor_name = models.TextField(max_length=100, default='Accelaration')
    description = models.TextField(default='', max_length=200)
    is_active = models.BooleanField(default=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def getJson(self):
        data = {"name": "Accelaration", "valueX": self.valueX, "valueY": self.valueY, "valueZ": self.valueZ, "unit": self.unit.__str__()}
        return data


class Gyroscope(models.Model):
    valueX = models.FloatField(default=0)
    valueY = models.FloatField(default=0)
    valueZ = models.FloatField(default=0)
    sensor_name = models.TextField(max_length=100, default='Gyroscope')
    description = models.TextField(default='', max_length=200)
    is_active = models.BooleanField(default=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def getJson(self):
        data = {"name": "Gyroscope", "valueX": self.valueX, "valueY": self.valueY, "valueZ": self.valueZ, "unit": self.unit.__str__()}
        return data


class Rotation(models.Model):
    valueX = models.FloatField(default=0)
    valueY = models.FloatField(default=0)
    valueZ = models.FloatField(default=0)
    sensor_name = models.TextField(max_length=100, default='Rotation')
    description = models.TextField(default='', max_length=200)
    is_active = models.BooleanField(default=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def getJson(self):
        data = {"name": "Rotation", "valueX": self.valueX, "valueY": self.valueY, "valueZ": self.valueZ, "unit": self.unit.__str__()}
        return data


class Patient(models.Model):
    first_name = models.TextField(default='', max_length=100)
    last_name = models.TextField(default='', max_length=100)
    birth = models.DateField(default='', max_length=100)
    email = models.EmailField(default='', max_length=100)
    phone_number = models.CharField(default='', max_length=15)
    address = models.TextField(default='', max_length=200)
    is_active = models.BooleanField(default=True)
    device = models.ForeignKey(Device, on_delete=models.PROTECT)

class Familiar(models.Model):
    first_name = models.TextField(default='', max_length=100)
    last_name = models.TextField(default='', max_length=100)
    birth = models.DateField(default='', max_length=100)
    email = models.EmailField(default='', max_length=100)
    phone_number = models.CharField(default='', max_length=15)
    address = models.TextField(default='', max_length=200)
    is_active = models.BooleanField(default=True)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)



class TouchStatus(models.Model):
    status_name = models.CharField(default='', max_length=50)
    description = models.TextField(default='', max_length=200)


    def __str__(self):
        return self.status_name


class Rawdata(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now())
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    touch_status = models.ForeignKey(TouchStatus, on_delete=models.CASCADE)
    acceleration = models.ForeignKey(Accelaration, on_delete=models.CASCADE)
    gyroscope = models.ForeignKey(Gyroscope, on_delete=models.CASCADE)
    rotation = models.ForeignKey(Rotation, on_delete=models.CASCADE)




    def save(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        sensor = [self.acceleration.getJson(), self.gyroscope.getJson(), self.rotation.getJson()]
        data = {'date':  str(self.date), 'device': self.device.__str__(), 'touch_status': self.touch_status.__str__(), 'data': sensor}
        async_to_sync(channel_layer.group_send)(
            'sensor_consumer_group', {
                'type': 'send_rawdata',
                'value': json.dumps(data),
            }
        )
        super(Rawdata, self).save(*args, **kwargs)






