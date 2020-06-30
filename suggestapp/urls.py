from django.conf.urls import include, url
from . import views



urlpatterns = [
    url(r'^suggest/(?P<word>.*)/$', views.suggest_detail, name = 'suggest_detail'),
    url(r'^panel/suggest/list/$', views.suggest_list, name = 'suggest_list'),
    url(r'^panel/suggest/add/$', views.suggest_add, name = 'suggest_add'),
    url(r'^panel/suggest/del/(?P<pk>\d+)/$', views.suggest_delete, name = 'suggest_delete'),
    url(r'^panel/suggest/edit/(?P<pk>\d+)/$', views.suggest_edit, name = 'suggest_edit'),
    url(r'^panel/suggest/publish/(?P<pk>\d+)/$', views.suggest_publish, name = 'suggest_publish'),
    url(r'^urls/(?P<pk>\d+)$', views.suggest_detail_short, name = 'suggest_detail_short'),
    url(r'^urls/all/(?P<word>.*)$', views.suggest_all_show, name = 'suggest_all_show'),
    url(r'^all/suggest/$', views.all_suggest, name = 'all_suggest'),
    url(r'^all/suggest/search$', views.all_suggest_search, name = 'all_suggest_search'),

]