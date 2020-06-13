from django.shortcuts import render, get_object_or_404, redirect
from .models import Suggest
from mycarapp.models import MyCar
from django.core.files.storage import FileSystemStorage
import datetime
from SubCategoryApp.models import SubCategoryApp
from CategoryApp.models import CategoryApp


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
    tagname = Suggest.objects.get(name=word).tag
    tag = tagname.split(',')

    try:
        mysuggest = Suggest.objects.get(name=word)
        mysuggest.show = mysuggest.show +1
        mysuggest.save()
    except:
        print("Can't Add show ")

    return render(request, 'front/pages/suggest_detail.html', {'site':site, 'suggest':suggest,
                                                               'cat':cat, 'subcat': subcat, 'lastsuggest': lastsuggest,
                                                               'showsuggest': showsuggest, 'popsuggest': popsuggest,
                                                               'popsuggestlimit': popsuggestlimit,
                                                               'tag': tag})

def suggest_list(request):

    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    suggest = Suggest.objects.all()
    return render(request, 'back/pages/suggest_list.html', {'suggest': suggest })

def suggest_add(request):



    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    if len(str(day)) == 1 :
        day = '0' + str(day)
    if len(str(month)) == 1 :
        month = '0' + str(month)
    today = str(year) + '/' + str(month) + '/' + str(day)
    time = str(now.hour) + ':' + str(now.minute)

    cat = SubCategoryApp.objects.all()

    if request.method == 'POST':
        suggesttitle = request.POST.get('suggesttitle')
        suggestname  = request.POST.get('suggestname')
        suggestcat   = request.POST.get('suggestcat')
        suggestshort = request.POST.get('suggestshort')
        suggesttxt   = request.POST.get('suggesttxt')
        suggestid    = request.POST.get('suggestcat')
        tag          = request.POST.get('tag')

        if suggesttitle == '' or suggestname == '' or suggestcat == '' or suggestshort == '' or suggesttxt == '':
            error = 'ALL Fields Requirded'
            return render(request, 'back/pages/error.html', {'error':error})

        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)


            if str(myfile.content_type).startswith('image'):

                if myfile.size < 5000000 :
                    suggestname = SubCategoryApp.objects.get(pk=suggestid).name
                    or_catid    = SubCategoryApp.objects.get(pk=suggestid).categoryid

                    data = Suggest(set_name = suggesttitle, name = suggestname,
                                   short_txt = suggestshort, body_txt = suggesttxt, catname = suggestname, catid = suggestid,
                                   date = today, picname = filename, picurl = url, writer = '-',
                                   show = 0, time = time, or_catid = or_catid, tag = tag)
                    data.save()

                    count = len(Suggest.objects.filter(or_catid = or_catid))

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


    return  redirect('suggest_list')

def suggest_edit(request, pk):


    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    if len(Suggest.objects.filter(pk=pk)) == 0 :
        error = "News Not Found"
        return render(request, 'back/pages/error.html', {'error': error})

    suggest = Suggest.objects.get(pk=pk)
    cat = SubCategoryApp.objects.all()

    if request.method == 'POST':
        suggesttitle = request.POST.get('suggesttitle')
        suggestname  = request.POST.get('suggestname')
        suggestcat   = request.POST.get('suggestcat')
        suggestshort = request.POST.get('suggestshort')
        suggesttxt   = request.POST.get('suggesttxt')
        suggestid    = request.POST.get('suggestcat')
        tag          = request.POST.get('tag')

        if suggesttitle == '' or suggestname == '' or suggestcat == '' or suggestshort == '' or suggesttxt == '':
            error = 'ALL Fields Requirded'
            return render(request, 'back/pages/error.html', {'error':error})

        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith('image'):

                if myfile.size < 5000000 :
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