from django.conf.urls import include, url
from . import views



urlpatterns = [
    url(r'^black/list/$', views.black_list, name = 'black_list'),
    url(r'^black/add/$', views.ip_add, name = 'ip_add'),
    url(r'^black/delete/(?P<pk>\d+)/$', views.ip_delete, name = 'ip_delete'),

]