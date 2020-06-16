from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^panel/manager/list/$', views.manager_list, name = 'manager_list'),
    url(r'^panel/manager/delete/(?P<pk>\d+)/$', views.manager_delete, name = 'manager_delete'),
]