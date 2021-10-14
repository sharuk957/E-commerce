import json
from json.encoder import JSONEncoder
from django.contrib import auth
from django.db.models.aggregates import Count
from django.db.models.query_utils import Q
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from adminpanel.models import products,coupon,user_coupon
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import datetime
import uuid
from .models import cart,address,orders,userimage,wishlist
from django.db.models import Q
from  django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
import base64
from django.core.files.base import ContentFile

from .twilio import send_sms

def home(request):
    product = products.objects.all()
    wish_count = wishlist_count(request)
    count= cart_count(request)
    return render(request, 'user/index.html', {'products': product,'count':count,'wish_count':wish_count})



def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('user-name')
        password = request.POST.get('user-password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['logged_in'] = True
            if request.session.has_key('guest'):
                return redirect(guesthandler)
            if request.session.has_key('guest_wish'):
                return redirect(wishlist_handler)
            return redirect(home)
        else:
            messages.error(request, "invalid user name or password")
            return redirect('login')
    else:
        wish_count = wishlist_count(request)
        if request.session.has_key('logged_in'):
            return redirect('home')
        else:
            count= cart_count(request)
            return render(request, 'user/login.html',{'count':count,'wish_count':wish_count})


def register(request):
    if request.method == 'POST':
        firstname = request.POST['user-firstname']
        lastname = request.POST['user-lastname']
        username = request.POST['user-name']
        password = request.POST['user-password']
        confirmpassword = request.POST['confirm-password']
        email = request.POST['user-email']
        referral = request.POST['user-referral']
        if password == confirmpassword:
            if User.objects.filter(username=username):
                messages.error(request, "username already exist")
                return redirect(register)
            elif User.objects.filter(email=email):
                messages.error(request, "email already exist")
                return redirect(register)
            else:
                if referral:
                    if userimage.objects.filter(referral_code=referral):
                        pass
                    else:
                        messages.error(request, "invalid refferal code")
                        return redirect(register)
                user = User.objects.create_user(
                    username=username, email=email, password=password, first_name=firstname, last_name=lastname)
                user.save()
                referral_code = user.first_name + str(user.id)
                if referral:
                    referred_user = userimage.objects.get(referral_code=referral)
                    referred_user.wallet_cash+=50
                    referred_user.save()
                    cash = 20  
                else:
                    cash = 0
                userimage.objects.create(user_name=user,referral_code=referral_code,wallet_cash=cash)
                messages.success(request, "user successfully created")
                return redirect('login')
        else:
            return redirect(register)
    else:
        wish_count = wishlist_count(request)
        count= cart_count(request)
        return render(request, 'user/register.html',{'count':count,'wish_count':wish_count})



@login_required(login_url='login')
def userlogout(request):
    if request.session.has_key('logged_in'):
        del request.session['logged_in']
        logout(request)
        return redirect(home)
    else:
        return redirect(home)



def productview(request):
    data = products.objects.all().order_by("id")
    popular = orders.objects.all().values('products').annotate(total=Count('products')).order_by('-total').first
    wish_count = wishlist_count(request)
    count= cart_count(request)
    return render(request, 'user/products.html', {'products': data,'count':count,'popular':popular,'wish_count':wish_count})


def oneproduct(request, id):
    data = products.objects.get(id=id)
    wish_count = wishlist_count(request)
    count= cart_count(request)
    return render(request, 'user/oneproduct.html', {'product': data,'count':count,'wish_count':wish_count})


def cartview(request):
    sum=0
    price=0
    count=0
    wish_count = wishlist_count(request)
    if request.session.has_key('logged_in'):
        data = cart.objects.filter(user_name=request.user).order_by("-id")
        
        for cart1 in data:
            sum+=cart1.quantity
            price+=cart1.total
            count+=1
        return render(request, 'user/cart.html',{'cart':data, 'totalprice':price,'totalproduct':sum,'count':count,'wish_count':wish_count})
    else:
        if request.session.has_key('guest'):
            data = cart.objects.filter(guest_token=request.session['guest']).order_by("-id")
            for cart1 in data:
                sum+=cart1.quantity
                price+=cart1.total
                count+=1
            return render(request, 'user/cart.html',{'cart':data, 'totalprice':price,'totalproduct':sum,'count':count,'wish_count':wish_count})
        else:
            return render(request, 'user/cart.html',{'count':count,'wish_count':wish_count})
        



@login_required(login_url='login')
def checkout(request,id=-1):
    if request.session.has_key('logged_in'):
        count = cart.objects.filter(user_name=request.user).count()
        user_id=User.objects.get(username=request.user)
        address_data=address.objects.filter(user_name=user_id)
        wish_count = wishlist_count(request)
        if id == '-1' :
            cart_data=cart.objects.filter(user_name=request.user)
            if cart_data:
                total=0
                for cart_one in cart_data:
                    total +=cart_one.total
                new_total = total
                coupon_offers = user_coupon.objects.filter(user_name=request.user,status=False)
                if coupon_offers:
                    if coupon_offers.count() > 1:
                        coupon_offers=coupon_offers.last()
                    else:
                        coupon_offers=coupon_offers.first()
                    total = total - coupon_offers.coupon_code.percentage
                else:
                    total = total
                return render(request,'user/withlogincheckout.html',{'address_data':address_data,'cart_data':cart_data,'count':count,'product':-1,'total':total,'new':new_total,'wish_count':wish_count,'coupon':coupon_offers})
            else:
                return redirect(cartview)
            
        else:
            product=products.objects.get(id=id)
            if product.product_offer:
                total=product.product_offer_price
            else:
                total=product.price
            new_total = total
            coupon_offers = user_coupon.objects.filter(user_name=request.user,status=False)
            if coupon_offers:
                if coupon_offers.count() > 1:
                    coupon_offers=coupon_offers.last()
                else:
                    coupon_offers=coupon_offers.first()
                    total = total - coupon_offers.coupon_code.percentage
            else:
                total = total
            return render(request,'user/withlogincheckout.html',{'address_data':address_data,'count':count,'product_data':product,'product':product.id,'new':new_total,'total':total,'wish_count':wish_count,'coupon':coupon_offers})
    else:
        return redirect(userlogin)
  
  
  
@login_required(login_url='login')      
def my_orders(request): 
    order_list=orders.objects.filter(user_name=User.objects.get(username=request.user)).order_by("date")
    wish_count = wishlist_count(request)
    count= cart_count(request)
    return render(request,'user/orders.html',{'order_list':order_list,'count':count,'wish_count':wish_count})


@login_required(login_url='login')
def cancel_order(request,id):
    order_deatail = orders.objects.get(id=id)
    order_deatail.status = 'Cancelled'
    order_deatail.save()
    return redirect(my_orders)


def updatecart(request):
    data=json.loads(request.body)
    id = data['productid']
    username = request.user
    action = data['action']
    
    product = products.objects.get(pk=id)
    userdeatails = username
    
    if cart.objects.filter(user_name=userdeatails,products_id=product):
        cartdeatail=cart.objects.get(user_name=userdeatails,products_id=product)
        if action =="delete":
            cartdeatail.delete()
        else:
            if action == "add":
                if cartdeatail.quantity < product.unit:
                    cartdeatail.quantity = (cartdeatail.quantity + 1)
                else:
                    messages.error(request, "reach maximum availability")
                    cartdeatail.quantity=cartdeatail.quantity
            elif action == 'remove':
                if cartdeatail.quantity <=1:
                    cartdeatail.quantity =1
                else:
                    cartdeatail.quantity = (cartdeatail.quantity - 1)
            if cartdeatail.products_id.product_offer:
                cartdeatail.total = ((cartdeatail.products_id.product_offer_price)*(cartdeatail.quantity))
            else:
                cartdeatail.total = ((cartdeatail.products_id.price)*(cartdeatail.quantity))
            cartdeatail.date = datetime.datetime.now()
            cartdeatail.save()
    else:
        quantity = 1
        if product.product_offer:
            total = product.product_offer_price
        else:
            total = product.price
        cartdeatail= cart.objects.create(user_name=userdeatails,products_id=product,quantity=quantity,total=total,date=datetime.datetime.now())
    return JsonResponse('success', safe=False)


def guestcart(request):
    data=json.loads(request.body)
    id = data['productid']
    action = data['action']
    product = products.objects.get(pk=id)
    if request.session.has_key('guest') and cart.objects.filter(guest_token=request.session['guest'],products_id=product):
        cartdeatail=cart.objects.get(guest_token=request.session['guest'],products_id=product)
        if action =="delete":
            cartdeatail.delete()
        else:
            if action == "add":
                if cartdeatail.quantity < product.unit:
                    cartdeatail.quantity = (cartdeatail.quantity + 1)
                else:
                    messages.error(request, "reach maximum availability")
                    cartdeatail.quantity=cartdeatail.quantity
            elif action == 'remove':
                if cartdeatail.quantity <1:
                    cartdeatail.quantity =1
                else:
                    cartdeatail.quantity = (cartdeatail.quantity - 1)
            if cartdeatail.products_id.product_offer:
                cartdeatail.total = ((cartdeatail.products_id.product_offer_price)*(cartdeatail.quantity))
            else:
                cartdeatail.total = ((cartdeatail.products_id.price)*(cartdeatail.quantity))
            cartdeatail.date = datetime.datetime.now()
            cartdeatail.save()
    else:
        if request.session.has_key('guest'):
            guest_user=request.session['guest']
        else:
            guest_user = str(uuid.uuid4())
            request.session['guest']=guest_user
        quantity = 1
        if product.product_offer:
            total = product.product_offer_price
        else:
            total = product.price
        cartdeatail= cart.objects.create(guest_token=guest_user,products_id=product, quantity=quantity,total=total,date=datetime.datetime.now())
    return JsonResponse("success", safe=False)


@login_required(login_url='login')
def guesthandler(request):
    if request.session.has_key('guest'):
        data = cart.objects.filter(guest_token=request.session['guest'])
        username=User.objects.get(username=request.user)
        for guestuser in data:
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
        del request.session['guest']
        if request.session.has_key('guest_wish'):
            return redirect(wishlist_handler)
        else:
            return redirect(home)
    else:
        if request.session.has_key('guest_wish'):
            return redirect(wishlist_handler)
        else:
            return redirect(home)


def cart_count(request):
    if request.session.has_key('logged_in'):
        count=cart.objects.filter(user_name=request.user).count()
    else:
        if request.session.has_key('guest'):
            count=cart.objects.filter(guest_token=request.session.get('guest')).count()
        else:
            count=0
    return count
    
    
@login_required(login_url='login')   
def address_view(request,id=-1):
    address_limit = address.objects.filter(user_name=request.user).count()
    if address_limit >= 4 :
        data=address.objects.filter(user_name=request.user).order_by().first()
        data.delete()
    if request.method == 'POST':
        user_name=User.objects.get(username=request.user)
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        country=request.POST['place']
        city=request.POST['city']
        street_address=request.POST['house'] +', '+ request.POST['apartment']
        state=request.POST['state']
        pin_code=request.POST['pin_code']
        phn_number=request.POST['phn_no']
        order_notes=request.POST['message']
        address.objects.create(user_name=user_name,first_name=first_name,last_name=last_name,country=country,city=city,
                                         street_address=street_address,state=state,pin_code=pin_code,phn_no=phn_number,order_notes=order_notes)
        return redirect(checkout,id)
    else:
        wish_count = wishlist_count(request)
        count= cart_count(request)
        return render(request,'user/address.html',{'count':count,'product':id,'wish_count':wish_count})


@login_required(login_url='login')  
def deladdress_view(request,id):
    if address.objects.filter(id=id):
        data=address.objects.get(id=id)
        data.delete()
        return redirect(profile)
    else:
        orders.objects.all()
        return redirect(home)



@login_required(login_url='login')
def user_order(request,id=-1):
    if request.method == 'POST':
        user_data=User.objects.get(username=request.user)
        address_id = request.POST.get('address')
        payment = request.POST.get('payment_method')
        user_address=str(address.objects.get(id=address_id))
        date = datetime.datetime.now()
        if id == '-1':
            cart_data = cart.objects.filter(user_name=request.user)
            sub_total=0
            coupon_code = request.POST.get('offer_code')
            for each_product in cart_data:
                product_id=each_product.products_id.id
                quantity = each_product.quantity
                total = each_product.total
                product=products.objects.get(id=product_id)
                product.unit-=quantity
                sub_total += total
                if coupon_code:
                    try:
                        if coupon.objects.filter(coupon_code=coupon_code):
                            coupons = coupon.objects.get(coupon_code=coupon_code)
                            user_coupons = user_coupon.objects.filter(coupon_code=coupons,user_name=user_data,status=True)
                            if user_coupons:
                                total=total
                            else:
                                if sub_total<coupons.minimal_rate:
                                    total=total
                                else:
                                    if total>coupons.percentage:
                                        total = total - coupons.percentage
                                        offers=user_coupon.objects.get(coupon_code=coupons,user_name=user_data,status=False)
                                        offers.status=True
                                        offers.save()
                                    else:
                                        coupons.percentage -=total
                                        total=0
                    except:
                        total = total
                else:
                    total = total
                product.save()
                orders.objects.create(user_name=user_data,user_address=user_address,products_id=product_id, quantity=quantity,total=total,payment_method=payment,date=date,status="ordered")
            
            cart_data.delete()
        else:
            product=products.objects.get(id=id)
            coupon_code = request.POST.get('offer_code')
            product_id=id
            quantity=1
            if product.product_offer:
                total = product.product_offer_price
            else:
                total = product.price
            if coupon_code:
                try:
                    if coupon.objects.filter(coupon_code=coupon_code):
                        coupons = coupon.objects.get(coupon_code=coupon_code)
                        user_coupons = user_coupon.objects.filter(coupon_code=coupons,user_name=user_data,status=True)
                        if user_coupons:
                            total=total
                        else:
                            if total<coupons.minimal_rate:
                                total=total
                            else:
                                total = total - coupons.percentage
                                offers=user_coupon.objects.get(coupon_code=coupons,user_name=user_data,status=False)
                                offers.status=True
                                offers.save()
                    
                except:
                    total = total
            else:
                total = total
            product.unit-=1
            orders.objects.create(user_name=user_data,user_address=user_address,products_id=product_id, quantity=quantity,total=total,payment_method=payment,date=date,status="ordered")
        return render(request,"user/succes.html")
    else:
        return redirect(checkout,id)
    
    


def search(request):
    search_query=request.GET['search']
    data = products.objects.filter(Q(product_name__icontains=search_query)).order_by("id")
    wish_count = wishlist_count(request)
    count= cart_count(request)
    return render(request, 'user/products.html', {'products': data,'count':count,'wish_count':wish_count})


def profile(request):
    wish_count = wishlist_count(request)
    count= cart_count(request)
    user_detail=User.objects.get(username=request.user)
    user_address=address.objects.filter(user_name=request.user)
    user_image=userimage.objects.filter(user_name=user_detail).first()
    return render(request, 'user/profile.html',{'user_detail':user_detail,'count':count,'user_address':user_address,'user_image':user_image,'wish_count':wish_count})

@login_required(login_url='login')  
def editaddress(request,id):
    if address.objects.filter(id=id):
        data=address.objects.get(id=id)
        if request.method == 'POST':
            data.user_name=User.objects.get(username=request.user)
            data.first_name=request.POST['first_name']
            data.last_name=request.POST['last_name']
            data.country=request.POST['place']
            data.city=request.POST['city']
            data.street_address=request.POST['house'] +', '+ request.POST['apartment']
            data.state=request.POST['state']
            data.pin_code=request.POST['pin_code']
            data.phn_number=request.POST['phn_no']
            data.order_notes=request.POST['message']
            data.save()
            return redirect(profile)
        else:
            address_detail=address.objects.get(id=id)
            
            street_detail=address_detail.street_address.split(", ")
            
            return render(request, 'user/editaddress.html',{'address':address_detail,'street':street_detail[0],'apartment':street_detail[1]})
    else:
        # orders.objects.all()
        return redirect(home)
    

@login_required(login_url='login')   
def newaddress_view(request):
    address_limit = address.objects.filter(user_name=request.user).count()
    if address_limit >= 4 :
        data=address.objects.filter(user_name=request.user).order_by().first()
        data.delete()
        
    if request.method == 'POST':
        user_name=User.objects.get(username=request.user)
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        country=request.POST['place']
        city=request.POST['city']
        street_address=request.POST['house'] +', '+ request.POST['apartment']
        state=request.POST['state']
        pin_code=request.POST['pin_code']
        phn_number=request.POST['phn_no']
        order_notes=request.POST['message']
        address.objects.create(user_name=user_name,first_name=first_name,last_name=last_name,country=country,city=city,
                                         street_address=street_address,state=state,pin_code=pin_code,phn_no=phn_number,order_notes=order_notes)
        return redirect(profile)
    else:
        wish_count = wishlist_count(request)
        count= cart_count(request)
        return render(request,'user/newaddress.html',{'count':count,'wish_count':wish_count})

def edit_user(request):
    if request.method == 'POST':
        user_detail=User.objects.get(username=request.user)
        check=request.POST['change']
        user_detail.first_name=request.POST['f-name']
        user_detail.last_name=request.POST['l-name']
        user_detail.email=request.POST['e-mail']
        currentpass=request.POST['currentpass']
        newpass=request.POST['newpass']
        confpass=request.POST['confpass']
        mobile_num = request.POST.get('number')
        additional_details = userimage.objects.filter(mobile_num=mobile_num).first()
        if mobile_num!=additional_details.mobile_num:
            if additional_details:
                messages.error(request,"mobile number already exist")
            else:
                user_add = userimage.objects.filter(user_name=request.user).first()
                if user_add:
                    user_add.mobile_num=mobile_num
                    user_add.save()
                else:
                    userimage.objects.create(user_name=request.user,mobile_num=mobile_num,referral_code=request.user.username+" "+str(request.user.id),wallet_cash=0)
        if check == '1' :
            if check_password(currentpass,user_detail.password) :
                if confpass == newpass:
                    user_detail.set_password(newpass)
                    user_detail.save()
                    update_session_auth_hash(request, user_detail)
                else:
                    messages.error(request,"passwords doesn't match")
            else:
                messages.error(request,"passwords doesn't match") 
        else:
            user_detail.save()
    return redirect(profile)


    
def profileimage(request):
    if request.method == "POST":
        data=json.loads(request.body)
        image = data['profileimage']
        format, img1 = image.split(';base64,')
        ext = format.split('/')[-1]
        profile_image = ContentFile(base64.b64decode(img1), name= request.user.username + '1.' + ext)
        username = User.objects.get(username=request.user)
        if userimage.objects.filter(user_name=username):
            userimage_details = userimage.objects.get(user_name=username)
            userimage_details.profileimage = profile_image
            userimage_details.save()
        else:
            userimage.objects.create(user_name=username,profileimage=profileimage,wallet_cash=0)
    return JsonResponse('success',safe=False)


import razorpay

def razorpayment(request,id=-1):
    if id == '-1':
        cart_data = cart.objects.filter(user_name=request.user)
        for each_product in cart_data:
            total = each_product.total
        coupon_offers = user_coupon.objects.filter(user_name=request.user,status=False)
        if coupon_offers:
            if coupon_offers.count() > 1:
                coupon_offers=coupon_offers.last()
            else:
                coupon_offers=coupon_offers.first()
            total = total - coupon_offers.coupon_code.percentage
        else:
            total = total
        
    else:
        product=products.objects.get(id=id)
        if product.product_offer:
            total = product.product_offer_price
        else:
            total = product.price
        coupon_offers = user_coupon.objects.filter(user_name=request.user,status=False)
        if coupon_offers:
            if coupon_offers.count() > 1:
                coupon_offers=coupon_offers.last()
            else:
                coupon_offers=coupon_offers.first()
            total = total - coupon_offers.coupon_code.percentage
        else:
            total = total
    client = razorpay.Client(auth=("rzp_test_g8LOYD78mSH0b6", "QA95rexPt8ZJiMMrBj6alkqc"))
    order_amount = total*100
    
    order_currency = 'INR'

    payment=client.order.create(dict(amount=order_amount, currency=order_currency,payment_capture='1'))
    return JsonResponse(payment,safe=False)



def coupon_check(request):
    data=json.loads(request.body)
    if request.method == 'POST':
        code = data['coupon_code']
        total= data['total']
        try:
            if coupon.objects.filter(coupon_code=code):

                coupons = coupon.objects.get(coupon_code=code)
               
                user_coupons = user_coupon.objects.filter(user_name=request.user,coupon_code=coupons)
                if user_coupons:
                    
                    message = "coupon already used"
                    success = False
                else:
                    
                    if total<coupons.minimal_rate:
                        
                        message = "Coupon is not available"
                        success = False
                    else:
                        
                        new_total = total - coupons.percentage
                        message=new_total
                        success=True
                        user_coupon.objects.create(user_name=request.user,coupon_code=coupons,status=False)
            else:
                
                message = "coupon already used"
                success = False
        except:
            
            message = "Coupon is not available"
            success = False
        return JsonResponse({'value':message,'success':success},safe=False)   
    else:
        return JsonResponse('unsuccess',safe=False)
    
#wishlist.............................................
def wishlist_view(request):
    cart_counts= cart_count(request)
    if request.session.has_key('logged_in'):
        data = wishlist.objects.filter(user_name=request.user).order_by("-id")
        count = data.count()
        return render(request,'user/wishlist.html',{'wishlists':data,'wish_count':count,'count':cart_counts})
    else:
        if request.session.has_key('guest_wish'):
            data = wishlist.objects.filter(guest_token=request.session['guest_wish']).order_by("-id")
            count = data.count()
            return render(request, 'user/wishlist.html',{'wishlists':data,'wish_count':count,'count':cart_counts})
        else:
            count=0
            return render(request, 'user/wishlist.html',{'wish_count':count,'count':cart_counts})

def add_wishlist(request):
    data=json.loads(request.body)
    id = data['productid']
    username = request.user
    product = products.objects.get(pk=id)
    userdeatails = username
    if wishlist.objects.filter(user_name=userdeatails,products_id=product):
        messages.error(request, "item already in your wishlist")
    else:
        wishlist.objects.create(user_name=userdeatails,products_id=product)
    return JsonResponse('success', safe=False)


def remove_wishlist(request):
    data=json.loads(request.body)
    id = data['productid']
    username = request.user
    product = products.objects.get(pk=id)
    userdeatails = username
    wishlist_details=wishlist.objects.filter(user_name=userdeatails,products_id=product)
    if wishlist_details:
        wishlist_details.delete()
    return JsonResponse('success', safe=False)

def add_guest_wishlist(request):
    data=json.loads(request.body)
    id = data['productid']
    product = products.objects.get(pk=id)
    if request.session.has_key('guest_wish'):
        if wishlist.objects.filter(guest_wishlist=request.session['guest_wish'],products_id=product):
            messages.error(request, "item already in your wishlist")
        else:
            wishlist.objects.create(guest_wishlist=request.session['guest_wish'],products_id=product)
    else:
        guest_wishlist=str(uuid.uuid4())
        request.session['guest_wish']=guest_wishlist
        wishlist.objects.create(guest_wishlist=guest_wishlist,products_id=product)
    return JsonResponse('success', safe=False)


def remove_guest_wishlist(request):
    data=json.loads(request.body)
    id = data['productid']
    product = products.objects.get(pk=id)
    guest_details = request.session['guest_wish']
    wishlist_details=wishlist.objects.filter(guest_wishlist=guest_details,products_id=product)
    if wishlist_details:
        wishlist_details.delete()
    return JsonResponse('success', safe=False)

def wishlist_handler(request):
    if request.session.has_key('guest_wish'):
        data = wishlist.objects.filter(guest_wishlist=request.session['guest_wish'])
        username=User.objects.get(username=request.user)
        for guestuser in data:
            product = products.objects.get(pk=guestuser.products_id_id)
            if wishlist.objects.filter(user_name=username,products_id=product.id):
                guestuser.delete()
            else:
                guestuser.user_name=username.username
                guestuser.save()
        del request.session['guest_wish']
        return redirect(home)
    else:
        return redirect(home)


def wishlist_count(request):
    if request.session.has_key('logged_in'):
            wish_count=wishlist.objects.filter(user_name=request.user).count()
    else:
        if request.session.has_key('guest_wish'):
            wish_count=wishlist.objects.filter(guest_wishlist=request.session.get('guest_wish')).count()
        else:
            wish_count=0
    return wish_count




def login_with_otp(request):
    if request.method == 'POST':
        mobile_num=request.POST.get('mobile')
        user = userimage.objects.filter(mobile_num=mobile_num)
        if user:
            otp = gen_otp()
            user1=user.first()
            user1.otp = otp
            user1.save()
            message = "pls verify your mobile number. OTP: {}" .format(otp)
            send_sms(message, mobile_num)
            return render(request, 'user/enter_otp.html',{'mobile':mobile_num})
        else:
            messages.error(request, "invalid mobile number")
    return render(request, 'user/otp_login.html')

def check_otp(request):
    if request.method == 'POST':
        otp_num=request.POST.get('otp')
        mobile_num=request.POST.get('mobile')
        user = userimage.objects.filter(mobile_num=mobile_num)
        
        if user is not None:
            user1=user.first()
            main_user = User.objects.get(id=user1.user_name.id)
            if user1.otp == otp_num:
                login(request,main_user)
                request.session['logged_in']= True
                if request.session.has_key('guest'):
                    return redirect(guesthandler)
                else:
                    return redirect('home')
            else:
                messages.error(request, "invalid otp")
        else:
            messages.error(request, "invalid otp")
    else:
        return redirect(userlogin)
    

def gen_otp():
    import math, random
    digits = '1234567890'
    OTP = ''
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP
