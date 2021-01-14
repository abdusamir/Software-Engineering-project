from django.shortcuts import render,get_object_or_404
from .models import *
from django.http import JsonResponse
import json
from django.views.generic import ListView
from django.db.models import Q
import datetime
from .utils import cartData,cookieCart,guestOrder
# Create your views here.
def store_view(request):
    data = cartData(request)
    cartitems = data['cartitems']

    context={
        "objects":Product.objects.all(),
        "cartitems":cartitems
    }
    return render(request,"store/products.html",context)

def update_item(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    customer = request.user.customer
    product=Product.objects.get(id=productId)
    order,created =Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created =OrderItem.objects.get_or_create(order=order,product=product)
    if action=='add':
        orderItem.quantity=(orderItem.quantity+1)
    elif action=='remove':
        orderItem.quantity = (orderItem.quantity-1)

    orderItem.save()
    if orderItem.quantity <=0 or action=='delete':
        orderItem.delete()

    return JsonResponse('item was added', safe=False)

def update_wishlist(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    product=Product.objects.get(id=productId)
    customer=request.user.customer
    customer.wish_list.add(product)
    return JsonResponse('item was added',safe=False)

def cart(request):
    data = cartData(request)
    cartitems = data['cartitems']
    order = data['order']
    items = data['items']

    context={'items':items,'order':order,'cartitems':cartitems}
    return render(request,"store/cart_page.html",context)


def search_results(request):
    data = cartData(request)
    cartitems = data['cartitems']

    if request.method == 'GET':
        query = request.GET.get('q')

        submitbutton = request.GET.get('submit')

        if query is not None:
            category=query[0]
            lookups = Q(title__icontains=query) | Q(category__icontains=category)
            results = Product.objects.filter(lookups).distinct()
            count=results.all().count()
            context = {'object_list': results,
                       'submitbutton': submitbutton,
                       'count': count,
                       'cartitems':cartitems}

            return render(request, 'store/search.html', context)

        else:
            return render(request, 'store/search.html',{
                'cartitems':cartitems}
                )

    else:
        return render(request, 'store/search.html', {
            'cartitems': cartitems})

def checkout(request):
    data = cartData(request)
    cartitems = data['cartitems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order,'cartitems':cartitems}
    return render(request, "store/checkout1.html", context)


def product_view(request, id):
    data = cartData(request)
    cartitems = data['cartitems']
    product = get_object_or_404(Product,id=id)
    context = {
        'object': product,'cartitems':cartitems
    }
    return render(request, "store/colom.html", context)

def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)

    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        
        
    else:
        customer,order=guestOrder(request,data)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        items = order.orderitem_set.all()
        for item in items:
            customer.orders.add(item.get_product)
            product = Product.objects.get(
                title=item.get_product.title, price=item.get_product.price)
            product.pieces-=1
        order.complete = True
    order.save()
    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        country=data['shipping']['country'],
        zipcode=data['shipping']['zip']
        )
    return JsonResponse('Payment coplete',safe=False)

def customer_service(request):
    return render(request,"store/help.html")

def tags(request,cat):
    lookups = Q(category__icontains=cat)
    results = Product.objects.filter(lookups).distinct()
    category=results[0].get_category_display
    data = cartData(request)
    cartitems = data['cartitems']
    return render(request,"store/tags.html",{
        'object_list':results,
        'category':category,
        'cartitems':cartitems
    })
def unique(list1):
    list_set=set(list1)
    unique_list=list(list_set)
    return unique_list
def recommended(request):
    wishlist = request.user.customer.wish_list.all()
    x=[]
    customer=request.user.customer
    products = Product.objects.all()
    for item in wishlist:
        idd=products.get(title=item.title,price=item.price)
        x.append(idd.category)
    
    categories=unique(x)
    for item in products:
        if item.category in x:
            customer.recommended.add(item)
    recommended=customer.recommended.distinct()
    return (request,"store/recommended.html",{
        'object_list':recommended
    })

