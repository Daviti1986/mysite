from __future__ import unicode_literals
from django.db import models

# Create your models here.

class SubCategoryApp(models.Model):


    name         = models.CharField(max_length=30 )
    categoryname = models.CharField(max_length=30)
    categoryid   = models.IntegerField()

    def __str__(self):
        return self.name + ' | ' + str (self.pk)



