from __future__ import unicode_literals

from django.db import models

# Create your models here.

class HostGroup(models.Model):
    name = models.CharField(max_length=50)

class Host(models.Model):
    ip = models.GenericIPAddressField()
    group = models.ForeignKey('HostGroup')