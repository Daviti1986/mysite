from django.contrib.sitemaps import Sitemap
from suggestapp.models import Suggest



class MySuggestSiteMap(Sitemap):

    priority = 1.0
    chagefreq = 'daily'

    def items(self):

        return Suggest.objects.all()


    def location(self, item):
        return '/suggest/' + str (item)