from __future__ import unicode_literals
from django.db import models

# Create your models here.

class ManagerApp(models.Model):


    name     = models.CharField(max_length= 30, default= '' )
    lastname = models.CharField(max_length= 30, default= '' )
    usertxt  = models.CharField(max_length= 30, default= '' )
    age      = models.CharField(max_length= 30, default= '' )
    email    = models.CharField(max_length= 30, default= '' )

    def __str__(self):
        return self.name + ' | ' + str (self.pk)


