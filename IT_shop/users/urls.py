from django.urls import path
from . import views

urlpatterns = [
path('edit/', views.Edit.as_view(), name = 'edit_profile'),
path('sign_up/', views.register, name = 'sign_up'),
path('login/', views.LoginUser.as_view(), name = 'login'),
]