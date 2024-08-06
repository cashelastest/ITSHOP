from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.home, name = 'home'),
    path('moder/', views.moder, name = 'moder'),
    path('moder/accept/<int:product_id>/', views.accept, name = 'accept'),
    path('moder/ban/<int:product_id>/', views.ban, name = 'ban'),
    path('add-product/', views.AddProduct.as_view(), name = 'add_product'),
    path('products/<slug:product_slug>/', views.ShowProduct.as_view(), name = "ShowProduct"),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/',views.remove_from_cart, name='remove_from_cart'),
    path('<int:pk>/like/', views.AddLike.as_view(), name='like'),
    path('<int:pk>/dislike/',views.AddDislike.as_view(), name='dislike'),
    path('product/<int:pk>/edit/', views.EditProduct.as_view(), name='product_edit'),
    path('product/<int:pk>/delete/', views.DeleteProduct.as_view(), name='product_delete'),
    path('my-products/', views.MyProducts.as_view(), name='my_products'),
    path('products/by/<slug:profile_slug>/', views.SellerProducts.as_view(), name = 'seller_products'),
    path('contact/', views.contact, name = 'contact'),
    path('add-category/', views.CreateCategory.as_view(), name = 'add_product'),
]