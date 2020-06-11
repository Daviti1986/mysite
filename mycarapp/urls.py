from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^$', views.home, name = 'home' ),
    url(r'^about/$', views.about, name = 'about'),
    url(r'^panel/$', views.panel, name = 'panel'),
    url(r'^login/$', views.my_login, name = 'my_login'),
    url(r'^logout/$', views.my_logout, name = 'my_logout'),
    url(r'^panel/setting/$', views.site_setting, name = 'site_setting'),
]