from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.userlogin, name='login'),
    path('register/', views.register, name='register'),
    path('products/', views.productview, name='product'),
    path('oneproducts/<id>', views.oneproduct, name='oneproduct'),
    path('cart/',views.cartview, name='cart'),
    path('checkout/',views.checkout, name='checkout'),
    path('myorders/',views.my_orders, name='orders'),
    path('updatecart/',views.updatecart, name='updatecart'),
    path('guestcart/',views.guestcart, name='guestcart'),
    path('guesthandler/',views.guesthandler, name='guesthandler'),
    path('logout/', views.userlogout, name='logout'),
    path('add_address/',views.address_view,name='add_address'),
    path('delete_address/<id>',views.deladdress_view,name='delete_address'),
    path('user_order/',views.user_order,name='user_order'),
    # path('contact/', views.product),
]