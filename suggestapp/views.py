from django.shortcuts import render, get_object_or_404, redirect
from .models import Suggest
from mycarapp.models import MyCar


# Create your views here.
def suggest_detail(request, word):
    site = MyCar.objects.get(pk=2)
    suggest = Suggest.objects.filter(name=word)


    return render(request, 'front/pages/suggest_detail.html', {'suggest': suggest, 'site': site })

def suggest_list(request):

    suggest = Suggest.objects.all()
    return render(request, 'back/pages/suggest_list.html', {'sugest': suggest })

def suggest_add(request):


    if request.method == 'POST':
        suggesttitle = request.POST.get('suggesttitle')
        suggestname  = request.POST.get('suggestname')
        suggestcat   = request.POST.get('suggestcat')
        suggestshort = request.POST.get('suggestshort')
        suggesttxt   = request.POST.get('suggesttxt')

        if suggesttitle == '' or suggestname == '' or suggestcat == '' or suggestshort == '' or suggesttxt == '':
            error = 'ALL Fields Requirded'
            return render(request, 'back/pages/error.html', {'error':error})
        data = Suggest(set_name = suggesttitle, name = suggestname,
                       short_txt = suggestshort, body_txt = suggesttxt, catname = suggestcat, date = '2019',
                       pic = '-', writer = '-', catid = 0, show = 0)
        data.save()
        return redirect('suggest_list')

    return render(request, 'back/pages/suggest_add.html')