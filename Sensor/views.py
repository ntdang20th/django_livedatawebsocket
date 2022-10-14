from django.shortcuts import render
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import time
from .thread import *

from django.http import JsonResponse

async def home_sensor(request):

    # for i in range(1, 10):
    #     channel_layer = get_channel_layer()
    #     data = {'count': i}
    #     await(channel_layer.group_send)(
    #         'sensor_consumer_group', {
    #             'type': 'send_rawdata',
    #             'value': json.dumps(data),
    #         }
    #     )
    #     time.sleep(1)
    return render(request, 'home_sensor.html')

def generate_sensors_data(request):
    total = request.GET.get('total')
    CreateSensorsThread(int(total)).start()
    return JsonResponse({'status': 200})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.core import mail
from django.views.decorators.csrf import csrf_exempt

connection = mail.get_connection()
@csrf_exempt
@api_view(['POST'])
def ResponesData(request):
    data = request.data

    current_time = data['date']
    try:
        device = Device.objects.get(dv_name=data['UUID'])
    except Device.DoesNotExist:
        device = Device.objects.create(dv_name=data['UUID'], description='unknown device')
    touch = TouchStatus.objects.get(status_name='no touch detected')

    acceleration = data['data'][0]
    gyroscope = data['data'][1]
    rotation = data['data'][2]

    acceleration_sensor = Accelaration.objects.create(
        valueX=acceleration['valueX'],
        valueY=acceleration['valueY'],
        valueZ=acceleration['valueZ'],
        unit=Unit.objects.get(pk=1)
    )
    gyroscope_sensor = Gyroscope.objects.create(
        valueX=gyroscope['valueX'],
        valueY=gyroscope['valueY'],
        valueZ=gyroscope['valueZ'],
        unit=Unit.objects.get(pk=2)
    )
    rotation_sensor = Rotation.objects.create(
        valueX=rotation['RotationX'],
        valueY=rotation['RotationY'],
        valueZ=rotation['RotationZ'],
        unit=Unit.objects.get(pk=3)
    )

    #create new rawdata
    try:
        date = datetime.datetime.strptime(current_time, 'YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] format.')
    except ValueError as err:
        print(err)

    rawdata = Rawdata.objects.create(
        date=current_time,
        device=device,
        touch_status=touch,
        acceleration=acceleration_sensor,
        gyroscope=gyroscope_sensor,
        rotation=rotation_sensor
    )

    print(rawdata)








    # connection.open()
    # send_mail(
    #     'Reply mess!!',
    #     json_string,
    #     settings.EMAIL_HOST_USER,
    #     ['ntdang_20th@student.agu.edu.vn', 'eliane.schroeter@gmail.com'],
    #     connection=connection,
    # )
    # connection.close()
    return Response(request.data)