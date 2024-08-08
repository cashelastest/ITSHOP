from django import forms
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, SetPasswordForm
from django.contrib.auth.views import PasswordChangeForm
from django.forms import ModelForm
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm

from django.utils.translation import gettext_lazy as _

class MyPasswordResetForm(BasePasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'charfield', "autocomplete": "email"}),
    )

class MyPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(label = 'Придумайте новий та надійний пароль', widget = forms.PasswordInput(attrs={'class':'charfield','placeholder':"Придумайте новий пароль"}))
    new_password2 = forms.CharField(label = 'Повторіть новий пароль', widget = forms.PasswordInput(attrs={'class':'charfield','placeholder':"Повторіть пароль"}))
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label = 'Юзернейм', widget = forms.TextInput(attrs ={'class':'charfield', 'placeholder':" Ваш юзернейм"}))
    #first_name = forms.CharField(label = 'NAME', widget=forms.TextInput(attrs={'class':'charfield','placeholder':''' Ваше РЕАЛЬНЕ ім'я'''}))
    #last_name = forms.CharField(label = 'Прізвище', widget=forms.TextInput(attrs={'class':'charfield','placeholder':'Також РЕАЛЬНЕ прізвище'}))
    email = forms.EmailField(label = 'Пошта', widget=forms.EmailInput(attrs={'class':'charfield','placeholder':'Email'}))
    #photo = models.ImageField(upload_to='user/%Y/%m/%d', blank=True)
    password1 = forms.CharField(label = 'Твій таємний ключик', widget = forms.PasswordInput(attrs={'class':'charfield', 'placeholder':"Пароль"}))
    password2 = forms.CharField(label = 'Повтори', widget = forms.PasswordInput(attrs={'class':'charfield', 'placeholder':"Повторіть пароль"}))

    class Meta:

        model=get_user_model()
        fields = ('username', 'email', 'password1', 'password2')
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label = 'Юзернейм', widget = forms.TextInput(attrs ={'class':'charfield', 'placeholder':" Ваш юзернейм"}))
    password = forms.CharField(label = 'Таємний ключик', widget = forms.PasswordInput(attrs={'class':'charfield','placeholder':"Пароль"}))

class UserEditForm(ModelForm):
    username = forms.CharField(label='Юзернейм', widget=forms.TextInput(attrs={'class': 'charfield', 'placeholder':" Ваш юзернейм"}))
    first_name = forms.CharField(label='''Ім'я''', widget=forms.TextInput(attrs={'class': 'charfield','placeholder':''' Ваше РЕАЛЬНЕ ім'я'''}))
    last_name = forms.CharField(label='Прізвище', widget=forms.TextInput(attrs={'class': 'charfield','placeholder':'Також РЕАЛЬНЕ прізвище'}))
    email = forms.EmailField(label='Пошта', widget=forms.EmailInput(attrs={'class': 'charfield','placeholder':'Email'}))
    description = forms.CharField(label='Про себе:', widget=forms.Textarea(attrs={'class':'textarea' , 'placeholder': 'Напишіть щось про себе. Це побачать інші користувачі'}), required=False)
    #photo = forms.ImageField(label='Фото:',required=False)

    class Meta:
        model = Profile
        fields = ('photo', 'description')
        labels = {
            'photo': 'Фотографія',  # Custom label in Russian
        }
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'file-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = self.instance.user
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label = 'Старий пароль', widget = forms.PasswordInput(attrs={'class':'charfield','placeholder':"Ввеедіть старий пароль"}))
    new_password1 = forms.CharField(label = 'Придумайте новий та надійний пароль', widget = forms.PasswordInput(attrs={'class':'charfield','placeholder':"Придумайте новий пароль"}))
    new_password2 = forms.CharField(label = 'Повторіть новий пароль', widget = forms.PasswordInput(attrs={'class':'charfield','placeholder':"Повторіть пароль"}))

