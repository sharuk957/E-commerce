import json
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import products, category, subcategory, brand
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control
from django.contrib import messages
import datetime
from django.http import JsonResponse
# Create your views here.

# admin login & logout

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminlogin(request):
    if request.session.has_key('user_logged'):
        return redirect('adminhome')
    else:
        return render(request, 'adminlogin.html')

@login_required(login_url='adminlogin')
def adminlogout(request):
    del request.session['user_logged']
    logout(request)
    return redirect(adminlogin)

 
# dashboard

def adminhome(request):
    if request.session.has_key('user_logged'):
        return render(request, 'dashboard.html')
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
                        return redirect(adminhome)
                    else:
                        messages.error(request, "invalid password")
                        return redirect(adminlogin)
                else:
                    messages.error(request, "invalid username")
                    return redirect(adminlogin)
            else:
                messages.error(request, "invalid username")
                return redirect(adminlogin)
        else:
            return redirect(adminlogin)



#user management

@login_required(login_url='adminlogin')
def usermanagment(request):
    data = User.objects.all()
    return render(request, 'user.html', {'user_datas': data})


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
        return render(request, 'maincategory.html', {'data': category_data})



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
        return render(request, 'editmaincategory.html', {'data': edit_data})



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
                return redirect(subcategories)
        elif subcategory.objects.filter(slug=sub_category_slug):
            messages.error(
                request, "slug already exists pls choose edit option")
            return redirect(subcategories)
        else:
            sub_category_des = request.POST['sub_category_desc']
            subcategory.objects.create(category_name=category_name,sub_category_name=sub_category_name, slug=sub_category_slug, description=sub_category_des)
            return redirect(subcategories)
    else:
        category_data = category.objects.all()
        sub_category_data = subcategory.objects.all()
        return render(request, 'subcategory.html', {'data': sub_category_data,'category_data':category_data})


@login_required(login_url='adminlogin')
def edit_subcategory(request, pk):
    if request.method == 'POST':
        edit_data = subcategory.objects.get(pk=pk)
        if edit_data.category_name != (category.objects.get(category_name=request.POST['category'])) or edit_data.sub_category_name != request.POST['sub_category']:
            if subcategory.objects.filter(sub_category_name=request.POST['sub_category'],category_name = category.objects.get(category_name=request.POST['category'])):
                messages.error(request, "subcategory already exists")
                return redirect(edit_subcategory,pk)
            else:
                edit_data.sub_category_name = request.POST['sub_category']
                edit_data.category_name = category.objects.get(category_name=request.POST['category'])
        if edit_data.slug != request.POST['sub_category_slug']:
            if subcategory.objects.filter(slug=request.POST['sub_category_slug']):
                messages.error(request, "slug already exists")
                return redirect(edit_subcategory, pk)
            else:
                edit_data.slug = request.POST['sub_category_slug']
        edit_data.description = request.POST['sub_category_desc']
        edit_data.save()
        return redirect(subcategories)
    else:
        category_data = category.objects.all()
        sub_category_data = subcategory.objects.get(pk=pk)
        return render(request, 'editsubcategory.html', {'sub_data': sub_category_data,'category_data':category_data})

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
        return render(request, 'brand.html', {'brand_data': brand_data,'category_data':category_data,'data':sub_category_data})


@login_required(login_url='adminlogin')
def edit_brand(request, pk):
    if request.method == 'POST':
        edit_data = brand.objects.get(pk=pk)
        if edit_data.category_name != (category.objects.get(category_name=request.POST['category'])) or edit_data.sub_category_name != subcategory.objects.get( id=request.POST['sub_category']) or edit_data.brand_name !=request.POST['brand_uid']:
            if brand.objects.filter(category_name=category.objects.get(category_name=request.POST['category']),sub_category_name=subcategory.objects.get( id=request.POST['sub_category']),brand_name=request.POST['brand_name']):
                messages.error(request, "brand already exists")
                return redirect(edit_brand,pk)
            else:
                edit_data.sub_category_name = subcategory.objects.get( id=request.POST['sub_category'])
                edit_data.category_name = category.objects.get(category_name=request.POST['category'])
                edit_data.brand_name = request.POST['brand_name']
        if edit_data.slug != request.POST['brand_slug']:
            if brand.objects.filter(slug=request.POST['brand_slug']):
                messages.error(request, "slug already exists")
                return redirect(edit_brand, pk)
            else:
                edit_data.slug = request.POST['brand_slug']
        edit_data.save()
        return redirect(brandlist)
    else:
        category_data = category.objects.all()
        sub_category_data = subcategory.objects.all()
        brand_data = brand.objects.get(pk=pk)
        return render(request, 'editbrand.html', {'brand_data': brand_data,'category_data':category_data,'data':sub_category_data})

@login_required(login_url='adminlogin')
def delete_brand(request, pk):
    del_data = brand.objects.get(pk=pk)
    del_data.delete()
    return redirect(brandlist)


#product management

@login_required(login_url='adminlogin')
def productlist(request):
    product_list = products.objects.all()
    return render(request, 'productlist.html', {'data': product_list})


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
        product_image1 = request.FILES.get('images1')
        product_image2 = request.FILES.get('images2')
        product_image3 = request.FILES.get('images3')
        product_image4 = request.FILES.get('images4')
        date = datetime.datetime.now()
        add_product = products(date=date,product_name=product_name, description=product_desc, image1=product_image1,image2=product_image2,image3=product_image3,image4=product_image4,
                               sub_category=product_subcategory, category=product_category, price=product_price, unit=product_unit, brand=product_brand)
        add_product.save()
        return redirect(productlist)
    else:
        category_data = category.objects.all()
        subcategory_data = subcategory.objects.all()
        brand_data = brand.objects.all()
        return render(request, 'addproduct.html', {'cat': category_data, 'sub_cat': subcategory_data, 'brand': brand_data})





@login_required(login_url='adminlogin')
def edit_product(request, id):
    if request.method == 'POST':
        edit_data = products.objects.get(id=id)
        if edit_data.product_name != request.POST['product_name']:
            if products.objects.filter(product_name=request.POST['product_name']):
                messages.error(request, "product already exists")
                return redirect(edit_product, id)
            else:
                edit_data.product_name = request.POST['product_name']
        edit_data.description = request.POST['product_desc']
        edit_data.image1 = request.FILES.get('images1')
        edit_data.image2 = request.FILES.get('images2')
        edit_data.image3 = request.FILES.get('images3')
        edit_data.image4 = request.FILES.get('images4')
        edit_data.category = category.objects.get(category_name=request.POST['category'])
        edit_data.subcategory = subcategory.objects.get(id=request.POST['subcategory'])
        edit_data.brand = brand.objects.get(id=request.POST['brand'])
        edit_data.price = request.POST['price']
        edit_data.unit = request.POST['units']
        # edit_data.size = request.POST['size']
        edit_data.save()
        return redirect('productlist')
    else:
        edit_data = products.objects.get(id=id)
        category_data = category.objects.all()
        subcategory_data = subcategory.objects.all()
        brand_data = brand.objects.all()
        return render(request, 'editproduct.html', {'cat': category_data, 'sub_cat': subcategory_data, 'brand': brand_data, 'data': edit_data})

@login_required(login_url='adminlogin')
def delete_product(request, id):
    del_data = products.objects.get(id=id)
    del_data.delete()
    return redirect(productlist)

#order management

def ordermanagment(request):
    return render(request,'ordermanagment.html')

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
    