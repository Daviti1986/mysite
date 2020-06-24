from django.shortcuts import render, get_object_or_404, redirect
from .models import blacklist
from suggestapp.models import Suggest
from CategoryApp.models import CategoryApp
from SubCategoryApp.models import SubCategoryApp
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from TrendingApp.models import TrendingApp
from django.contrib.auth.models import User, Group, Permission
from ManagerApp.models import ManagerApp
import datetime
import string
import random
from random import randint

# Create your views here.


def black_list(request):

    ip = blacklist.objects.all()


    return render(request, 'back/pages/blacklist.html', {'ip':ip})


def ip_add(request):

    if request.method == 'POST':

        ip = request.POST.get('ip')
        if ip != '':
            data = blacklist(ip=ip)
            data.save()

    return redirect('black_list')


def ip_delete(request, pk):

    delete = blacklist.objects.filter(pk = pk)
    delete.delete()
    return redirect('black_list')