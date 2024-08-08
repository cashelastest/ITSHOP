from django.shortcuts import render
from .serializers import *
from .permissions import *
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from shop.models import *

class ProductViewSet(viewsets.ModelViewSet):
	serializer_class= ProductSerializer
	def get_queryset(self):
		pk = self.kwargs.get("pk")
		if not pk:
			return Product.objects.filter(is_published = True)
		return Product.objects.filter(pk = pk, is_published=True)

	def get_permissions(self):
		if self.action in ['list', 'retrieve']:
			permission_classes = [AllowAny]
		elif self.action in ['update','partial_update', 'destroy']:
			permission_classes = [IsSellerOrReadOnly]
		elif self.action =='create':
			permission_classes = [IsAuthenticatedOrReadOnly]
		else:
			permission_classes = [IsAuthenticatedOrReadOnly]
		return [permission() for permission in permission_classes]

	@action(methods = ['get'], detail = False)
	def category(self, request):
		cats = Category.objects.all().values('id', 'name')
		return Response({'categories ': cats})
	@action(methods = ['get'], detail = True)
	def user_info(self, request,pk):
		pk = self.kwargs.get('pk')
		if not pk:
			return Response({'error': "Нужно ввести id пользователя"})
		try:
			user = Profile.objects.filter(pk = pk).values()
			return Response({'profile':list(user)})
		except:
			return Response ({'error': "Такого пользователя не существует"})
	@action(methods = ['get'], detail = True)
	def user_products(self, request, pk):
		pk = self.kwargs.get("pk")
		if not pk:
			return Response({'error': "Нужно ввести id пользователя"})

		user_products = Product.objects.filter(seller_id = pk, is_published = True).values()
		return Response({'products':list(user_products)})
		
class ProductList(generics.ListCreateAPIView):
	queryset = Product.objects.filter(is_published=True)
	serializer_class = ProductSerializer
	permission_classes = (IsAuthenticatedOrReadOnly,)


# Create your views here.
