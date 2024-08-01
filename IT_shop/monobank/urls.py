from django.urls import path
from . import views
app_name = 'mono'
urlpatterns = [
    path('create-payment/', views.create_payment, name='create_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('check-payment/<str:invoice_id>/', views.check_payment, name='check_payment'),
    path('webhook/', views.webhook, name='webhook'),
    path('generate-receipt/<str:invoice_id>/', views.generate_receipt, name='generate_receipt'),
]
