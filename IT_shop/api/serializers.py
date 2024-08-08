from rest_framework import serializers
from shop.models import *


class ProductSerializer(serializers.ModelSerializer):
	seller = serializers.HiddenField(default = serializers.CurrentUserDefault())
	class Meta:
		model = Product
		fields=('__all__')
	def to_representation(self, instance):
		representation = super().to_representation(instance)
		# Делает seller видимым при GET запросах
		representation['seller'] = instance.seller.user.username  # или другое поле, например, 'id'
		return representation