from django.core.files.base import ContentFile
import json
from userlogin.models import orders
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import products, category, subcategory, brand,offer,coupon
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control
from django.contrib import messages
import datetime
from django.http import JsonResponse
from django.db.models import Sum
import base64
import uuid

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminlogin(request):
    if request.session.has_key('user_logged'):
        return redirect('adminhome')
    else:
        return render(request, 'admin/adminlogin.html')



@login_required(login_url='adminlogin')
def adminlogout(request):
    del request.session['user_logged']
    logout(request)
    return redirect(adminlogin)

 
 
# dashboard

def adminhome(request):
    if request.session.has_key('user_logged'):
        total_orders=orders.objects.all().count()
        total_products=products.objects.all().count()
        total_sale=orders.objects.aggregate(Sum('total'))
        category_list = subcategory.objects.order_by('sub_category_name').distinct('sub_category_name')
        quantity_list=[]
        for k in category_list:
            product_list  =products.objects.filter(sub_category=k.id)
            quantity_sum=0
            for i in product_list:
                quantity = orders.objects.filter(products=i.id)
                for j in quantity:
                    quantity_sum+=j.quantity
            quantity_list.append(quantity_sum)
        every_product = products.objects.all()
        context={
            'total_orders':total_orders,
            'total_products':total_products,
            'total_sale':total_sale,
            'category':category_list,
            'quantity':quantity_list,
            'product_list':every_product
        }
        return render(request, 'admin/dashboard.html',context)
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            admin = User.objects.filter(username=username)
            if admin:
                super_user = User.objects.get(username=username)
                if super_user.is_superuser:
                    admin = authenticate(username=username, password=password)
                    if admin is not None:
                        login(request, admin)
                        request.session['user_logged'] = True
                    else:
                        messages.error(request, "invalid password")
                else:
                    messages.error(request, "invalid username")
            else:
                messages.error(request, "invalid username")
        return redirect(adminlogin)



#user management

@login_required(login_url='adminlogin')
def usermanagment(request):
    data = User.objects.all()
    return render(request, 'admin/user.html', {'user_data': data})


@login_required(login_url='adminlogin')
def userblock(request, id):
    data = User.objects.get(id=id)
    data.is_active = False
    data.save()
    return redirect(usermanagment)


@login_required(login_url='adminlogin')
def userunblock(request, id):
    data = User.objects.get(id=id)
    data.is_active = True
    data.save()
    return redirect(usermanagment)


# category management


