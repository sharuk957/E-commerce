import json
from json.encoder import JSONEncoder
from django.contrib import auth
from django.db.models.aggregates import Count
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import AnonymousUser, User
from adminpanel.models import products
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import datetime
import uuid
from .models import cart,address,orders
# Create your views here.
# def login(request):
#     return render(request,'login-register.html')


def home(request):
    product = products.objects.all()
    # print(product.sub_category.pk)
    return render(request, 'index.html', {'products': product})

# def product(request):
#     return render(request,'adminlogin.html')


def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('user-name')
        password = request.POST.get('user-password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['logged_in'] = True
            print(request.session['logged_in'])
            if request.session.has_key('guest'):
                return redirect(guesthandler)
            else:
                return redirect('home')
        else:
            messages.error(request, "invalid user name or password")
            return redirect('login')
    else:
        if request.session.has_key('logged_in'):
            return redirect('home')
        else:
            return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        firstname = request.POST['user-firstname']
        lastname = request.POST['user-lastname']
        username = request.POST['user-name']
        password = request.POST['user-password']
        confirmpassword = request.POST['confirm-password']
        email = request.POST['user-email']

        if password == confirmpassword:
            if User.objects.filter(username=username):
                messages.error(request, "username already exist")
                return redirect(register)
            elif User.objects.filter(email=email):
                messages.error(request, "email already exist")
                return redirect(register)
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password, first_name=firstname, last_name=lastname)
                user.save()
                messages.success(request, "user succesfully created")
                return redirect('login')
        else:
            return redirect(register)
    else:
        print(request.session.has_key('logged_in'))
        if request.session.has_key('logged_in'):
            return redirect('home')
        else:
            return render(request, 'register.html')


def userlogout(request):
    if request.session.has_key('logged_in'):
        del request.session['logged_in']
        logout(request)
        return redirect(home)
    else:
        return redirect(home)


def productview(request):
    data = products.objects.all()
    return render(request, 'products.html', {'products': data})


def oneproduct(request, id):
    data = products.objects.get(id=id)
    return render(request, 'oneproduct.html', {'product': data})


