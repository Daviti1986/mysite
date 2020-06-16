from django.shortcuts import render, get_object_or_404, redirect
from .models import ManagerApp
from suggestapp.models import Suggest
from CategoryApp.models import CategoryApp
from SubCategoryApp.models import SubCategoryApp
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from TrendingApp.models import TrendingApp
from django.contrib.auth.models import User, Group, Permission
import random
from random import randint


# Create your views here.

def manager_list(request):

    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1
    if perm == 0:
        error = 'Access Denied'
        return render(request, 'back/pages/error.html', {'error': error})

    manager = ManagerApp.objects.all()


    return render(request, 'back/pages/manager_list.html', {'manager': manager})

def manager_delete(request, pk) :

    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end


    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1
    if perm == 0:
        error = 'Access Denied'
        return render(request, 'back/pages/error.html', {'error': error})

    uname = ManagerApp.objects.get(pk=pk)
    data = User.objects.filter(username= uname.usertxt)
    data.delete()

    uname.delete()

    return redirect('manager_list')

def manager_group(request):

    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1
    if perm == 0 :
        error = 'Access Denied'
        return render(request, 'back/pages/error.html', {'error': error})

    group = Group.objects.all().exclude(name='masteruser')


    return render(request, 'back/pages/manager_group.html', {'group': group})

def manager_group_add(request):

    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1
    if perm == 0:
        error = 'Access Denied'
        return render(request, 'back/pages/error.html', {'error': error})

    if request.method == "POST":
        name = request.POST.get('name')

        if name != '':
            if len(Group.objects.filter(name = name)) == 0 :

                group = Group(name=name)
                group.save()




    return redirect('manager_group')

def manager_group_delete(request, name):


    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end


    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1
    if perm == 0:
        error = 'Access Denied'
        return render(request, 'back/pages/error.html', {'error': error})

    data = Group.objects.filter(name=name)
    data.delete()

    return redirect('manager_group')

def users_group(request, pk):

    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1
    if perm == 0:
        error = 'Access Denied'
        return render(request, 'back/pages/error.html', {'error': error})

    manager = ManagerApp.objects.get(pk=pk)
    user = User.objects.get(username = manager.usertxt)

    user_group = []
    for i in user.groups.all():
        user_group.append(i.name)

    group = Group.objects.all()

    return render(request, 'back/pages/users_groups.html', {'user_group': user_group, 'group': group, 'pk': pk})

def add_users_to_group(request, pk):

    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1
    if perm == 0:
        error = 'Access Denied'
        return render(request, 'back/pages/error.html', {'error': error})

    if request.method == 'POST' :

        groupname = request.POST.get('groupname')
        group = Group.objects.get(name=groupname)
        manager = ManagerApp.objects.get(pk=pk)
        user = User.objects.get(username=manager.usertxt)
        user.groups.add(group)

    return redirect('users_group', pk=pk)

def delete_users_to_group(request, pk, name):

    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1
    if perm == 0:
        error = 'Access Denied'
        return render(request, 'back/pages/error.html', {'error': error})

    group = Group.objects.get(name=name)
    manager = ManagerApp.objects.get(pk=pk)
    user = User.objects.get(username=manager.usertxt)
    user.groups.remove(group)

    return redirect('users_group', pk=pk)