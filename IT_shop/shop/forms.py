from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label = 'Юзернейм', widget = forms.TextInput(attrs ={'class':'form-input'}))
    first_name = forms.CharField(label = 'NAME', widget=forms.TextInput(attrs={'class':'form-input'}))
    last_name = forms.CharField(label = 'LASTNAME', widget=forms.TextInput(attrs={'class':'form-input'}))
    email = forms.EmailField(label = 'Почта', widget=forms.EmailInput(attrs={'class':'form-input'}))
    password1 = forms.CharField(label = 'Твой секретный ключик', widget = forms.PasswordInput(attrs={'class':'form-input'}))
    password2 = forms.CharField(label = 'Повтори', widget = forms.PasswordInput(attrs={'class':'form-input'}))
    class Meta:

        model=User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label = 'Юзернейм', widget = forms.TextInput(attrs ={'class':'form-input'}))
    password = forms.CharField(label = 'Секретный ключик', widget = forms.PasswordInput(attrs={'class':'form-input'}))
class UserEditForm(forms.ModelForm):
    username = forms.CharField(label = 'Юзернейм', widget = forms.TextInput(attrs ={'class':'form-input'}))
    email = forms.EmailField(label = 'Почта')
    class Meta:
        model =User
        fields= {'username', 'first_name', 'last_name', 'email', 'photo'}

class SellerEditForm(forms.ModelForm):

    class Meta:

        model= Seller
        fields ={'description', 'photo'}
class AddProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'content', 'price', 'category', 'photo']