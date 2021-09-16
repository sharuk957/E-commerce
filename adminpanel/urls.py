from django.urls import path
from . import views

urlpatterns = [
    path('', views.adminlogin, name='adminlogin'),
    path('adminhome/', views.adminhome, name='adminhome'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('productlist/', views.productlist, name='productlist'),
    path('categories/', views.categories, name='categories'),
    path('subcategories/', views.subcategories, name='subcategories'),
    path('brandlist/', views.brandlist, name='brandlist'),
    path('adminlogout/', views.adminlogout, name='adminlogout'),
    path('usermanagment/', views.usermanagment, name='usermanagment'),
    path('userblock/<id>', views.userblock, name='userblock'),
    path('userunblock/<id>', views.userunblock, name='userunblock'),
    path('product_delete/<id>', views.delete_product, name='product_delete'),
    path('product_edit/<id>', views.edit_product, name='product_edit'),
    path('category_delete/<category_name>', views.delete_category, name='category_delete'),
    path('category_edit/<pk>', views.edit_category, name='category_edit'),
    path('sub_category_delete/<pk>', views.delete_subcategory, name='sub_category_delete'),
    path('sub_category_edit/<pk>', views.edit_subcategory, name='sub_category_edit'),
    path('brand_delete/<pk>', views.delete_brand, name='brand_delete'),
    path('brand_edit/<pk>', views.edit_brand, name='brand_edit'),
    path('ordermanagment/', views.ordermanagment, name='ordermanagment'),
    path('dropdownview/', views.dropdownview, name='dropdownview'),
    
    
]
