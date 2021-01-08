from django.shortcuts import render

# Create your views here.
def sing_up_view(request):
    return render(request,"accounts/register.html")

def login_view(request):
    return render(request,"accounts/login.html")
