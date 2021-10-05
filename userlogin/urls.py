from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.userlogin, name='login'),
    path('register/', views.register, name='register'),
    path('products/', views.productview, name='product'),
    path('oneproducts/<id>', views.oneproduct, name='oneproduct'),
    path('cart/',views.cartview, name='cart'),
    path('checkout/<id>',views.checkout, name='checkout'),
    path('checkout/',views.checkout, name='checkout'),
    path('myorders/',views.my_orders, name='orders'),
    path('cancel_order/<id>',views.cancel_order, name='cancel_order'),
    path('updatecart/',views.updatecart, name='updatecart'),
    path('guestcart/',views.guestcart, name='guestcart'),
    path('guesthandler/',views.guesthandler, name='guesthandler'),
    path('logout/', views.userlogout, name='logout'),
    path('add_address/<id>',views.address_view,name='add_address'),
     path('add_address/',views.newaddress_view,name='new_address'),
    path('delete_address/<id>',views.deladdress_view,name='delete_address'),
    path('user_order/<id>',views.user_order,name='user_order'),
    path('search_products',views.search,name='search_products'),
    path('profile/', views.profile, name='profile'),
    path('edit_address/<id>',views.editaddress,name='edit_address'),
    path('edit_user/',views.edit_user,name='edit_user'),
    path('razorpayment/<id>',views.razorpayment,name='razorpayment'),
    path('profileimage/',views.profileimage,name='profileimage'),
    path('coupon_check/',views.coupon_check,name='coupon_check'),
    
    # path('contact/', views.product),
]