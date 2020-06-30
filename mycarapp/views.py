from django.shortcuts import render, get_object_or_404, redirect
from .models import MyCar
from suggestapp.models import Suggest
from CategoryApp.models import CategoryApp
from SubCategoryApp.models import SubCategoryApp
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from TrendingApp.models import TrendingApp
from django.contrib.auth.models import User, Group, Permission
from ManagerApp.models import ManagerApp
from ipware import get_client_ip
from ip2geotools.databases.noncommercial import DbIpCity
from BlackListApp.models import blacklist
from django.core.mail import send_mail
from django.conf import settings
from ContactFormApp.models import ContactFormApp




import string
import random
from random import randint




# Create your views here.

def home(request):
    site = MyCar.objects.get(pk = 2)
    suggest = Suggest.objects.filter(act=1).order_by('-pk')
    cat = CategoryApp.objects.all()
    subcat = SubCategoryApp.objects.all()
    lastsuggest = Suggest.objects.filter(act=1).order_by('-pk')[:3]
    popsuggest = Suggest.objects.filter(act=1).order_by('-show')
    popsuggestlimit = Suggest.objects.filter(act=1).order_by('-show')[:3]
    trending = TrendingApp.objects.all().order_by('-pk')[:5]
    lastsuggesttwo = Suggest.objects.filter(act=1).order_by('-pk')[:3]


    return render(request, 'front/pages/home.html', {'site':site, 'suggest':suggest, 'cat':cat, 'subcat': subcat,
                                                     'lastsuggest':lastsuggest, 'popsuggest':popsuggest,
                                                     'popsuggestlimit': popsuggestlimit,
                                                     'trending': trending, 'lastsuggesttwo': lastsuggesttwo})


def about(request):
    site = MyCar.objects.get(pk = 2)
    suggest = Suggest.objects.all().order_by('-pk')
    cat = CategoryApp.objects.all()
    subcat = SubCategoryApp.objects.all()
    lastsuggest = Suggest.objects.all().order_by('-pk')[:3]
    popsuggestlimit = Suggest.objects.all().order_by('-show')[:3]
    trending = TrendingApp.objects.all().order_by('-pk')[:5]
    return render(request, 'front/pages/about.html', {'site':site, 'suggest':suggest, 'cat':cat, 'subcat': subcat,
                                                     'lastsuggest':lastsuggest,
                                                     'popsuggestlimit': popsuggestlimit, 'trending': trending})

def panel(request):
    # login check start
    if not request.user.is_authenticated :
        return redirect('my_login')
    # login check end

    perm = 0
    perm = Permission.objects.filter(user=request.user)
    for i in perm :
        if i.codename == 'masteruser' :
            perm = 1
    '''''
    test= ['!', '@', '#', '$', '%']
    rand = ''
    for i in range(4):
        rand = rand + random.choice(string.ascii_letters )
        rand += random.choice(test)
        rand += str(random.randint(0,9))
    


    count = Suggest.objects.count()
    rand = Suggest.objects.all()[random.randint(0, count-1)]
    '''






    return render(request, 'back/pages/home.html')




def my_login(request):
    if request.method == 'POST':
        utxt = request.POST.get('username')
        ptxt = request.POST.get('password')

        if utxt != '' and ptxt != '':
            user = authenticate(username = utxt, password = ptxt)

            if user != None :

                login(request, user)
                return redirect('panel')

    return render(request, 'front/pages/login.html')

def my_register(request):

    if request.method == 'POST':
        uname = request.POST.get('user-name')
        ufirstname = request.POST.get('register-firstname')
        ulastname = request.POST.get('register-lastname')
        uage = request.POST.get('register-age')
        uemail = request.POST.get('register-email')
        upass = request.POST.get('register-password')
        uchpass = request.POST.get('register-password-verify')

        if ufirstname == '' and ulastname == '' and uage == '':
            msg = 'Your Pass Did not Match'
            return render(request, 'front/pages/msgbox.html', {'msg': msg})

        if upass != uchpass :
            msg = 'Your Pass Did not Match'
            return render(request, 'front/pages/msgbox.html', {'msg': msg})
        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        for i in upass:

            if i > '0' and i < '9':
                count1 = 1
            if i > 'A' and i < 'Z':
                count2 = 1
            if i > 'a' and i < 'z':
                count3 = 1
            if i > '!' and i < '(':
                count4 = 1

        if count1 == 0 or count2 == 0 or count3 == 0 or count4 == 0 :
            msg = 'Your Pass IS Not Strong'
            return render(request, 'front/pages/msgbox.html', {'msg': msg})

        if len(upass) < 8 :
            msg = 'Your Pass Most Be 8 Character'
            return render(request, 'front/pages/msgbox.html', {'msg': msg})
        if len(User.objects.filter(username = uname)) == 0 and len(User.objects.filter(email = uemail)) == 0 :
            ip, is_routable = get_client_ip(request)
            if ip is None:
                ip = '0.0.0.0'

            try:
                response = DbIpCity.get(ip, api_key='free')
                country = response.country + ' | ' + response.city
            except:
                country = 'Unknown'


            user = User.objects.create_user(username=uname, email= uemail, password=upass)
            data = ManagerApp(name=ufirstname, usertxt= uname, email = uemail, age = uage,
                              lastname = ulastname, ip=ip, country = country )
            data.save()

    return render(request, 'front/pages/login.html')

