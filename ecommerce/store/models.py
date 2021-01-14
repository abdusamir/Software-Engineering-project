from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

CATEGORY_CHOICES=(
    ('S','Clothes and fashion'),
    ('M','Mobile Phone'),
    ('G','Games and Books'),
    ('C','Computer and electronics')
)
# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=256, null=True)
    description = models.TextField(blank=True, null=False)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=1)
    image = models.ImageField(blank=True, null=True)
    pieces =models.IntegerField(blank=False,default=1,null=False)

    def __str__(self):
        return str(self.title)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    def get_absolute_url(self):
        return reverse('store:home-page')


class Customer(models.Model):
    user        =models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    first_name  =models.CharField(max_length=64,null=True)
    last_name   =models.CharField(max_length=64,null=True)
    email       =models.CharField(max_length=200,null=True)
    profile_pic =models.ImageField(default="profile.png",blank=True,null=True)
    wish_list   =models.ManyToManyField(Product,blank=True,related_name="wishlist")
    phone       =models.CharField(max_length=20,null=True,blank=True)
    products    = models.ManyToManyField(Product, blank=True,related_name='products')
    orders      =models.ManyToManyField(Product,blank=True,related_name='orders')
    recommended = models.ManyToManyField(Product, blank=True)
    def __str__(self):
        return self.first_name

    @property
    def get_wishlist(self):
        return self.wish_list.all()



class Order(models.Model):
    customer        =models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered    =models.DateTimeField(auto_now_add=True)
    complete        =models.BooleanField(default=False,null=True,blank=False)
    transaction_id  =models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    @property
    def shipping(self):
        return True
    def is_valid_order(self):
        if self.complete:
            return False
        else:
            return True


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total=self.product.price * self.quantity
        return total
    @property
    def get_product(self):
        return self.product
    def is_valid_orderitem(self):
        if self.product.exists():
            return True
        else:
            return False
class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)

    address = models.CharField(max_length=256, null=True)
    city = models.CharField(max_length=256, null=True)
    country = models.CharField(max_length=256, null=True)
    zipcode = models.CharField(max_length=256, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
