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
	name =models.CharField(max_length = 255, verbose_name ='name')
	slug= models.SlugField(max_length = 255, unique=True, db_index = True, verbose_name = "URL")
	content = models.TextField(verbose_name="description")
	price = models.IntegerField(verbose_name = 'price')
	category = models.ManyToManyField(Category, verbose_name = "Категория")
	seller = models.ForeignKey("users.Profile", on_delete = models.PROTECT, blank = True, null = True)
	is_published = models.BooleanField(blank = True, null = True,default=False)

	likes = models.ManyToManyField(User, blank=True, related_name='likes')
	dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
	def toggle_like(self, user):
		if user in self.likes.all():
			self.likes.remove(user)
		else:
			self.likes.add(user)
		self.save()

	def toggle_dislike(self, user):
		if user in self.dislikes.all():
			self.dislikes.remove(user)
		else:
			self.dislikes.add(user)
		self.save()

	def likes_count(self):
		return self.likes.count()

	def dislikes_count(self):
		return self.dislikes.count()

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)
	def get_absolute_url(self):
		return reverse('product', kwargs={'product_slug': self.slug})
class ProductImages(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, blank = True, null = True,related_name='images')
	photo = models.ImageField(upload_to = 'products/%Y/%m/%d', verbose_name = "")
	caption = models.CharField(max_length=100, blank=True, null = True)
class Cart(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

