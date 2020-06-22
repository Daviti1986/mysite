from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment
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

# create your views here.

def news_cm_add(request, pk):

    if request.method == 'POST' :
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
        if len(str(day)) == 1:
            day = '0' + str(day)
        if len(str(month)) == 1:
            month = '0' + str(month)
        today = str(year) + '/' + str(month) + '/' + str(day)
        time = str(now.hour) + ':' + str(now.minute)

        cm = request.POST.get('msg')
        name = request.POST.get('name')
        email = request.POST.get('email')

        if request.user.is_authenticated :
            manager = ManagerApp.objects.get(usertxt = request.user)
            data = Comment(name=manager.name, email = manager.email, cm = cm, news_id = pk, date = today, time = time )
            data.save()
        else:


            data = Comment(name=name, email=email, cm=cm, news_id = pk, date = today, time = time)
            data.save()

    newsname = Suggest.objects.get(pk = pk).name

    return redirect('suggest_detail', word = newsname)

def comments_list(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1
    if perm == 0:
        master = Suggest.objects.get(pk=pk).writer
        if str(master) != str(request.user):
            error = 'Access Denied'
            return render(request, 'back/pages/error.html', {'error': error})

    comment = Comment.objects.all()



    return render(request, 'back/pages/comments_list.html', {'comment': comment})


def comments_delete(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1
    if perm == 0:
        master = Suggest.objects.get(pk=pk).writer
        if str(master) != str(request.user):
            error = 'Access Denied'
            return render(request, 'back/pages/error.html', {'error': error})

    comment = Comment.objects.filter(pk=pk)
    comment.delete()



    return redirect('comments_list')


def comments_confirmed(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1
    if perm == 0:
        master = Suggest.objects.get(pk=pk).writer
        if str(master) != str(request.user):
            error = 'Access Denied'
            return render(request, 'back/pages/error.html', {'error': error})

    comment = Comment.objects.get(pk=pk)
    comment.status = 1
    comment.save()


    return redirect('comments_list')