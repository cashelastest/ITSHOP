from django import forms
from .models import *
from django.forms.widgets import TextInput

class CategoryForm(forms.ModelForm):
    name = forms.CharField(label ='Назва категорії', widget=forms.TextInput(attrs={'class':'charfield', 'placeholder': 'Введіть назву категорії'}))
    class Meta:
        model = Category
        fields = ('name',)

class DataListTextInput(TextInput):
    template_name = 'shop/widgets/datalist.html'

    def __init__(self, datalist_id='', *args, **kwargs):
        self.datalist_id = datalist_id
        self.datalist = kwargs.pop('datalist', [])
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget'].update({
            'datalist_id': self.datalist_id,
            'datalist': self.datalist,
        })
        return context

class FilterForm(forms.Form):
        price = models.PositiveIntegerField(verbose_name = 'min_price')
        price = models.PositiveIntegerField(verbose_name = 'max_price')

class AddProduct(forms.ModelForm):
    name = forms.CharField(
        label='Назва товару', 
        widget=forms.TextInput(attrs={'class':'charfield','placeholder': 'Назва товару'})
    )
    content = forms.CharField(
        label='Опис',
        widget=forms.Textarea(attrs={'class':'textarea','placeholder': 'Тут ви можете написати опис до товару(Стан, причину продажи, можливість торгу)'})
    )
    category = forms.ModelChoiceField(
        label='Категорія',
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'charfield', 'placeholder': 'Виберіть категорію'})
    )
    price = forms.CharField(
        label="Ціна",
        widget=forms.NumberInput(attrs={'class': 'charfield', 'placeholder': 'Впишіть ціну:'})
    )

    class Meta:
        model = Product
        fields = ['name', 'content', 'price', 'category', 'photo']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'charfield'}),
            'content': forms.Textarea(attrs={'class': 'charfield'}),
            'price': forms.NumberInput(attrs={'class': 'charfield'}),
            'category': forms.Select(attrs={'class': 'charfield'}),
        }

class AddImages(forms.ModelForm):

    class Meta:
        model = ProductImages
        fields = ['photo']
AddImagesFormSet = forms.inlineformset_factory(Product,ProductImages,form=AddImages,can_delete=False, extra=3)


