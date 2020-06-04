from django.conf.urls import include, url
from . import views



urlpatterns = [
    url(r'^panel/category/list/$', views.Category_list, name = 'category_list'),
    url(r'^panel/category/add/$', views.Category_add, name = 'category_add'),
    url(r'^panel/category/del/(?P<pk>\d+)/$', views.category_delete, name = 'category_delete'),
]