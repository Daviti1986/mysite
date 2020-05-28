from django.shortcuts import render, get_object_or_404, redirect

from .models import MyCar


# Create your views here.

def home(requset):
    site = MyCar.objects.get(pk = 2)
    return render(requset, 'front/pages/home.html', {'site':site,})


def about(requset):
    site = MyCar.objects.get(pk = 2)
    return render(requset, 'front/pages/about.html', {'site':site})