from django import forms
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import PasswordChangeForm
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label = 'Юзернейм', widget = forms.TextInput(attrs ={'class':'form-input'}))
    first_name = forms.CharField(label = 'NAME', widget=forms.TextInput(attrs={'class':'form-input'}))
    last_name = forms.CharField(label = 'LASTNAME', widget=forms.TextInput(attrs={'class':'form-input'}))
    email = forms.EmailField(label = 'Почта', widget=forms.EmailInput(attrs={'class':'form-input'}))
    photo = models.ImageField(upload_to='user/%Y/%m/%d', blank=True)
    password1 = forms.CharField(label = 'Твой секретный ключик', widget = forms.PasswordInput(attrs={'class':'form-input'}))
    password2 = forms.CharField(label = 'Повтори', widget = forms.PasswordInput(attrs={'class':'form-input'}))

    class Meta:

        model=get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label = 'Юзернейм', widget = forms.TextInput(attrs ={'class':'form-input'}))
    password = forms.CharField(label = 'Секретный ключик', widget = forms.PasswordInput(attrs={'class':'form-input'}))
class UserEditForm(forms.ModelForm):
    username = forms.CharField(label = 'Юзернейм', widget = forms.TextInput(attrs ={'class':'form-input'}))
    email = forms.EmailField(label = 'Почта')
    photo = forms.ImageField(widget=forms.FileInput)
    class Meta:
        model =get_user_model()
        fields= ('photo','username', 'first_name', 'last_name', 'email',  'description')

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label = 'old', widget = forms.PasswordInput())
    new_password1 = forms.CharField(label = 'new1', widget = forms.PasswordInput())
    new_password2 = forms.CharField(label = 'new2', widget = forms.PasswordInput())

