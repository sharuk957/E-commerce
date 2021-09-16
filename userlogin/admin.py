from django.contrib import admin
from .models import cart,address,orders
# Register your models here.
admin.site.register(cart)
admin.site.register(address)
admin.site.register(orders)