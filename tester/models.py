from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Feature(models.Model):
    name = models.CharField(max_length=200)
    file_path = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Scenario(models.Model):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    tag = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name