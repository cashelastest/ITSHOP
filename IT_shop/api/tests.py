from django.test import TestCase
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient
from shop.models import Product, Profile
from api.serializers import ProductSerializer
from django.contrib.auth.models import User
import base64
from PIL import Image
import io

class ProductSerializerTestCase(TestCase):
    def setUp(self):
        # Создание пользователя и профиля
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile = Profile.objects.create(user=self.user)

        # Создание тестового изображения
        self.image_data = self.create_test_image()

        self.valid_data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': 100.0,
            'photoCode': self.image_data,
        }
    
    def create_test_image(self):
        """Создает тестовое изображение и возвращает его в формате base64"""
        image = Image.new('RGB', (100, 100), color='red')
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return f"data:image/jpeg;base64,{img_str}"
    
    def test_valid_serializer(self):
        serializer = ProductSerializer(data=self.valid_data, context={'request': self.client.request})
        self.assertTrue(serializer.is_valid())
        product = serializer.save()
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.description, 'Test Description')
        self.assertEqual(product.price, 100.0)
        self.assertEqual(product.seller, self.profile)
        self.assertTrue(product.photo)  # Убедитесь, что изображение было сохранено

    def test_invalid_image_data(self):
        invalid_data = self.valid_data.copy()
        invalid_data['photoCode'] = 'invalid_image_data'
        serializer = ProductSerializer(data=invalid_data, context={'request': self.client.request})
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_to_representation(self):
        product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=100.0,
            seller=self.profile,
            photo=self.create_test_image()
        )
        serializer = ProductSerializer(product)
        representation = serializer.to_representation(product)
        self.assertEqual(representation['seller'], self.user.username)

