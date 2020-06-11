from __future__ import unicode_literals
from django.db import models

# Create your models here.

class MyCar(models.Model):

    set_name = models.CharField(default='-', max_length=30 )
    name     = models.CharField(max_length=30 )
    fb       = models.CharField(default= '-', max_length=30 )
    tw       = models.CharField(default= '-', max_length=30 )
    yt       = models.CharField(default= '-', max_length=30 )
    Tell     = models.CharField(default= '-', max_length=30 )
    Link     = models.CharField(default= '-', max_length=30 )
    about    = models.TextField()

    picurl = models.TextField(default='')
    picname = models.TextField(default='')

    picurl2 = models.TextField(default='')
    picname2 = models.TextField(default='')

    def __str__(self):
        return self.set_name + ' | ' + str (self.pk)


