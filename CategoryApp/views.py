from django.shortcuts import render, get_object_or_404, redirect
from .models import CategoryApp


# Create your views here.
def Category_list(request):

    category = CategoryApp.objects.all()

    return render(request, 'back/pages/category.html', {'category':category})

def Category_add(request):

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

    try:
        delete = CategoryApp.objects.get(pk=pk)
        delete.delete()
    except:
        error = "Something Wrong"
        return render(request, 'back/pages/error.html', {'error': error})


    return  redirect('category_list')

