from django.shortcuts import render,redirect
from django.contrib.auth import logout,login,authenticate
from .forms import CreateUserForm,NewProduct
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users
from django.contrib.auth.models import Group
from store.models import *
from django.http import Http404
from django.views.generic import CreateView
from django.db import models
from django import forms
from django.db.models import Q
from store.forms import CustomerForm
from store.utils import cartData
from django.http import Http404
# Create your views here.
@unauthenticated_user
def sing_up_view(request):
    form= CreateUserForm()
    if request.method=="POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            name=form.cleaned_data.get('first_name')
            sorc=form.cleaned_data.get('sorc')
            if sorc==True:
                group=Group.objects.get(name='seller')
                user.groups.add(group)
                Customer.objects.create(
                    user=user,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email
                )

            else:
                group = Group.objects.get(name='customer')
                user.groups.add(group)
                Customer.objects.create(
                    user=user,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email
                )
            messages.success(request,"Account was created for "+name)
            if user is not None:
                login(request,user)
                return redirect('store:home-page')
    context={'form':form}
    return render(request,"accounts/register.html",context)


@unauthenticated_user
def login_view(request):
    if request.method=='POST':
        username     = request.POST['username']
        password     = request.POST['password']
        user         = authenticate(request,username=username,password=password)
        if user is not None:
           login(request,user)
           return redirect('store:home-page')
        else:
            messages.info(request,"Username or Password incorrect")
    return render(request,"accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def profile_view(request):
    data = cartData(request)
    cartitems = data['cartitems']
    if not request.user.is_authenticated:
        raise Http404 
    if request.user.groups.exists():
	    group = request.user.groups.all()[0].name

    if group =='seller':
        products = request.user.customer.products.all()
        context={'products':products,'cartitems':cartitems}
        return render(request,"accounts/seller_profile1.html",context)
    
    if group == 'customer':
        x=[]
        y=[]
        wish_list=request.user.customer.wish_list.all()
        products=Product.objects.all()
        for item in wish_list:
            idd=products.get(title=item.title,price=item.price)
            x.append(idd.id)
        zipped=zip(wish_list,x)
        orders=request.user.customer.orders.all()
        for item in orders:
            idd = products.get(title=item.title, price=item.price)
            y.append(idd.id)
        zipped2=zip(orders,y)
        context = {'wishlist':zipped,'cartitems':cartitems,'orders':zipped2}
        return render(request, "accounts/buyer_profile1.html", context)
class AddProduct(CreateView):
    model=Product
    template_name="accounts/add_product.html"
    fields=['title','description','price','category','image']

@allowed_users(allowed_roles=['seller'])
def add_product(request):
    data = cartData(request)
    cartitems = data['cartitems']
    form=NewProduct(request.POST,request.FILES or None)
    if form.is_valid():
        form.save()
        title=form.cleaned_data['title']
        description = form.cleaned_data['description']
        price= form.cleaned_data['price']
        category=form.cleaned_data['category']
        pieces=form.cleaned_data['pieces']
        product=Product.objects.get(title=title,description=description,price=price,category=category,pieces=pieces)
        request.user.customer.products.add(product)
        form=NewProduct()
        return redirect("store:home-page")
    context={
        'form': form,
        'cartitems':cartitems
    }
    return render(request, "accounts/add_product.html",context)

def edit_profile(request):
    data = cartData(request)
    cartitems = data['cartitems']
    customer = request.user.customer
    form=CustomerForm(instance=customer)
    
    if request.method=='POST':
        form=CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()

    context={
        'form':form,
        'cartitems':cartitems
    }
    return render(request,"accounts/edit_profile.html",context)


