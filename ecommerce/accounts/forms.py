from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from store.models import Product

class CreateUserForm(UserCreationForm):
    sorc=forms.BooleanField(required=False,label="Do u want to register as a seller?")
    class Meta:
        model= User
        fields= [
            'username','first_name','last_name','email','password1','password2','sorc'
        ]

class NewProduct(forms.ModelForm):
    description=forms.CharField(required=False,widget=forms.Textarea(attrs={"rows":3}))
    class Meta:
        model=Product
        fields=[
            'title',
            'description',
            'price',
            'category',
            'image',
            'pieces'
        ]