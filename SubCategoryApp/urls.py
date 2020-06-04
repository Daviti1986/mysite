from django.conf.urls import include, url
from . import views



urlpatterns = [
    url(r'^panel/subcategory/list/$', views.sub_category_list, name = 'sub_category_list'),
    url(r'^panel/subcategory/add/$', views.sub_category_add, name = 'sub_category_add'),

]