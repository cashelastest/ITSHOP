from django import forms
from .models import *

class FilterForm(forms.Form):
        price = models.PositiveIntegerField(verbose_name = 'min_price')
        price = models.PositiveIntegerField(verbose_name = 'max_price')

class AddProduct(forms.ModelForm):
    class Meta:

        model = Product
        fields = ['name', 'content', 'price', 'category']
class AddImages(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ['photo', 'caption']
AddImagesFormSet = forms.inlineformset_factory(Product,ProductImages,form=AddImages, extra=3)