def my_logout(request):

    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')

        if user == '' or password == '' :
            user = authenticate(username= user, password = password)
            if user != None :

                login(request, user)
                return redirect('panel')



def site_setting(request):
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



    if request.method == 'POST':
        name = request.POST.get('name')
        tell = request.POST.get('tell')
        fb = request.POST.get('fb')
        tw = request.POST.get('tw')
        yt = request.POST.get('yt')
        link = request.POST.get('link')
        txt = request.POST.get('txt')

        if fb   == '':
            fb = '#'
        if tw   == '':
            tw = '#'
        if yt   == '':
            yt = '#'
        if link == '':
            link = '#'
        if name == '' or tell == '' or txt == '':
            error = "Please input your image"
            return render(request, 'back/pages/error.html', {'error': error})

        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            picurl = url
            picname = filename
        except:
            picurl = '-'
            picname = '-'

        try:
            myfile2 = request.FILES['myfile2']
            fs2 = FileSystemStorage()
            filename2 = fs2.save(myfile2.name, myfile2)
            url2 = fs2.url(filename2)

            picurl2 = url2
            picname2 = filename2
        except:
            picurl2 = '-'
            picname2 = '-'

        data = MyCar.objects.get(pk = 2)
        data.name =name
        data.tell = tell
        data.fb = fb
        data.tw = tw
        data.yt = yt
        data.link = link
        data.about = txt

        if picurl != '-':
            data.picurl = picurl
        if picname != '-':
            data.picname = picname
        if picurl2 != '-':
            data.picurl2 = picurl2
        if picname2 != '-':
            data.picname2 = picname2
        data.save()



    site = MyCar.objects.get(pk=2)
    return render(request, 'back/pages/setting.html', {'site': site})

def about_setting(request):
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

    if request.method == 'POST':
        txt = request.POST.get('txt')

        if txt == '':
            error = 'ALL Fields Requirded'
            return render(request, 'back/pages/error.html', {'error': error})
        data = MyCar.objects.get(pk=2)
        data.abouttxt = txt
        data.save()

    about = MyCar.objects.get(pk=2).abouttxt



    return render(request, 'back/pages/about_setting.html', {'about': about})

def contact(request):
    site = MyCar.objects.get(pk=2)
    suggest = Suggest.objects.all().order_by('-pk')
    cat = CategoryApp.objects.all()
    subcat = SubCategoryApp.objects.all()
    lastsuggest = Suggest.objects.all().order_by('-pk')[:3]
    popsuggestlimit = Suggest.objects.all().order_by('-show')[:3]
    trending = TrendingApp.objects.all().order_by('-pk')[:5]



    return render(request, 'front/pages/contact.html', {'site':site, 'suggest':suggest, 'cat':cat, 'subcat': subcat,
                                                     'lastsuggest':lastsuggest,
                                                     'popsuggestlimit': popsuggestlimit, 'trending': trending})


def change_pass(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    if request.method == 'POST':

        oldpass = request.POST.get('oldpass')
        newpass = request.POST.get('newpass')

        if oldpass == '' or newpass == '':
            error = 'ALL Fields Requirded'
            return render(request, 'back/pages/error.html', {'error': error})
        user = authenticate(username=request.user, password=oldpass)

        if user != None:

            if len(newpass) < 8 :
                error = 'Your Password Most Be AT less 8 Character'
                return render(request, 'back/pages/error.html', {'error': error})

            count1  = 0
            count2 = 0
            count3 = 0
            count4 = 0
            for i in newpass:

                if i > '0' and i < '9' :
                    count1 = 1
                if i > 'A' and i < 'Z' :
                    count2 = 1
                if i > 'a' and i < 'z' :
                    count3 = 1
                if i > '!' and i < '(':
                    count4 = 1

            print('count', count1, count2, count3, count4)
            if  count1 == 1 and count2 == 1 and count3 == 1 and count4 == 1 :

                user = User.objects.get(username= request.user)
                user.set_password(newpass)
                user.save()
                return redirect('my_logout')


        else:
            error = 'Your Password Is Not Correct'
            return render(request, 'back/pages/error.html', {'error': error})




    return render(request, 'back/pages/changepass.html')

def answer_cm(request, pk):

    if request.method == 'POST':
        txt = request.POST.get('txt')
        if txt == '':
            error = 'Type Your Answer'
            return render(request, 'back/pages/error.html', {'error': error})
        to_email = ContactFormApp.objects.get(pk=pk).email

        subjects = 'answer form'
        message = txt
        email_from = settings.EMAIL_HOST_USER
        emails = [to_email]
        send_mail(subjects, message, email_from, emails)
        '''
        send_mail(
            'sender number 2',
            txt,
            'admin@dalaudi.ge',
            [to_email],
            fail_silently=False,
        )
        '''

    return render(request, 'back/pages/answer_cm.html', {'pk':pk})














