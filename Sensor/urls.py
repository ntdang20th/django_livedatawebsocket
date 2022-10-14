from django.urls import path
from .views import *

urlpatterns = [
    path('', home_sensor),
    path('send/', generate_sensors_data),
    path('post/', ResponesData)
]