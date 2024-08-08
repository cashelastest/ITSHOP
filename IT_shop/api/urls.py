from django.urls import path, include
from .views import *
from rest_framework import routers
from django.urls import re_path
router = routers.SimpleRouter()
router.register(r'products', ProductViewSet, basename = 'products')
app_name = 'api'
urlpatterns =[
path('api-info/', api_info, name = 'api_info'),
path('api/v1/', include(router.urls)),
#path('api/v1/products/category/')
path('api/v1/auth/', include('djoser.urls')),
re_path(r'^auth/', include('djoser.urls.authtoken')),

]