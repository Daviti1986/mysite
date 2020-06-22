from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^news/add/$', views.news_letter, name = 'news_letter'),
    url(r'^panel/newsletter/emails/$', views.news_email, name = 'news_email'),
    url(r'^panel/newsletter/phones/$', views.news_phones, name = 'news_phones'),
    url(r'^panel/newsletter/delete/(?P<pk>\d+)/(?P<num>\d+)/$', views.news_txt_delete, name = 'news_txt_delete'),
]