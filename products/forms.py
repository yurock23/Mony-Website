"""
Celeste Ha, Linh Luu, Yurock Heo
COM214 Final Project
"""



from django import forms
from .models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        template_name = 'product.html'
        fields = ('item_name', 'item_image',
        	'item_description', 'item_category',
        	'item_price',
        	)

        widgets ={
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('body',)