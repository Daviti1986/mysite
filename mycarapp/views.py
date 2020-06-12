from django.shortcuts import render, get_object_or_404, redirect
from .models import MyCar
from suggestapp.models import Suggest
from CategoryApp.models import CategoryApp
from SubCategoryApp.models import SubCategoryApp
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage


# Create your views here.

def home(request):
    site = MyCar.objects.get(pk = 2)
    suggest = Suggest.objects.all().order_by('-pk')
    cat = CategoryApp.objects.all()
    subcat = SubCategoryApp.objects.all()
    lastsuggest = Suggest.objects.all().order_by('-pk')[:3]
    popsuggest = Suggest.objects.all().order_by('-show')
    popsuggestlimit = Suggest.objects.all().order_by('-show')[:3]
    return render(request, 'front/pages/home.html', {'site':site, 'suggest':suggest, 'cat':cat, 'subcat': subcat,
                                                     'lastsuggest':lastsuggest, 'popsuggest':popsuggest,
                                                     'popsuggestlimit': popsuggestlimit})


def about(request):
    site = MyCar.objects.get(pk = 2)
    return render(request, 'front/pages/about.html', {'site':site})

def panel(request):
    # login check start
    if not request.user.is_authenticated :
        return redirect('my_login')
    # login check end
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

def my_logout(request):

    logout(request)
    return redirect('my_login')

def site_setting(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end



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







