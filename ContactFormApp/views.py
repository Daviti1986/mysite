from django.shortcuts import render, get_object_or_404, redirect
from .models import ContactFormApp
from suggestapp.models import Suggest
from CategoryApp.models import CategoryApp
from SubCategoryApp.models import SubCategoryApp
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
import datetime


# Create your views here.
def contact_add(request):

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

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        txt = request.POST.get('txt')


        if name == '' or email == '' or txt == '':
            msg = 'ALL Fields Requirded'
            return render(request, 'front/pages/msgbox.html', {'msg': msg})

        data = ContactFormApp(name=name, email=email, txt=txt, date=today, time=time)
        data.save()
        msg = 'Your Message Receved'
        return render(request, 'front/pages/msgbox.html', {'msg': msg})


    return render(request, 'front/pages/msgbox.html')


def contact_show(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    msg = ContactFormApp.objects.all()

    return render(request, 'back/pages/contact_form.html', {'msg': msg})

def contact_delete(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end
    delete = ContactFormApp.objects.filter(pk=pk)
    delete.delete()


    return redirect( 'contact_show', )