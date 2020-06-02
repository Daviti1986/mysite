from django.shortcuts import render, get_object_or_404, redirect
from .models import Suggest
from mycarapp.models import MyCar
from django.core.files.storage import FileSystemStorage
import datetime


# Create your views here.
def suggest_detail(request, word):
    site = MyCar.objects.get(pk=2)
    suggest = Suggest.objects.filter(name=word)


    return render(request, 'front/pages/suggest_detail.html', {'suggest': suggest, 'site': site })

def suggest_list(request):

    suggest = Suggest.objects.all()
    return render(request, 'back/pages/suggest_list.html', {'suggest': suggest })

def suggest_add(request):

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

    if request.method == 'POST':
        suggesttitle = request.POST.get('suggesttitle')
        suggestname  = request.POST.get('suggestname')
        suggestcat   = request.POST.get('suggestcat')
        suggestshort = request.POST.get('suggestshort')
        suggesttxt   = request.POST.get('suggesttxt')

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
                    data = Suggest(set_name = suggesttitle, name = suggestname,
                                   short_txt = suggestshort, body_txt = suggesttxt, catname = suggestcat, date = today,
                                   picname = filename, picurl = url, writer = '-',
                                   catid = 0, show = 0, time = time,)
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

    return render(request, 'back/pages/suggest_add.html')

def suggest_delete(request, pk):

    try:
        delete = Suggest.objects.get(pk=pk)
        fs = FileSystemStorage()
        fs.delete(delete.picname)
        delete.delete()
    except:
        error = "Something Wrong"
        return render(request, 'back/pages/error.html', {'error': error})


    return  redirect('suggest_list')