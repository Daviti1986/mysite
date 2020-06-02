from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Suggest(models.Model):

    set_name  = models.CharField(default='-', max_length=30 )
    name      = models.CharField(max_length=30 )
    short_txt = models.TextField()
    body_txt  = models.TextField()
    date      = models.CharField(max_length=12)
    time      = models.CharField(max_length=12, default='00:00')
    picname   = models.TextField()
    picurl    = models.TextField(default = '-')
    writer    = models.CharField(max_length=50 )
    catname   = models.CharField(max_length=30, default='-')
    catid     = models.IntegerField(default=0)
    show      = models.IntegerField(default=0)

    def __str__(self):
        return self.set_name + ' | ' + str (self.pk)


