from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, DO_NOTHING, PROTECT
# Create your models here.

    
class address(models.Model):
    user_name = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    street_address = models.CharField(max_length=2500)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    pin_code = models.IntegerField()
    phn_no = models.BigIntegerField()
    order_notes = models.CharField(max_length=2500,null=True)
    
    def __str__(self):
         return self.first_name + ' '+self.last_name+ ' '+ self.street_address + ' '+ self.city + ' '+self.state+ ' '+ str(self.pin_code)
     
 

from adminpanel.models import products
class cart(models.Model):
    user_name = models.CharField(max_length=250, blank=True,null=True)
    products_id = models.ForeignKey(products,on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    total = models.IntegerField(null=True)
    date = models.DateTimeField(null=True)
    guest_token = models.UUIDField(null=True,unique=False)

class orders(models.Model):
    user_name=models.ForeignKey(User,on_delete=models.CASCADE)
    user_address = models.ForeignKey(address,on_delete=CASCADE)
    products = models.ForeignKey(products,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.IntegerField()
    payment_method = models.CharField(max_length=100)
    date = models.DateTimeField()
    status = models.CharField(max_length=100)
    