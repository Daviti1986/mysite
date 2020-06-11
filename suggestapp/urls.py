from django.conf.urls import include, url
from . import views



urlpatterns = [
    url(r'^suggest/(?P<word>\w.*)$', views.suggest_detail, name = 'suggest_detail'),
    url(r'^panel/suggest/list/$', views.suggest_list, name = 'suggest_list'),
    url(r'^panel/suggest/add/$', views.suggest_add, name = 'suggest_add'),
    url(r'^panel/suggest/del/(?P<pk>\d+)/$', views.suggest_delete, name = 'suggest_delete'),
    url(r'^panel/suggest/edit/(?P<pk>\d+)/$', views.suggest_edit, name = 'suggest_edit'),

]