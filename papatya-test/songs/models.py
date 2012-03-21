from django.db import models

# Create your models here.

class Songs(models.Model):
    name = models.CharField(max_length="50")
    album =  models.ForeignKey('Album')
    singer = models.ForeignKey('Singer')
    file_info = models.ForeignKey('FileInfo')

class Singer(models.Model):
    name = models.CharField(max_length="50")
    surname = models.CharField(max_length="100")

class Album(models.Model):
    year = models.IntegerField()
    name = models.CharField(max_length="100")
    #cover = models.ImageField()

class FileInfo(models.Model):
    extension = models.CharField(max_length="5")
    size = models.FloatField()
    length = models.FloatField()
