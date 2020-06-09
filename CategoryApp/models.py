from __future__ import unicode_literals
from django.db import models

# Create your models here.

class CategoryApp(models.Model):


    name      = models.CharField(max_length=30 )
    count     = models.IntegerField(default=0)
    def __str__(self):
        return self.name + ' | ' + str (self.pk)


