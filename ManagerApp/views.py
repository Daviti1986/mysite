from django.shortcuts import render, get_object_or_404, redirect
from .models import ManagerApp
from suggestapp.models import Suggest
from CategoryApp.models import CategoryApp
from SubCategoryApp.models import SubCategoryApp
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from TrendingApp.models import TrendingApp
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
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


def manager_permissions(request):

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

    perms = Permission.objects.all()

    return render(request, 'back/pages/manager_permissions.html', {'perms': perms})

def manager_permissions_delete(request, name):

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

    perms = Permission.objects.filter(name=name)
    perms.delete()

    return redirect('manager_permissions')

def manager_permissions_add(request):

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

    if request.method == 'POST' :
        name = request.POST.get('name')
        code_name = request.POST.get('code_name')

        if len(Permission.objects.filter(codename = code_name)) == 0 :
            content_type = ContentType.objects.get(app_label='mycarapp', model = 'MyCar')
            permission = Permission.objects.create(codename=code_name, name=name, content_type = content_type)

        else:
            error = 'This Code Name Used Before'
            return render(request, 'back/pages/error.html', {'error': error})

    return redirect('manager_permissions')

def users_permissions(request, pk):

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

    permissions = Permission.objects.filter(user=user)


    user_perms = []
    for i in permissions:
        user_perms.append(i.name)

    perms = Permission.objects.all()


    return render(request, 'back/pages/users_permissions.html', {'user_perms': user_perms, 'pk': pk, 'perms': perms})


def users_permissions_delete(request, pk, name):
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
    user = User.objects.get(username=manager.usertxt)

    permissions = Permission.objects.get(name=name)
    user.user_permissions.remove(permissions)



    return redirect("users_permissions", pk=pk)



def users_permissions_add(request, pk):
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

        permissionsname = request.POST.get('permissionsname')

        manager = ManagerApp.objects.get(pk=pk)
        user = User.objects.get(username=manager.usertxt)

        permissions = Permission.objects.get(name=permissionsname)
        user.user_permissions.add(permissions)



    return redirect("users_permissions", pk=pk)


def groups_permissions(request, name):

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

    group =Group.objects.get(name=name)
    perms = group.permissions.all()

    allperms = Permission.objects.all()



    return render(request, 'back/pages/groups_permissions.html', {'perms': perms, 'name': name, 'allperms': allperms })

def groups_permissions_delete(request, group_name, name):

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
    group = Group.objects.get(name=group_name)
    perm = Permission.objects.get(name=name)

    group.permissions.remove(perm)



    return redirect('groups_permissions', name=group_name)

def groups_permissions_add(request, name):

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

        permissionsname = request.POST.get('permissionsname')
        group = Group.objects.get(name=name)
        permissions = Permission.objects.get(name=permissionsname)

        group.permissions.add(permissions)



    return redirect('groups_permissions', name=name)
