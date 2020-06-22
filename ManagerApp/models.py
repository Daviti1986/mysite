from __future__ import unicode_literals
from django.db import models

# Create your models here.

class ManagerApp(models.Model):


    name     = models.CharField(max_length= 30 )
    lastname = models.TextField()
    usertxt  = models.TextField()
    age      = models.TextField(default='')
    email    = models.TextField(default='')

    def __str__(self):
        return self.name + ' | ' + str (self.pk)


