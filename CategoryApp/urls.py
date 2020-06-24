from django.conf.urls import include, url
from . import views



urlpatterns = [
    url(r'^panel/category/list/$', views.Category_list, name = 'category_list'),
    url(r'^panel/category/add/$', views.Category_add, name = 'category_add'),
    url(r'^panel/category/del/(?P<pk>\d+)/$', views.category_delete, name = 'category_delete'),
    url(r'^export/category/csv/$', views.export_category_csv, name = 'export_category_csv'),
    url(r'^import/category/csv/$', views.import_category_csv, name = 'import_category_csv'),
]