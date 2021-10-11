from django.contrib import admin
from .models import cart,address,orders, userimage
# Register your models here.
admin.site.register(cart)
admin.site.register(address)
admin.site.register(orders)
admin.site.register(userimage)