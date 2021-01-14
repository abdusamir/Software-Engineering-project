from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model=Customer
        field='__all__'
        exclude=['user']