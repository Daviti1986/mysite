"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from django.contrib.sitemaps.views import sitemap
from mycarapp.sitemap import MySuggestSiteMap
from rest_framework import routers
from mycarapp import views

router = routers.DefaultRouter()
router.register(r'mysuggest', views.SuggestViewSet)


sitemaps = {
    'suggest' : MySuggestSiteMap(),
}




urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'rest/', include(router.urls)),
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name = 'django.contrib.sitemaps.views.sitemap'),

    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    url(r'', include('mycarapp.urls')),
    url(r'', include('suggestapp.urls')),
    url(r'', include('CategoryApp.urls')),
    url(r'', include('SubCategoryApp.urls')),
    url(r'', include('ContactFormApp.urls')),
    url(r'', include('TrendingApp.urls')),
    url(r'', include('ManagerApp.urls')),
    url(r'', include('NewsLetterApp.urls')),
    url(r'', include('CommentApp.urls')),
    url(r'', include('BlackListApp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




