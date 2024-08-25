from rest_framework import serializers
from shop.models import *
from django.core.files.base import ContentFile
import base64
import io
from PIL import Image, UnidentifiedImageError

class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop('seller')
        profile = Profile.objects.get(user=user)
        validated_data['seller'] = profile

        # Обработка изображения
        image_data = validated_data.pop('photoCode', None)
        if image_data and isinstance(image_data, str):
            try:
                # Очищаем префиксы, если есть
                image_data = self.clean_base64_image_data(image_data)
                
                # Декодируем base64
                img_data = base64.b64decode(image_data)
                
                # Проверяем, можем ли мы открыть изображение
                image = Image.open(io.BytesIO(img_data))
                image.verify()  # Проверяем корректность изображения
                
                # Сохраняем изображение в формате PNG
                image_io = io.BytesIO()
                image.save(image_io, format='PNG')
                
                # Создаем ContentFile
                image_file = ContentFile(image_io.getvalue(), name='temp.png')
                
                validated_data['photo'] = image_file
            except UnidentifiedImageError:
                raise serializers.ValidationError("Ошибка: Не удалось идентифицировать формат изображения.")
            except base64.binascii.Error:
                raise serializers.ValidationError("Ошибка декодирования Base64 данных изображения.")
            except Exception as e:
                raise serializers.ValidationError(f"Неизвестная ошибка: {str(e)}")

        return super().create(validated_data)

    def clean_base64_image_data(self, image_data):
        if image_data.startswith('data:image/'):
            image_data = image_data.split(';base64,')[-1]
        return image_data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['seller'] = instance.seller.user.username
        return representation
