from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^comment/add/news/(?P<pk>\d+)/$', views.news_cm_add, name = 'news_cm_add'),
    url(r'^comment/list/$', views.comments_list, name = 'comments_list'),
    url(r'^comment/delete/(?P<pk>\d+)/$', views.comments_delete, name = 'comments_delete'),
    url(r'^comment/confirmed/(?P<pk>\d+)/$', views.comments_confirmed, name = 'comments_confirmed'),

]