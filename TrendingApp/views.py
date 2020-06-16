from django.shortcuts import render, get_object_or_404, redirect
from .models import TrendingApp
from suggestapp.models import Suggest
from CategoryApp.models import CategoryApp
from SubCategoryApp.models import SubCategoryApp
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage

# Create your views here.


def trending_add(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    if request.method == 'POST':
        txt = request.POST.get('txt')

        if txt == '':
            error = 'ALL Fields Requirded'
            return render(request, 'back/pages/error.html', {'error': error})

        data = TrendingApp(txt=txt)
        data.save()

    trendinglist = TrendingApp.objects.all()



    return render(request, 'back/pages/trending.html', {'trendinglist': trendinglist})


def trending_delete(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    data = TrendingApp.objects.filter(pk=pk)
    data.delete()

    return redirect( 'trending_add')

def trending_edit(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    mytxt = TrendingApp.objects.get(pk=pk).txt
    if request.method == "POST":
        txt = request.POST.get('txt')
        if txt == '':
            error = 'ALL Fields Requirded'
            return render(request, 'back/pages/error.html', {'error': error})
        data = TrendingApp.objects.get(pk=pk)
        data.txt = txt
        data.save()
        return redirect('trending_add')

    return render(request, 'back/pages/trending_edit.html', {'mytxt': mytxt, 'pk': pk})
