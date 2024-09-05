from rest_framework.test import APITestCase
from rest_framework import status
from shop.models import *
from users.models import *
import os
from termcolor import colored
class ProductTest(APITestCase):
	def setUp(self):
		self.category = Category.objects.create(
			name = "test 1"
			)
		self.user = User.objects.create(
			username = "TestUser",
			password = "TestPassword"
			)
		#self.profile = Profile.objects.create(user = self.user)

		Product.objects.create(
			name = "Gojo",
			content = "HIII? Love u",
			price = 120,
			category = self.category,
			seller = self.user.profile,
			is_banned = False,
			is_published = True
					)
		self.data = {
		"name" :"Test Name",
		"content":"Test Description",
		"price": 250,
		"category": self.category.id,
		"seller":self.user.profile.id,
		"is_banned" : False,
		"is_published" : True,
		"likes":[],
		"dislikes":[]
		}
		self.client.force_authenticate(user = self.user)
		self.base_url = "/api/v1"
	def test_slugify_category(self):
		self.assertEqual(self.category.slug, "test-1")

		print('\n\n\x1b[30;42m' + 'test_slugify_category PASSED ' + '\x1b[0m')
	def test_get_products(self):
		url = self.base_url + '/products/'
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		print('\n\n\x1b[30;42m' + 'test get model PASSED ' + '\x1b[0m')
	def test_add_product(self):
		url =self.base_url + "/products/"

		response = self.client.post(url, self.data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		print("\n\n\x1b[30;42m test_add_product PASSED \x1b[0m")
	def test_get_detail_product(self):
		url = self.base_url + f"/products/1/"
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		print("\n\n\x1b[30;42m test_get_detail_product PASSED \x1b[0m")
	def test_put_extra_info(self):
		url = self.base_url + "/products/1/"
		data = {
		"name": "ale"
		}
		response = self.client.patch(url,data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		print("\n\n\x1b[30;42m test_put_extra_info PASSED \x1b[0m")