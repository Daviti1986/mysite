from django.shortcuts import render, get_object_or_404, redirect
from .models import NewsLetterApp
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

def news_letter(request):

    if request.method == 'POST' :
        txt = request.POST.get('txt')

        result = txt.find('@')

        if int(result) != -1 :
            data = NewsLetterApp(txt=txt, status=1)
            data.save()
        else:
            try:
                int(txt)
                data = NewsLetterApp(txt=txt, status=2)
                data.save()
            except:
                return redirect('home')


    return redirect('home')

def news_email(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    email = NewsLetterApp.objects.filter(status=1)



    return render(request, 'back/pages/emails.html', {'email': email})


def news_phones(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    phones = NewsLetterApp.objects.filter(status=2)



    return render(request, 'back/pages/phones.html', {'phones': phones})

def news_txt_delete(request, pk, num):
    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    data = NewsLetterApp.objects.get(pk=pk)
    data.delete()

    if int(num) == 2 :
        return redirect('news_phones')

    return redirect('news_email')