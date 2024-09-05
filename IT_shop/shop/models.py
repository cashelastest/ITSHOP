from django.db import models
from django.urls import reverse
from users.models import Profile
from slugify import slugify
from unidecode import unidecode
from django.contrib.auth.models import User


class Category(models.Model):
	slug = models.SlugField(max_length = 255)
	name = models.CharField(max_length=255)
	def __str__(self):
		return self.name
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(unidecode(self.name))
		super().save(*args, **kwargs)	


class Product(models.Model):
	name =models.CharField(max_length = 255, verbose_name ='Назва товару:')
	slug= models.SlugField(max_length = 255, unique=True, db_index = True, verbose_name = "URL", blank = True)
	content = models.TextField(verbose_name="Опис товару: ")
	price = models.IntegerField(verbose_name = 'price')
	category = models.ForeignKey(Category,on_delete = models.PROTECT, verbose_name = "Категорія")
	seller = models.ForeignKey(Profile, on_delete = models.PROTECT, blank = True, null = True)
	is_banned = models.BooleanField(blank = True, null = True, default =False)
	is_published = models.BooleanField(blank = True, null = True,default=False)
	likes = models.ManyToManyField(User, blank=True, related_name='likes')
	dislikes = models.ManyToManyField(User, blank=True,related_name='dislikes')
	photo = models.ImageField(upload_to='products/%Y/%m/%d', blank=False, null=True, verbose_name="Фото товара")
	photoCode = models.TextField(null = True, blank = False)
	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)
	def get_absolute_url(self):
		return reverse('product', kwargs={'product_slug': self.slug})

class ProductImages(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='images')
	photo = models.ImageField(upload_to = 'products/%Y/%m/%d', blank=False, null=False, verbose_name="")
class Cart(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"