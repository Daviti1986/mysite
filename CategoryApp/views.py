from django.shortcuts import render, get_object_or_404, redirect
from .models import CategoryApp
import csv
from django.http import HttpResponse


# Create your views here.
def Category_list(request):

    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end
    category = CategoryApp.objects.all()

    return render(request, 'back/pages/category.html', {'category':category})

def Category_add(request):

    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    if request.method == "POST":

        name = request.POST.get('name')

        if name == "":
            error = "All Fields Requirded"
            return render(request, 'back/pages/error.html', {'error': error})

        if len(CategoryApp.objects.filter(name=name)) != 0 :
            error = "This Name Used Before"
            return render(request, 'back/pages/error.html', {'error': error})

        data = CategoryApp(name=name)
        data.save()
        return redirect('category_list')

    return render(request, 'back/pages/category_add.html')

def category_delete(request, pk):


    # login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    # login check end

    try:
        delete = CategoryApp.objects.get(pk=pk)
        delete.delete()
    except:
        error = "Something Wrong"
        return render(request, 'back/pages/error.html', {'error': error})


    return  redirect('category_list')


def export_category_csv(request):

    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename="category.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Counter'])
    for i in CategoryApp.objects.all():
        writer.writerow([i.name, i.count])

    return response
def import_category_csv(request):
    if request.method == 'POST' :
        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            error = "Please Input Csv File"
            return render(request, 'back/pages/error.html', {'error': error})
        if csv_file.multiple_chunks():
            error = "File Too large"
            return render(request, 'back/pages/error.html', {'error': error})

        file_data = csv_file.read().decode('utf-8')
        lines = file_data.split('\n')

        for line in lines :
            fields = line.split(',')
            try:

                if len(CategoryApp.objects.filter(name=fields[0])) == 0 and fields[0] != 'Title' and fields[0] != '':
                    data = CategoryApp(name=fields[0])
                    data.save()

            except:
                print('finish')

    return redirect('category_list')

