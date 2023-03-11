from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Book(models.Model):
    external_id = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    authors = ArrayField(models.CharField(max_length=255), blank=True, null=True) #default=[]
    published_year = models.CharField(max_length=4, null=True, blank=True)
    acquired = models.BooleanField(default=False)
    thumbnail = models.CharField(max_length=1023, blank=True, null=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return "untitled"
        
