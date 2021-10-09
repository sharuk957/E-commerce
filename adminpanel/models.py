import datetime
from django.db import models
from django.contrib.auth.models import User

class offer(models.Model):
    offer_name= models.CharField(max_length=255,unique=True)
    percentage = models.PositiveIntegerField()
    expiry_date = models.DateField()
    expiry_time = models.TimeField()

class category(models.Model):
    category_name = models.CharField(max_length=100,unique=True)
    slug = models.CharField(max_length=100,unique=True)
    description = models.TextField(max_length=250)
     

class subcategory(models.Model):
    category_name = models.ForeignKey(category,on_delete=models.CASCADE)
    sub_category_name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100,unique=True)
    description = models.TextField(max_length=250)
    subcategory_offer = models.CharField(max_length=200,null=True)

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
    product_offer=models.CharField(max_length=200,null=True)
    offer_type = models.CharField(max_length=200,null=True)
    product_offer_price = models.IntegerField(null=True)

class coupon(models.Model):
    minimal_rate= models.IntegerField()
    coupon_code = models.UUIDField()
    percentage = models.PositiveIntegerField()
    expiry_date = models.DateField()
    expiry_time = models.TimeField()

    
class user_coupon(models.Model):
    user_name= models.ForeignKey(User,on_delete=models.CASCADE)
    coupon_code=models.ForeignKey(coupon,on_delete=models.CASCADE)
    status = models.CharField(max_length=100)