def cartview(request):
    print("hai")
    print(request.session.has_key('logged_in'))
    if request.session.has_key('logged_in'):
        data = cart.objects.filter(user_name=request.user)
        sum=0
        price=0
        print("hellooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
        print(data)
        for cart1 in data:
            sum+=cart1.quantity
            price+=cart1.total
        return render(request, 'cart.html',{'cart':data, 'totalprice':price,'totalproduct':sum})
    else:
        if request.session.has_key('guest'):
            print("hiiiii")
            data = cart.objects.filter(guest_token=request.session['guest'])
            
            price=0
            sum=0
            print(data)
            for cart1 in data:
                print("hi")
                print(cart1)
                sum+=cart1.quantity
                print(sum)
                price+=cart1.total
                print(price)
            return render(request, 'cart.html',{'cart':data, 'totalprice':price,'totalproduct':sum})
        else:
            return render(request, 'cart.html')

def checkout(request):
    if request.session.has_key('logged_in'):
        if cart.objects.filter(user_name=request.user):
            user_id=User.objects.get(username=request.user)
            address_data=address.objects.filter(user_name=user_id)
            cart_data = cart.objects.filter(user_name=request.user)
            return render(request,'withlogincheckout.html',{'address_data':address_data
                                                            })
        else:
            return redirect(cartview)
    else:
        return render(request,'withoutlogincheckout.html')
        
def my_orders(request):
    
    order_list=orders.objects.filter(user_name=User.objects.get(username=request.user))
    print(order_list)
    return render(request,'orders.html',{'order_list':order_list})


def updatecart(request):
    data=json.loads(request.body)
    id = data['productid']
    username = request.user
    print(username.id)
    action = data['action']
    
    product = products.objects.get(pk=id)
    userdeatails = username
    
    if cart.objects.filter(user_name=userdeatails,products_id=product):
        cartdeatail=cart.objects.get(user_name=userdeatails,products_id=product)
        if action =="delete":
            cartdeatail.delete()
        else:
            if action == "add":
                cartdeatail.quantity = (cartdeatail.quantity + 1)
            elif action == 'remove':
                if cartdeatail.quantity <=0:
                    cartdeatail.quantity =1
                else:
                    cartdeatail.quantity = (cartdeatail.quantity - 1)
            cartdeatail.total = ((cartdeatail.products_id.price)*(cartdeatail.quantity))
            cartdeatail.date = datetime.datetime.now()
            cartdeatail.save()
    else:
        quantity = 1
        total = product.price
        cartdeatail= cart.objects.create(user_name=userdeatails,products_id=product,quantity=quantity,total=total,date=datetime.datetime.now())
    return JsonResponse("success", safe=False)


def guestcart(request):
    data=json.loads(request.body)
    id = data['productid']
    action = data['action']
    product = products.objects.get(pk=id)
    if request.session.has_key('guest') and cart.objects.filter(guest_token=request.session['guest'],products_id=product):
        print("hai")
        cartdeatail=cart.objects.get(guest_token=request.session['guest'],products_id=product)
        if action =="delete":
            cartdeatail.delete()
        else:
            if action == "add":
                cartdeatail.quantity = (cartdeatail.quantity + 1)
            elif action == 'remove':
                if cartdeatail.quantity <2:
                    cartdeatail.quantity =1
                else:
                    cartdeatail.quantity = (cartdeatail.quantity - 1)
            cartdeatail.total = ((cartdeatail.products_id.price)*(cartdeatail.quantity))
            cartdeatail.date = datetime.datetime.now()
            cartdeatail.save()
    else:
        if request.session.has_key('guest'):
            guest_user=request.session['guest']
        else:
            guest_user = str(uuid.uuid4())
            request.session['guest']=guest_user
            print(request.session['guest'])
        quantity = 1
        print(product.price)
        total = product.price
        cartdeatail= cart.objects.create(guest_token=guest_user,products_id=product,quantity=quantity,total=total,date=datetime.datetime.now())
    return JsonResponse("success", safe=False)

def guesthandler(request):
    if request.session.has_key('guest'):
        data = cart.objects.filter(guest_token=request.session['guest'])
        print(data.values())
        username=User.objects.get(username=request.user)
        for guestuser in data:
            print(request.user)
            product = products.objects.get(pk=guestuser.products_id_id)
            if cart.objects.filter(user_name=username,products_id=product.id):
                data1=cart.objects.get(user_name=username,products_id=product.id)
                data1.quantity=data1.quantity+guestuser.quantity
                data1.total=data1.total + guestuser.total
                data1.save()
                guestuser.delete()
            else:
                guestuser.user_name=username.username
                guestuser.save()
                print(guestuser.user_name)
        del request.session['guest']
        return redirect(home)
    else:
        return redirect(home)
    
def address_view(request):
    if request.method == 'POST':
        user_name=User.objects.get(username=request.user)
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        country=request.POST['place']
        city=request.POST['city']
        street_address=request.POST['house'] + request.POST['apartment']
        state=request.POST['state']
        pin_code=request.POST['pin_code']
        phn_number=request.POST['phn_no']
        order_notes=request.POST['message']
        address.objects.create(user_name=user_name,first_name=first_name,last_name=last_name,country=country,city=city,
                                         street_address=street_address,state=state,pin_code=pin_code,phn_no=phn_number,order_notes=order_notes)
        return redirect(checkout)
    else:
        return render(request,'address.html')
    
def deladdress_view(request,id):
    if address.objects.filter(id=id):
        data=address.objects.get(id=id)
        data.delete()
        return redirect(checkout)
    else:
        orders.objects.all()
        return redirect(home)

def user_order(request):
    if request.method == 'POST':
        cart_data = cart.objects.filter(user_name=request.user)
        for each_product in cart_data:
            user_data=User.objects.get(username=request.user)
            print(each_product.products_id.id)
            product_id=each_product.products_id.id
            quantity = each_product.quantity
            total = each_product.total
            address_id = request.POST['address']
            payment = request.POST['payment_method']
            date = datetime.datetime.now()
            orders.objects.create(user_name=user_data,user_address=address.objects.get(id=address_id),products_id=product_id,quantity=quantity,total=total,payment_method=payment,date=date,status="ordered")
        cart_data.delete()
        return render(request,"succes.html")
    else:
        return redirect(checkout)