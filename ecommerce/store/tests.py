from django.test import TestCase,Client
from .models import *
from django.db.models import Max

class ProductTestCase(TestCase):

    def setUp(self):
        p1 =Product.objects.create(title="title1",price=22,category="C")
        p2 = Product.objects.create(title="title2", price=33, category="M")
        c1=Customer.objects.create(first_name="abdelrahman",last_name="ahmed",email="abdoahemd@gmail.com")
        o1=Order.objects.create(customer=c1,complete=False,transaction_id="56644884441")
        oi1=OrderItem.objects.create(quantity=3,product=p1,order=o1)
        oi2 = OrderItem.objects.create(quantity=1, product=p2, order=o1)

    def test_products_count(self):
        self.assertEqual(Product.objects.all().count(),2)

    def test_order_count(self):
        self.assertEqual(Order.objects.all().count(),1)

    def test_orderitem_count(self):
        self.assertEqual(OrderItem.objects.all().count(),2)

    def test_valid_order(self):
        o1 = Order.objects.get(transaction_id="56644884441")
        self.assertTrue(o1.is_valid_order())

    def test_invalid_order(self):
        o1 = Order.objects.get(transaction_id="56644884441")
        o1.complete=True
        self.assertFalse(o1.is_valid_order())

    def test_index(self):
        c=Client()
        response=c.get("")
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context["objects"].count(),2)
    
    def test_valid_cart_page(self):
        c=Client()
        response=c.get("/cart")
        self.assertEqual(response.status_code,200)

    def test_valid_productpage(self):
        p1=Product.objects.get(title="title1")

        c=Client()
        response=c.get(f"/product/{p1.id}")
        self.assertEqual(response.status_code,200)
    def test_invalid_productpage(self):
        max_id=Product.objects.all().aggregate(Max("id"))["id__max"]

        c=Client()
        response=c.get(f"/product/{max_id+1}")
        self.assertEqual(response.status_code,404)

    def test_profile_not_customers(self):
        c = Client()
        response = c.get("/accounts/profile")
        self.assertEqual(response.status_code, 404)

    def test_add_product_none_seller(self):
        c = Client()
        response = c.get("/accounts/addproduct")
        self.assertEqual(response.status_code, 404)
    


    


    


