from django.contrib import admin
from .models import MyCar
from django.contrib.auth.models import Permission


# Register your models here.
admin.site.register(MyCar)
admin.site.register(Permission)