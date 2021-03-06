from django.shortcuts import render, get_object_or_404, redirect
from .models import Suggest
from mycarapp.models import MyCar
from django.core.files.storage import FileSystemStorage
import datetime
from SubCategoryApp.models import SubCategoryApp
from CategoryApp.models import CategoryApp
from TrendingApp.models import TrendingApp
import random
from CommentApp.models import Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain

mysearch = ''

# Create your views here.
def suggest_detail(request, word):
    site = MyCar.objects.get(pk=2)
    suggest = Suggest.objects.all().order_by('-pk')
    cat = CategoryApp.objects.all()
    subcat = SubCategoryApp.objects.all()
    lastsuggest = Suggest.objects.all().order_by('-pk')[:3]

    showsuggest = Suggest.objects.filter(name=word)
    popsuggest = Suggest.objects.all().order_by('-show')
    popsuggestlimit = Suggest.objects.all().order_by('-show')[:3]
    trending = TrendingApp.objects.all().order_by('-pk')[:5]

    tagname = Suggest.objects.get(name=word).tag
    tag = tagname.split(',')

    try:
        mysuggest = Suggest.objects.get(name=word)
        mysuggest.show = mysuggest.show + 1
        mysuggest.save()
    except:
        print("Can't Add show ")
    code = Suggest.objects.get(name=word).pk
    comment = Comment.objects.filter(news_id=code, status=1).order_by('-pk')[:3]
    cmcount = len(comment)

    link = '/urls/' + str(Suggest.objects.get(name=word).rand)

    return render(request, 'front/pages/suggest_detail.html', {'site': site, 'suggest': suggest,
                                                               'cat': cat, 'subcat': subcat, 'lastsuggest': lastsuggest,
                                                               'showsuggest': showsuggest, 'popsuggest': popsuggest,
                                                               'popsuggestlimit': popsuggestlimit, 'tagname': tagname,
                                                               'trending': trending, 'code': code,
                                                               'comment': comment, 'cmcount': cmcount, 'link': link})

def suggest_detail_short(request, pk):
    site = MyCar.objects.get(pk=2)
    suggest = Suggest.objects.all().order_by('-pk')
    cat = CategoryApp.objects.all()
    subcat = SubCategoryApp.objects.all()
    lastsuggest = Suggest.objects.all().order_by('-pk')[:3]

    showsuggest = Suggest.objects.filter(rand=pk)
    popsuggest = Suggest.objects.all().order_by('-show')
    popsuggestlimit = Suggest.objects.all().order_by('-show')[:3]
    trending = TrendingApp.objects.all().order_by('-pk')[:5]

    tagname = Suggest.objects.get(rand=pk).tag
    tag = tagname.split(',')

    try:
        mysuggest = Suggest.objects.get(rand=pk)
        mysuggest.show = mysuggest.show + 1
        mysuggest.save()
    except:
        print("Can't Add show ")

    link = '/urls/' + str(Suggest.objects.get(name=word).rand)

    return render(request, 'front/pages/suggest_detail.html', {'site': site, 'suggest': suggest,
                                                               'cat': cat, 'subcat': subcat, 'lastsuggest': lastsuggest,
                                                               'showsuggest': showsuggest, 'popsuggest': popsuggest,
                                                               'popsuggestlimit': popsuggestlimit,
                                                               'tag': tag, 'trending': trending, 'link': link})


