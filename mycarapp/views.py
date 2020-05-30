from django.shortcuts import render, get_object_or_404, redirect
from .models import MyCar
from suggestapp.models import Suggest


# Create your views here.

def home(requset):
    site = MyCar.objects.get(pk = 2)
    suggest = Suggest.objects.all()


    return render(requset, 'front/pages/home.html', {'site':site, 'suggest':suggest})


def about(requset):
    site = MyCar.objects.get(pk = 2)
    return render(requset, 'front/pages/about.html', {'site':site})

def panel(request):

    return render(request, 'back/pages/home.html')