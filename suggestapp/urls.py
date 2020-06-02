from django.conf.urls import include, url
from . import views



urlpatterns = [
    url(r'^suggest/(?P<word>\w.*)$', views.suggest_detail, name = 'suggest_detail'),
    url(r'^panel/suggest/list/$', views.suggest_list, name = 'suggest_list'),
    url(r'^panel/suggest/add/$', views.suggest_add, name = 'suggest_add'),
]