@login_required(login_url='adminlogin')
def categories(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        if category.objects.filter(category_name=category_name):
            messages.error(
                request, "category already exists pls choose edit option")
            return redirect(categories)
        category_slug = request.POST['category_slug']
        if category.objects.filter(slug=category_slug):
            messages.error(
                request, "slug already exists pls choose edit option")
            return redirect(categories)
        category_des = request.POST['category_desc']
        category.objects.create(category_name=category_name, slug=category_slug, description=category_des)
        return redirect(categories)
    else:
        category_data = category.objects.all()
        return render(request, 'admin/maincategory.html', {'data': category_data})



@login_required(login_url='adminlogin')
def edit_category(request, pk):
    if request.method == 'POST':
        edit_data = category.objects.get(pk=pk)
        if edit_data.category_name != request.POST['category_name']:
            if category.objects.filter(category_name=request.POST['category_name']):
                messages.error(request, "category already exists")
                return redirect(edit_category, pk)
            else:
                edit_data.category_name = request.POST['category_name']
        if edit_data.slug != request.POST['category_slug']:
            if category.objects.filter(slug=request.POST['category_slug']):
                messages.error(request, "slug already exists")
                return redirect(edit_category, pk)
            else:
                edit_data.slug = request.POST['category_slug']
        edit_data.description = request.POST['category_desc']
        edit_data.save()
        return redirect(categories)
    else:
        edit_data = category.objects.get(pk=pk)
        return render(request, 'admin/editmaincategory.html', {'data': edit_data})



@login_required(login_url='adminlogin')
def delete_category(request, category_name):
    del_data = category.objects.get(category_name=category_name)
    del_data.delete()
    return redirect(categories)


# sub category management


@login_required(login_url='adminlogin')
def subcategories(request):
    if request.method == 'POST':
        category_name = category.objects.get(category_name=request.POST['category'])
        sub_category_name = request.POST['sub_category']
        sub_category_slug = request.POST['sub_category_slug']
        if subcategory.objects.filter(sub_category_name=request.POST['sub_category'],category_name = category.objects.get(category_name=request.POST['category'])):
                messages.error(request, "subcategory already exists pls choose edit option")
        elif subcategory.objects.filter(slug=sub_category_slug):
            messages.error(
                request, "slug already exists pls choose edit option")
        else:
            sub_category_des = request.POST['sub_category_desc']
            subcategory.objects.create(category_name=category_name,sub_category_name=sub_category_name, slug=sub_category_slug, description=sub_category_des)
        return redirect(subcategories)
    else:
        category_data = category.objects.all()
        sub_category_data = subcategory.objects.all()
        offers = offer.objects.all()
        return render(request, 'admin/subcategory.html', {'data': sub_category_data,'category_data':category_data,'offers':offers})


@login_required(login_url='adminlogin')
def edit_subcategory(request, pk):
    edit_data = subcategory.objects.get(pk=pk)
    if request.method == 'POST':
        category_name =request.POST['category']
        subcategory_name=request.POST['sub_category']
        subcategory_slug = request.POST['sub_category_slug']
        category_object = category.objects.get(category_name=category_name)
        if edit_data.category_name != category_object or edit_data.sub_category_name != subcategory_name:
            if subcategory.objects.filter(sub_category_name=subcategory_name,category_name =category_object):
                messages.error(request, "subcategory already exists")
                return redirect(edit_subcategory,pk)
            else:
                edit_data.sub_category_name = subcategory_name
                edit_data.category_name = category_object
        if edit_data.slug != subcategory_slug:
            if subcategory.objects.filter(slug=subcategory_slug):
                messages.error(request, "slug already exists")
                return redirect(edit_subcategory, pk)
            else:
                edit_data.slug = subcategory_slug
        edit_data.description = request.POST['sub_category_desc']
        edit_data.save()
        return redirect(subcategories)
    else:
        category_data = category.objects.all()
        return render(request, 'admin/editsubcategory.html', {'sub_data': edit_data,'category_data':category_data})



@login_required(login_url='adminlogin')
def delete_subcategory(request, pk):
    del_data = subcategory.objects.get(pk=pk)
    del_data.delete()
    return redirect(subcategories)


# brand management

@login_required(login_url='adminlogin')
def brandlist(request):
    if request.method == 'POST':
        brand_category = category.objects.get(category_name=request.POST['category'])
        brand_sub_category = subcategory.objects.get(id=request.POST['sub_category'])
        
        brand_name = request.POST['brand_name']

        brand_slugs = request.POST.get('brand_uid')
        
        if brand.objects.filter(sub_category_name=brand_sub_category,category_name = brand_category,brand_name = brand_name):
            messages.error(request, "brand already exists pls choose edit option")
            return redirect(brandlist)
        if brand.objects.filter(slug=brand_slugs):
            messages.error(
                request, "slug already exists pls choose edit option")
            return redirect(brandlist)
        brand.objects.create(brand_name=brand_name, slug = brand_slugs,category_name=brand_category,sub_category_name=brand_sub_category)
        return redirect(brandlist)
    else:
        category_data = category.objects.all()
        sub_category_data = subcategory.objects.all()
        brand_data = brand.objects.all()
        return render(request, 'admin/brand.html', {'brand_data': brand_data,'category_data':category_data,'data':sub_category_data})


@login_required(login_url='adminlogin')
def edit_brand(request, pk):
    edit_data = brand.objects.get(pk=pk)
    if request.method == 'POST':
        category_name = category_name=request.POST['category']
        subcategory_name = request.POST['sub_category']
        brand_slugs = request.POST['brand_slug']
        brand_name = request.POST['brand_name']
        category_object = category.objects.get(category_name=category_name)
        subcategory_objects = subcategory.objects.get(id=subcategory_name)
        if edit_data.category_name != category_object or edit_data.sub_category_name != subcategory_objects or edit_data.brand_name !=brand_name:
            if brand.objects.filter(category_name=category_object,sub_category_name=subcategory_objects,brand_name=brand_name):
                messages.error(request, "brand already exists")
                return redirect(edit_brand,pk)
            else:
                edit_data.sub_category_name = subcategory_objects
                edit_data.category_name = category_object
                edit_data.brand_name = brand_name
        if edit_data.slug != brand_slugs:
            if brand.objects.filter(slug=brand_slugs):
                messages.error(request, "slug already exists")
                return redirect(edit_brand, pk)
            else:
                edit_data.slug = brand_slugs
        edit_data.save()
        return redirect(brandlist)
    else:
        category_data = category.objects.all()
        sub_category_data = subcategory.objects.filter(category_name=edit_data.category_name.id)
        return render(request, 'admin/editbrand.html', {'brand_data': edit_data,'category_data':category_data,'data':sub_category_data})

@login_required(login_url='adminlogin')
def delete_brand(request,pk):
    del_data = brand.objects.get(pk=pk)
    del_data.delete()
    return redirect(brandlist)


#product management

@login_required(login_url='adminlogin')
def productlist(request):
    offers = offer.objects.all()
    product_list = products.objects.all()
    return render(request, 'admin/productlist.html', {'data': product_list,'offers':offers})


@login_required(login_url='adminlogin')
def addproduct(request):
    if request.method == 'POST':
        product_name = request.POST['product_name']
        if products.objects.filter(product_name=product_name):
            messages.error(
                request, "product already exists pls choose edit option")
            return redirect(addproduct)
        product_desc = request.POST['product_desc']
        product_category = category.objects.get(category_name=request.POST['category'])
        product_subcategory = subcategory.objects.get(id=request.POST['subcategory'])
        product_brand = brand.objects.get(id=request.POST['brand'])
        product_price = request.POST['price']
        product_unit = request.POST['units']
        # size = request.POST['size']
        image1 = request.POST.get('pro_img1')
        
        image2 = request.POST.get('pro_img2')
        image3 = request.POST.get('pro_img3')
        image4 = request.POST.get('pro_img4')
        
        format, img1 = image1.split(';base64,')
        ext = format.split('/')[-1]
        product_image1 = ContentFile(base64.b64decode(img1), name= product_name + '1.' + ext)
        
        format, img2 = image2.split(';base64,')
        ext = format.split('/')[-1]
        product_image2 = ContentFile(base64.b64decode(img2), name= product_name + '2.' + ext)
        
        format, img3 = image3.split(';base64,')
        ext = format.split('/')[-1]
        product_image3 = ContentFile(base64.b64decode(img3), name= product_name + '3.' + ext)
        
        format, img4 = image4.split(';base64,')
        ext = format.split('/')[-1]
        product_image4 = ContentFile(base64.b64decode(img4), name= product_name + '4.' + ext)
        
        
        date = datetime.datetime.now()
        add_product = products(date=date,product_name=product_name, description=product_desc, image1=product_image1,image2=product_image2,image3=product_image3,image4=product_image4,
                               sub_category=product_subcategory, category=product_category, price=product_price, unit=product_unit, brand=product_brand)
        add_product.save()
        return redirect(productlist)
    else:
        category_data = category.objects.all()
        subcategory_data = subcategory.objects.all()
        brand_data = brand.objects.all().order_by('id')
        return render(request, 'admin/addproduct.html', {'cat': category_data, 'sub_cat': subcategory_data, 'brand': brand_data})





@login_required(login_url='adminlogin')
def edit_product(request, id):
    edit_data = products.objects.get(id=id)
    if request.method == 'POST':
        
        products_name = request.POST['product_name']
        if edit_data.product_name != products_name:
            if products.objects.filter(product_name=products_name):
                messages.error(request, "product already exists")
                return redirect(edit_product, id)
            else:
                edit_data.product_name = products_name
        edit_data.description = request.POST['product_desc']
        if request.FILES.get('images1'):
            edit_data.image1 = request.FILES.get('images1')
        if request.FILES.get('images2'):
            edit_data.image2 = request.FILES.get('images2')
        if request.FILES.get('images3'):
            edit_data.image3 = request.FILES.get('images3')
        if request.FILES.get('images4'):
            edit_data.image4 = request.FILES.get('images4')
        edit_data.category = category.objects.get(category_name=request.POST['category'])
        edit_data.sub_category = subcategory.objects.get(id=request.POST['subcategory'])
        edit_data.brand = brand.objects.get(id=request.POST['brand'])
        edit_data.price = request.POST['price']
        edit_data.unit = request.POST['units']
        # edit_data.size = request.POST['size']
        edit_data.save()
        return redirect('productlist')
    else:
        category_data = category.objects.all()
        subcategory_data = subcategory.objects.filter(category_name = edit_data.category.id)
        brand_data = brand.objects.filter(sub_category_name = edit_data.sub_category.id,category_name = edit_data.category.id)
        return render(request, 'admin/editproduct.html', {'cat': category_data, 'sub_cat': subcategory_data, 'brand': brand_data, 'data': edit_data})

@login_required(login_url='adminlogin')
def delete_product(request, id):
    del_data = products.objects.get(id=id)
    del_data.delete()
    return redirect(productlist)

#order management

def ordermanagment(request):
    if request.method == 'POST':
        data=json.loads(request.body)
        order_id=data['order_id']
        status=data['status']
        order_data = orders.objects.get(id=order_id)
        order_data.status=status
        order_data.save()
        return JsonResponse("success",safe=False)
    else:
        order_data = orders.objects.all().order_by("id")
        return render(request,'admin/ordermanagment.html',{'orders_data':order_data})

def dropdownview(request):
    data=json.loads(request.body)
    selected_val=data['selection']
    action=data['action']
    
    if action=="category" or action=="brandcategory":
        category_val=category.objects.get(category_name=selected_val)
        sub_category=subcategory.objects.filter(category_name=category_val)
        # return render(request,'subcategorydropdown.html',{'subcategory_data':sub_category})
        return JsonResponse(list(sub_category.values('id','sub_category_name')),safe=False)
    else:
        selected_category=data['category']
        sub_category=subcategory.objects.get(id=selected_val)
        brand_name=brand.objects.filter(sub_category_name=sub_category,category_name=category.objects.get(category_name=selected_category))
        # return render(request,'branddroplist.html',{'brand_data':brand_name})
        return JsonResponse(list(brand_name.values('id','brand_name')),safe=False)

def offermanagement(request):
    if request.method == 'POST':
        offer_name = request.POST.get('Offer_name')
        offer_percentage = request.POST.get('Offer_percentage')
        offer_expire_date = request.POST.get('Expiry_date')
        offer_expire_time = request.POST.get('Expiry_time')
        offer.objects.create(offer_name=offer_name, percentage=offer_percentage,expiry_date=offer_expire_date,expiry_time=offer_expire_time)
        return redirect(offermanagement)
    else:
        offers = offer.objects.all()
        return render(request, 'admin/offer.html',{'offers': offers})

def offer_edit(request,id):
    if request.method == 'POST':
        offers = offer.objects.get(id=id)
        offers.offer_name= request.POST.get('Offer_name')
        offers.percentage = request.POST.get('Offer_percentage')
        offers.expiry_date = request.POST.get('Expiry_date')
        offers.expiry_time = request.POST.get('Expiry_time')
        offers.save()
        return redirect(offermanagement)
    else:
        offers = offer.objects.get(id=id)
        return render(request, 'admin/edit_offer.html',{'offer':offers})


def offer_delete(request, id):
    offers = offer.objects.get(id=id)
    offers.delete()
    return redirect(offermanagement)

def add_product_offer(request):
    if request.method == 'POST':
        id = request.POST.get('product_id')
        product = products.objects.get(id=id)
        product.product_offer = request.POST.get('product_offer')
        offers = offer.objects.get(offer_name=product.product_offer)
        product.offer_type = 'product'
        offer_price = (offers.percentage*product.price)/100
        product.product_offer_price = product.price - offer_price
        product.save()
    return redirect(productlist)




def add_category_offer(request):
    if request.method == 'POST':
        id = request.POST.get('sub_category_id')
        category_data = subcategory.objects.get(id=id)
        category_data.subcategory_offer = request.POST.get('subcategory_offer')
        offers = offer.objects.get(offer_name=category_data.subcategory_offer)
        category_data.save()
        product_data = products.objects.filter(sub_category=id)
        for product in product_data:
            if product.offer_type == 'product':
                continue
            else:
                product.product_offer = offers.offer_name
                product.offer_type = 'subcategory'
                offer_price = (offers.percentage*product.price)/100
                product.product_offer_price = product.price - offer_price
                product.save()
    return redirect(subcategories)


def couponmanagement(request):
    if request.method == 'POST':
        minimal_rate = request.POST.get('minimal_rate')
        coupon_percentage = request.POST.get('coupon_percentage')
        coupon_expire_date = request.POST.get('Expiry_date')
        coupon_expire_time = request.POST.get('Expiry_time')
        coupon.objects.create(minimal_rate=minimal_rate, coupon_code=uuid.uuid4(), percentage=coupon_percentage,expiry_date=coupon_expire_date,expiry_time=coupon_expire_time)
        return redirect(couponmanagement)
    else:
        coupons = coupon.objects.all()
        return render(request, 'admin/coupon.html',{'coupons': coupons})

def coupon_edit(request,id):
    if request.method == 'POST':
        coupons = coupon.objects.get(id=id)
        coupons.minimal_rate= request.POST.get('minimal_rate')
        coupons.percentage = request.POST.get('coupon_percentage')
        coupons.expiry_date = request.POST.get('Expiry_date')
        coupons.expiry_time = request.POST.get('Expiry_time')
        coupons.save()
        return redirect(couponmanagement)
    else:
        coupons = coupon.objects.get(id=id)
        return render(request, 'admin/edit_coupon.html',{'coupons':coupons})


def coupon_delete(request, id):
    coupons = coupon.objects.get(id=id)
    coupons.delete()
    return redirect(couponmanagement)



def check_validity(request):
    date = datetime.datetime.now().date()
    time = datetime.datetime.now().time()
    offers = offer.objects.filter(expiry_date__gte=date,expiry_time__gte=time)
    coupons = coupon.objects.filter(expiry_date__gte=date,expiry_time__gte=time)
    coupons.delete()
    offers.delete()
    return JsonResponse('success',safe=False)

def sales_report(request):
    if request.method == 'POST':
        from_date = request.POST.get('from')
        to_date = request.POST.get('to')
        # datetime.Combine(from_date, datetime.min.time())
        # datetime.combine(to_date, datetime.min.time())
        report = orders.objects.filter(date__range=[from_date, to_date])
        print(report)
        return render(request, 'admin/salesreport.html',{'orders_data':report})
    else:
        report = orders.objects.all()
        return render(request, 'admin/salesreport.html',{'orders_data':report}) 
    
