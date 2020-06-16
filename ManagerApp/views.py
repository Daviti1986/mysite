from django.shortcuts import render, get_object_or_404, redirect
from .models import ManagerApp
from suggestapp.models import Suggest
from CategoryApp.models import CategoryApp
from SubCategoryApp.models import SubCategoryApp
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from TrendingApp.models import TrendingApp
from django.contrib.auth.models import User
import random
from random import randint


# Create your views here.

def manager_list(request):

    manager = ManagerApp.objects.all()


    return render(request, 'back/pages/manager_list.html', {'manager': manager})

def manager_delete(request, pk) :

    uname = ManagerApp.objects.get(pk=pk)
    data = User.objects.filter(username= uname.usertxt)
    data.delete()

    uname.delete()

    return redirect('manager_list')