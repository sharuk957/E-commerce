from django.contrib import admin
from .models import category,subcategory,brand,products
# Register your models here.
admin.site.register(category)
admin.site.register(subcategory)
admin.site.register(brand)
admin.site.register(products)

