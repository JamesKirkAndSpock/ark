'''Model module for phones'''
from django.db import models

# Create your models here.

class PhoneCategory(models.Model):
    '''Model table for phone categories.'''
    name = models.CharField(max_length=15, blank=False)


class Phones(models.Model):
    '''Model table for phones.'''
    phone_category = models.ForeignKey(PhoneCategory, on_delete=models.CASCADE)
    phone_name = models.CharField(max_length=15, blank=False)
    price = models.PositiveIntegerField(default=0)
    photo = models.ImageField(upload_to="phonephotos/%Y/%m/%d", default="default.jpeg")
    details = models.TextField(default="")
    front_image = models.ImageField(upload_to="phonephotos/%Y/%m/%d", default="default.jpeg")
    back_image = models.ImageField(upload_to="phonephotos/%Y/%m/%d", default="default.jpeg")
    side_image = models.ImageField(upload_to="phonephotos/%Y/%m/%d", default="default.jpeg")
