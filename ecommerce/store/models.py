from django.db import models
from django.contrib.auth.models import User
CATEGORY_CHOICES=(
    ('S','Shirt'),
    ('M','Mobile Phone'),
)
# Create your models here.
class Customer(models.Model):
    user        =models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    first_name  =models.CharField(max_length=64,null=True)
    last_name   =models.CharField(max_length=64,null=True)
    email       =models.CharField(max_length=200,null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Product(models.Model):
    title       =models.CharField(max_length=256,null=True)
    description =models.TextField(blank=True,null=False)
    price       =models.FloatField()
    category    =models.CharField(choices=CATEGORY_CHOICES,max_length=1)  
    image       =models.ImageField(blank=True, null=True) 

    def __str__(self):
        return self.title
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url

class Order(models.Model):
    customer        =models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered    =models.DateTimeField(auto_now_add=True)
    complete        =models.BooleanField(default=False,null=True,blank=False)
    transaction_id  =models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

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
