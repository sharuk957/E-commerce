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
    path('offer_management/', views.offermanagement, name='offer_management'),
    path('offer_edit/<id>', views.offer_edit, name='offer_edit'),
    path('offer_delete/<id>', views.offer_delete, name='offer_delete'),
    path('add_product_offer/', views.add_product_offer, name='add_product_offer'),
    path('add_category_offer/', views.add_category_offer, name='add_category_offer'),
    path('coupon_management/', views.couponmanagement, name='coupon_management'),
    path('coupon_edit/<id>', views.coupon_edit, name='coupon_edit'),
    path('coupon_delete/<id>', views.coupon_delete, name='coupon_delete'),
    path('check_validity/',views.check_validity, name='check_validity'),
    path('report/',views.sales_report, name='report'),
    # path('convertreport/<from_date><to_date>',views.html_to_pdf_view, name='convertreport'),
    
    
]
