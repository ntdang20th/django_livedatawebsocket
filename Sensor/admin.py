from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Device)
admin.site.register(Unit)
admin.site.register(Accelaration)
admin.site.register(Gyroscope)
admin.site.register(Rotation)
admin.site.register(Patient)
admin.site.register(Familiar)
admin.site.register(TouchStatus)
admin.site.register(Rawdata)