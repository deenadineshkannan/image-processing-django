from django.db import models
from datetime import datetime
# Create your models here.

class Details1(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()
    price = models.IntegerField()

class image_trial(models.Model):    
    label_name = models.CharField(max_length=25)
    image_path = models.ImageField(upload_to='images')
    image_uploaded = models.DateTimeField(default=datetime.now, blank=True)