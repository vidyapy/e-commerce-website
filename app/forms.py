from django import forms
from app.models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','category','desc','price','product_available_count','img']
        widget = {
            'name': forms.TextInput(attrs={'class':'form_control'}),
            'category': forms.Select(attrs={'class':'form_control'}),
            'desc': forms.Textarea(attrs={'class':'form_control'}),
            'price': forms.NumberInput(attrs={'class':'form_control'}),
            'product_available_count': forms.NumberInput(attrs={'class':'form_control'}),
            'img': forms.FileInput(attrs={'class':'form_control'}),

        }
        
# class CheckoutForm(forms.Form):
#     street_address=forms.CharField(widget=forms.TextInput(attrs={
#         'class':'form-control',
#         'placeholder':'123 main street',
#     }))
#     appartment_address=forms.CharField(required=False,widget=forms.TextInput(attrs={
#         'class':'form-control',
#         'placeholder':'Apartment or suit',
#     }))
#     country= forms.CharField(widget=forms.TextInput(attrs={
#         'class':'form-control',
#         'placeholder':'country',

#     }))
#     zip= forms.CharField(widget=forms.TextInput(attrs={
#         'class':'form-control',
        

#     }))

