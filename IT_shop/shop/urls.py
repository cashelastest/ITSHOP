from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductsList.as_view(), name = 'home'),
    path('ad/', views.AddProduct.as_view(), name = 'add_product'),
    path('products/<slug:product_slug>/', views.ShowProduct.as_view(), name = "ShowProduct"),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/',views.remove_from_cart, name='remove_from_cart'),
]