def suggest_list(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1
    if perm == 0:
        suggest = Suggest.objects.filter(writer=request.user)
    elif perm == 1:
        suggestpagin = Suggest.objects.all()
        paginator = Paginator(suggestpagin,1)
        page = request.GET.get('page')

        try:
            suggest = paginator.page(page)

        except EmptyPage :
            suggest = paginator.page(paginator.num_page)

        except PageNotAnInteger :
            suggest = paginator.page(1)


    return render(request, 'back/pages/suggest_list.html', {'suggest': suggest})


def suggest_add(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

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

    date = str(year) + str(month) + str(day)
    randint = str(random.randint(1000,9999))
    rand = date + randint
    rand = int(rand)

    while len(Suggest.objects.filter(rand=rand)) != 0:
        randint = str(random.randint(1000, 9999))
        rand = date + randint
        rand = int(rand)

    cat = SubCategoryApp.objects.all()

    if request.method == 'POST':
        suggesttitle = request.POST.get('suggesttitle')
        suggestname = request.POST.get('suggestname')
        suggestcat = request.POST.get('suggestcat')
        suggestshort = request.POST.get('suggestshort')
        suggesttxt = request.POST.get('suggesttxt')
        suggestid = request.POST.get('suggestcat')
        tag = request.POST.get('tag')

        if suggesttitle == '' or suggestname == '' or suggestcat == '' or suggestshort == '' or suggesttxt == '':
            error = 'ALL Fields Requirded'
            return render(request, 'back/pages/error.html', {'error': error})

        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith('image'):

                if myfile.size < 50000000:
                    suggestname = SubCategoryApp.objects.get(pk=suggestid).name
                    or_catid = SubCategoryApp.objects.get(pk=suggestid).categoryid

                    data = Suggest(set_name = suggesttitle, name = suggestname,
                                   short_txt = suggestshort, body_txt = suggesttxt, catname = suggestname, catid = suggestid,
                                   date = today, picname = filename, picurl = url, writer = request.user,
                                   show = 0, time = time, or_catid = or_catid, tag = tag, rand = rand)
                    print(rand)
                    data.save()


                    count = len(Suggest.objects.filter(or_catid=or_catid))

                    data = CategoryApp.objects.get(pk=or_catid)
                    data.count = count
                    data.save()

                    return redirect('suggest_list')

                else:
                    fs = FileSystemStorage()
                    fs.delete(filename)

                    error = "Your File Is Bigger Than 5 MB"
                    return render(request, 'back/pages/error.html', {'error': error})

            else:
                fs = FileSystemStorage()
                fs.delete(filename)

                error = "Your File Not Supported"
                return render(request, 'back/pages/error.html', {'error': error})

        except:
            error = "Please input your image"
            return render(request, 'back/pages/error.html', {'error': error})

    return render(request, 'back/pages/suggest_add.html', {'cat': cat})


def suggest_delete(request, pk):
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

    try:
        delete = Suggest.objects.get(pk=pk)
        fs = FileSystemStorage()
        fs.delete(delete.picname)
        orcatid = Suggest.objects.get(pk=pk).or_catid

        delete.delete()

        count = len(Suggest.objects.filter(or_catid=orcatid))
        Del = CategoryApp.objects.get(pk=orcatid)
        Del.count = count
        Del.save()

    except:
        error = "Something Wrong"
        return render(request, 'back/pages/error.html', {'error': error})

    return redirect('suggest_list')


def suggest_edit(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    if len(Suggest.objects.filter(pk=pk)) == 0:
        error = "News Not Found"
        return render(request, 'back/pages/error.html', {'error': error})

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser": perm = 1
    if perm == 0:
        master = Suggest.objects.get(pk=pk).writer
        if str(master) != str(request.user):
            error = 'Access Denied'
            return render(request, 'back/pages/error.html', {'error': error})

    suggest = Suggest.objects.get(pk=pk)
    cat = SubCategoryApp.objects.all()

    if request.method == 'POST':
        suggesttitle = request.POST.get('suggesttitle')
        suggestname = request.POST.get('suggestname')
        suggestcat = request.POST.get('suggestcat')
        suggestshort = request.POST.get('suggestshort')
        suggesttxt = request.POST.get('suggesttxt')
        suggestid = request.POST.get('suggestcat')
        tag = request.POST.get('tag')

        if suggesttitle == '' or suggestname == '' or suggestcat == '' or suggestshort == '' or suggesttxt == '':
            error = 'ALL Fields Requirded'
            return render(request, 'back/pages/error.html', {'error': error})

        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith('image'):

                if myfile.size < 5000000:
                    suggestname = SubCategoryApp.objects.get(pk=suggestid).name

                    data = Suggest.objects.get(pk=pk)

                    fss = FileSystemStorage()
                    fss.delete(data.picnanem)

                    data.name = suggesttitle
                    data.shor_txt = suggestshort
                    data.body_txt = suggesttxt
                    data.picname = filename
                    data.pcurl = url
                    data.catname = suggestname
                    data.catid = suggestid
                    data.tag = tag
                    data.act = 0

                    data.save()
                    return redirect('suggest_list')

                else:
                    fs = FileSystemStorage()
                    fs.delete(filename)

                    error = "Your File Is Bigger Than 5 MB"
                    return render(request, 'back/pages/error.html', {'error': error})

            else:
                fs = FileSystemStorage()
                fs.delete(filename)

                error = "Your File Not Supported"
                return render(request, 'back/pages/error.html', {'error': error})

        except:
            suggestname = SubCategoryApp.objects.get(pk=suggestid).name

            data = Suggest.objects.get(pk=pk)

            data.name = suggesttitle
            data.shor_txt = suggestshort
            data.body_txt = suggesttxt
            data.catname = suggestname
            data.catid = suggestid
            data.tag = tag

            data.save()
            return redirect('suggest_list')

    return render(request, 'back/pages/suggest_edit.html', {'pk': pk, 'suggest': suggest, 'cat': cat})


def suggest_publish(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    suggest = Suggest.objects.get(pk=pk)
    suggest.act = 1
    suggest.save()

    return redirect('suggest_list')

def suggest_all_show(request, word):

    catid = CategoryApp.objects.get(name=word).pk
    allsuggest = Suggest.objects.filter(or_catid=catid)

    site = MyCar.objects.get(pk=2)
    suggest = Suggest.objects.filter(act=1).order_by('-pk')
    cat = CategoryApp.objects.all()
    subcat = SubCategoryApp.objects.all()
    lastsuggest = Suggest.objects.filter(act=1).order_by('-pk')[:3]
    popsuggest = Suggest.objects.filter(act=1).order_by('-show')
    popsuggestlimit = Suggest.objects.filter(act=1).order_by('-show')[:3]
    trending = TrendingApp.objects.all().order_by('-pk')[:5]
    lastsuggesttwo = Suggest.objects.filter(act=1).order_by('-pk')[:3]

    paginator = Paginator(allsuggest, 12)
    page = request.GET.get('page')
    try:
        allsuggests = paginator.page(page)
    except EmptyPage :
        allsuggests = paginator.page(paginator.num_page)
    except PageNotAnInteger:
        allsuggests = paginator.page(1)
    return render(request, 'front/pages/all_news.html', {'site': site, 'suggest': suggest, 'cat': cat, 'subcat': subcat,
                                                     'lastsuggest': lastsuggest, 'popsuggest': popsuggest,
                                                     'popsuggestlimit': popsuggestlimit,
                                                     'trending': trending, 'lastsuggesttwo': lastsuggesttwo,
                                                         'allsuggest': allsuggest, 'allsuggests' : allsuggests})

def all_suggest(request):


    allsuggest = Suggest.objects.all()

    site = MyCar.objects.get(pk=2)
    suggest = Suggest.objects.filter(act=1).order_by('-pk')
    cat = CategoryApp.objects.all()
    subcat = SubCategoryApp.objects.all()
    lastsuggest = Suggest.objects.filter(act=1).order_by('-pk')[:3]
    popsuggest = Suggest.objects.filter(act=1).order_by('-show')
    popsuggestlimit = Suggest.objects.filter(act=1).order_by('-show')[:3]
    trending = TrendingApp.objects.all().order_by('-pk')[:5]
    lastsuggesttwo = Suggest.objects.filter(act=1).order_by('-pk')[:3]

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    if len(str(day)) == 1:
        day = '0' + str(day)
    if len(str(month)) == 1:
        month = '0' + str(month)
    today = str(year) + '/' + str(month) + '/' + str(day)
    f_rom = []
    t_o = []
    for i in range(30):
        date = datetime.datetime.now() - datetime.timedelta(days=i)
        year = date.year
        month = date.month
        day = date.day
        if len(str(day)) == 1:
            day = '0' + str(day)
        if len(str(month)) == 1:
            month = '0' + str(month)
        date = str(year) + '/' + str(month) + '/' + str(day)
        f_rom.append(date)
    for i in range(30):
        date = datetime.datetime.now() - datetime.timedelta(days=i)

        year = date.year
        month = date.month
        day = date.day
        if len(str(day)) == 1:
            day = '0' + str(day)
        if len(str(month)) == 1:
            month = '0' + str(month)
        date = str(year) + '/' + str(month) + '/' + str(day)
        t_o.append(date)

    paginator = Paginator(allsuggest, 12)
    page = request.GET.get('page')
    try:
        allsuggests = paginator.page(page)
    except EmptyPage:
        allsuggests = paginator.page(paginator.num_page)
    except PageNotAnInteger:
        allsuggests = paginator.page(1)
    return render(request, 'front/pages/all_suggest.html',
                      {'site': site, 'suggest': suggest, 'cat': cat, 'subcat': subcat,
                       'lastsuggest': lastsuggest, 'popsuggest': popsuggest,
                       'popsuggestlimit': popsuggestlimit,
                       'trending': trending, 'lastsuggesttwo': lastsuggesttwo,
                       'allsuggest': allsuggest, 'allsuggests': allsuggests, 'f_rom': f_rom, 't_o': t_o})


def all_suggest_search(request):

    if request.method == "POST":

        txt = request.POST.get('txt')
        catid = request.POST.get('cat')
        f_rom = request.POST.get('from')
        t_o = request.POST.get('to')
        mysearch = txt
        if f_rom != '0' and t_o != '0':
            if t_o < f_rom :
                msg = "Your To Date Most Be Littel Than From Date"
                return render(request, 'front/pages/msgbox.html', {'msg': msg})

        if catid == '0':
            if f_rom != '0' and t_o != '0':
                name_query = Suggest.objects.filter(name__contains=txt, date__gte=f_rom, date__lte=t_o)
                short_txt_query = Suggest.objects.filter(short_txt__contains = txt, date__gte=f_rom, date__lte=t_o)
                body_txt_query = Suggest.objects.filter(body_txt__contains=txt, date__gte=f_rom, date__lte=t_o)
            elif f_rom != '0' :
                name_query = Suggest.objects.filter(name__contains=txt, date__gte=f_rom)
                short_txt_query = Suggest.objects.filter(short_txt__contains = txt, date__gte=f_rom)
                body_txt_query = Suggest.objects.filter(body_txt__contains=txt, date__gte=f_rom)
            elif  t_o != '0':
                name_query = Suggest.objects.filter(name__contains=txt, date__lte=t_o)
                short_txt_query = Suggest.objects.filter(short_txt__contains = txt, date__lte=t_o)
                body_txt_query = Suggest.objects.filter(body_txt__contains=txt, date__lte=t_o)
            else:
                name_query = Suggest.objects.filter(name__contains=txt)
                short_txt_query = Suggest.objects.filter(short_txt__contains=txt)
                body_txt_query = Suggest.objects.filter(body_txt__contains=txt)

        else:
            if f_rom != '0' and t_o != '0':
                name_query = Suggest.objects.filter(name__contains=txt, or_catid=catid, date__gte=f_rom, date__lte=t_o)
                short_txt_query = Suggest.objects.filter(short_txt__contains=txt, or_catid=catid, date__gte=f_rom, date__lte=t_o)
                body_txt_query = Suggest.objects.filter(body_txt__contains=txt, or_catid=catid, date__gte=f_rom, date__lte=t_o)
            elif f_rom != '0' :
                name_query = Suggest.objects.filter(name__contains=txt, or_catid=catid, date__gte=f_rom)
                short_txt_query = Suggest.objects.filter(short_txt__contains=txt, or_catid=catid, date__gte=f_rom)
                body_txt_query = Suggest.objects.filter(body_txt__contains=txt, or_catid=catid, date__gte=f_rom)
            elif t_o != '0':
                name_query = Suggest.objects.filter(name__contains=txt, or_catid=catid, date__lte=t_o)
                short_txt_query = Suggest.objects.filter(short_txt__contains=txt, or_catid=catid, date__lte=t_o)
                body_txt_query = Suggest.objects.filter(body_txt__contains=txt, or_catid=catid, date__lte=t_o)
            else:
                name_query = Suggest.objects.filter(name__contains=txt, or_catid=catid)
                short_txt_query = Suggest.objects.filter(short_txt__contains=txt, or_catid=catid)
                body_txt_query = Suggest.objects.filter(body_txt__contains=txt, or_catid=catid)



        allsuggest = list(chain(name_query, short_txt_query, body_txt_query))
        allsuggest = list(dict.fromkeys(allsuggest))
    else:
        if catid == '0':
            if f_rom != '0' and t_o != '0':
                name_query = Suggest.objects.filter(name__contains = mysearch, date__gte=f_rom, date__lte=t_o)
                short_txt_query = Suggest.objects.filter(short_txt__contains = mysearch, date__gte=f_rom, date__lte=t_o)
                body_txt_query = Suggest.objects.filter(body_txt__contains=mysearch, date__gte=f_rom, date__lte=t_o)
            elif f_rom != '0' :
                name_query = Suggest.objects.filter(name__contains = mysearch, date__gte=f_rom)
                short_txt_query = Suggest.objects.filter(short_txt__contains = mysearch, date__gte=f_rom)
                body_txt_query = Suggest.objects.filter(body_txt__contains=mysearch, date__gte=f_rom)
            elif t_o != '0':
                name_query = Suggest.objects.filter(name__contains = mysearch, date__lte=t_o)
                short_txt_query = Suggest.objects.filter(short_txt__contains = mysearch, date__lte=t_o)
                body_txt_query = Suggest.objects.filter(body_txt__contains=mysearch, date__lte=t_o)
            else:
                name_query = Suggest.objects.filter(name__contains=mysearch)
                short_txt_query = Suggest.objects.filter(short_txt__contains=mysearch)
                body_txt_query = Suggest.objects.filter(body_txt__contains=mysearch)
        else:
            if f_rom != '0' and t_o != '0':
                name_query = Suggest.objects.filter(name__contains=mysearch, or_catid=catid, date__gte=f_rom, date__lte=t_o)
                short_txt_query = Suggest.objects.filter(short_txt__contains=mysearch, or_catid=catid, date__gte=f_rom, date__lte=t_o)
                body_txt_query = Suggest.objects.filter(body_txt__contains=mysearch, or_catid=catid, date__gte=f_rom, date__lte=t_o)
            elif f_rom != '0' :
                name_query = Suggest.objects.filter(name__contains=mysearch, or_catid=catid, date__gte=f_rom)
                short_txt_query = Suggest.objects.filter(short_txt__contains=mysearch, or_catid=catid, date__gte=f_rom)
                body_txt_query = Suggest.objects.filter(body_txt__contains=mysearch, or_catid=catid, date__gte=f_rom)
            elif t_o != '0':
                name_query = Suggest.objects.filter(name__contains=mysearch, or_catid=catid, date__lte=t_o)
                short_txt_query = Suggest.objects.filter(short_txt__contains=mysearch, or_catid=catid, date__lte=t_o)
                body_txt_query = Suggest.objects.filter(body_txt__contains=mysearch, or_catid=catid, date__lte=t_o)
            else:
                name_query = Suggest.objects.filter(name__contains=mysearch, or_catid=catid)
                short_txt_query = Suggest.objects.filter(short_txt__contains=mysearch, or_catid=catid)
                body_txt_query = Suggest.objects.filter(body_txt__contains=mysearch, or_catid=catid)
        allsuggest = list(chain(name_query, short_txt_query, body_txt_query))
        allsuggest = list(dict.fromkeys(allsuggest))


    site = MyCar.objects.get(pk=2)
    suggest = Suggest.objects.filter(act=1).order_by('-pk')
    cat = CategoryApp.objects.all()
    subcat = SubCategoryApp.objects.all()
    lastsuggest = Suggest.objects.filter(act=1).order_by('-pk')[:3]
    popsuggest = Suggest.objects.filter(act=1).order_by('-show')
    popsuggestlimit = Suggest.objects.filter(act=1).order_by('-show')[:3]
    trending = TrendingApp.objects.all().order_by('-pk')[:5]
    lastsuggesttwo = Suggest.objects.filter(act=1).order_by('-pk')[:3]

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    if len(str(day)) == 1:
        day = '0' + str(day)
    if len(str(month)) == 1:
        month = '0' + str(month)
    today = str(year) + '/' + str(month) + '/' + str(day)
    f_rom = []
    t_o = []
    for i in range(30):
        data = datetime.datetime.now() - datetime.timedelta(days=i)

        year = data.year
        month = data.month
        day = data.day
        if len(str(day)) == 1:
            day = '0' + str(day)
        if len(str(month)) == 1:
            month = '0' + str(month)
        data = str(year) + '/' + str(month) + '/' + str(day)
        f_rom.append(data)
    for i in range(30):
        data = datetime.datetime.now() - datetime.timedelta(days=i)

        year = data.year
        month = data.month
        day = data.day
        if len(str(day)) == 1:
            day = '0' + str(day)
        if len(str(month)) == 1:
            month = '0' + str(month)
        data = str(year) + '/' + str(month) + '/' + str(day)
        t_o.append(data)






    paginator = Paginator(allsuggest, 12)
    page = request.GET.get('page')
    try:
        allsuggest = paginator.page(page)
    except EmptyPage:
        allsuggest = paginator.page(paginator.num_page)
    except PageNotAnInteger:
        allsuggest = paginator.page(1)

    return render(request, 'front/pages/all_suggest.html',
                      {'site': site, 'suggest': suggest, 'cat': cat, 'subcat': subcat,
                       'lastsuggest': lastsuggest, 'popsuggest': popsuggest,
                       'popsuggestlimit': popsuggestlimit,
                       'trending': trending, 'lastsuggesttwo': lastsuggesttwo,
                       'allsuggest': allsuggest, 'f_rom': f_rom, 't_o': t_o})


#data = Suggest.objects.filter(date__gte='2020/02/02')
#data = Suggest.objects.filter(date__lte='2020/02/02')
#Suggest.objects.filter(pk=pk).exclude(date_gte='2020/02=1/01')
#Suggest.objects.filter(pk=pk).exclude(pk=10)
