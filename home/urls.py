from django.urls import path
from .views import *

urlpatterns = [
    path('', home),
    path('students/', generate_student_data),
]