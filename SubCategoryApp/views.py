from django.shortcuts import render, get_object_or_404, redirect
from .models import SubCategoryApp
from CategoryApp.models import CategoryApp


# Create your views here.
def sub_category_list(request):

    subcategory = SubCategoryApp.objects.all()

    return render(request, 'back/pages/sub_category.html', {'subcategory':subcategory})

def sub_category_add(request):

    categories = CategoryApp.objects.all()

    if request.method == "POST":

        name = request.POST.get('name')
        catid = request.POST.get('cat')


        if name == "":
            error = "All Fields Requirded"
            return render(request, 'back/pages/error.html', {'error': error})

        if len(SubCategoryApp.objects.filter(name=name)) != 0 :
            error = "This Name Used Before"
            return render(request, 'back/pages/error.html', {'error': error})

        catname = CategoryApp.objects.get(pk=catid).name

        data = SubCategoryApp(name = name, categoryname = catname, categoryid = catid)
        data.save()
        return redirect('sub_category_list')

    return render(request, 'back/pages/sub_category_add.html', {'categories' : categories})


