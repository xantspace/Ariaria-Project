from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'min_order_quantity', 'stock_quantity', 'image', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
