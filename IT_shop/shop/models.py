from django.db import models
from django.urls import reverse

class Category(models.Model):
	name = models.CharField(max_length = 255)

def __str__(self):
	return self.user.username

class Product(models.Model):
	name =models.CharField(max_length = 255, verbose_name ='name')
	slug= models.SlugField(max_length = 255, unique=True, db_index = True, verbose_name = "URL")
	content = models.TextField(verbose_name="description")
	price = models.IntegerField(verbose_name = 'price')
	category = models.ManyToManyField(Category, verbose_name = "Категория")
	seller = models.CharField(max_length = 100)
	photo = models.ImageField(upload_to = 'products/%Y/%m/%d')
	def save(self, *args, **kwargs):
		self.seller = self.seller.user.username
		if not self.slug:
			self.slug = slugify(unidecode(self.name))
		super().save(*args, **kwargs)
	def get_absolute_url(self):
		return reverse('product', kwargs={'product_slug': self.slug})




