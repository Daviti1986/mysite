from django.shortcuts import render, get_object_or_404, redirect
from .models import Suggest
from mycarapp.models import MyCar


# Create your views here.
def suggest_detail(request, word):
    site = MyCar.objects.get(pk=2)
    suggest = Suggest.objects.filter(name=word)


    return render(request, 'front/pages/suggest_detail.html', {'suggest': suggest, 'site': site })

def suggest_list(request):

    suggest = Suggest.objects.all()
    return render(request, 'back/pages/suggest_list.html', {'sugest': suggest })
