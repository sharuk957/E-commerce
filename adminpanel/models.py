import datetime
from django.db import models
from django.contrib.auth.models import User


class category(models.Model):
    category_name = models.CharField(max_length=100,unique=True)
    slug = models.CharField(max_length=100,unique=True)
    description = models.TextField(max_length=250)
     

class subcategory(models.Model):
    category_name = models.ForeignKey(category,on_delete=models.CASCADE)
    sub_category_name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100,unique=True)
    description = models.TextField(max_length=250)

class brand(models.Model):
    category_name = models.ForeignKey(category,on_delete=models.CASCADE)
    sub_category_name = models.ForeignKey(subcategory,on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100,unique=True)

class products(models.Model):
    product_name = models.CharField(max_length=250, unique=True)
    description = models.TextField(max_length=500)
    image1 = models.ImageField(upload_to='pics')
    image2 = models.ImageField(upload_to='pics')
    image3 = models.ImageField(upload_to='pics')
    image4 = models.ImageField(upload_to='pics')
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(subcategory, on_delete=models.CASCADE)
    price = models.IntegerField()
    unit = models.IntegerField()
    brand = models.ForeignKey(brand, on_delete=models.CASCADE)
    date = models.DateTimeField()




