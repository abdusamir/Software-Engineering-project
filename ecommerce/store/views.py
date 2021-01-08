from django.shortcuts import render
from .models import Product
# Create your views here.
def store_view(request):
    context={
        "objects":Product.objects.all()
    }
    return render(request,"store/products.html",context)