import json 
from .models import *
from accounts.models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart={}

    items=[]
    order={'get_cart_total':0,'get_cart_items':0}
    cartitems = order['get_cart_items']
    for i in cart:
        try:
            cartitems+= cart[i]['quantity']
            product=Product.objects.get(id=i)
            total=(product.price*cart[i]['quantity'])
            order['get_cart_total']+=total
            order['get_cart_items']+=cart[i]['quantity']

            item={
                'product':{
                    'id':product.id,
                    'title':product.title,
                    'price':product.price,
                    'imageURL':product.imageURL
                },
                'quantity':cart[i]['quantity'],
                'get_total':total,

                }
            items.append(item)
        except:
            pass
    return {'cartitems':cartitems,'order':order,'items':items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartitems = cookieData['cartitems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartitems':cartitems,'order':order,'items':items}

def guestOrder(request,data):
    print('user not logged in')
    first_name = data['form']['first_name']
    last_name = data['form']['last_name']
    email = data['form']['email']
    cookieData = cookieCart(request)
    items = cookieData['items']
    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.first_name = first_name
    customer.last_name = last_name
    customer.save()
    order = Order.objects.create(
        customer=customer, complete=False
    )
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderitem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer,order

