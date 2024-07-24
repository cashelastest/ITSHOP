from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
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
	seller = models.ForeignKey('Seller', on_delete = models.PROTECT, verbose_name="Продавец")
	photo = models.ImageField(upload_to = 'products/%Y/%m/%d')
	def save(self, *args, **kwargs):
		self.seller = self.seller.user.username
		if not self.slug:
			self.slug = slugify(unidecode(self.name))
		super().save(*args, **kwargs)
	def get_absolute_url(self):
		return reverse('product', kwargs={'product_slug': self.slug})


class Seller(models.Model):
	slug = models.SlugField(max_length = 255,unique=True, db_index = True)
	user = models.OneToOneField(settings.AUTH_USER_MODEL,  on_delete = models.PROTECT)
	description = models.TextField(verbose_name='description')
	photo = models.ImageField(upload_to='user/%Y/%m/%d', blank=True)

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(unidecode(self.name))
		super().save(*args, **kwargs)
	def get_absolute_url(self):
		return reverse('seller', kwargs={'seller_slug': self.slug})
def __str__(self):
	return self.user.username


class UserManager(BaseUserManager):
	def create_user(self, first_name, last_name, username, email, password = None):
		if not email:
			raise ValueError('Need email adress')
		if not username:
			raise ValueError("Need username")


		user = self.model(
			email = self.normalize_email(email),
			username = username,
			first_name = first_name,
			last_name = last_name,
			)
		user.set_password(password)
		user.save(using = self._db)
		return user

class User(AbstractUser):
	username = models.CharField(max_length = 50)
	first_name = models.CharField(max_length = 255)
	last_name = models.CharField(max_length = 255)
	email = models.EmailField(max_length = 150)
	photo = models.CharField(max_length = 255)
	objects = UserManager()
	#required
	date_joined = models.DateTimeField(auto_now_add=True)
	last_login = models.DateTimeField(auto_now_add=True)
	create_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)
	is_admin = models.BooleanField(default = False)
	is_staff = models.BooleanField(default = False)
	is_active = models.BooleanField(default = False)
	is_superadmin = models.BooleanField(default = False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


	def __str__(self):
		return self.email
	def has_perm(self, perm, obj = None):
		return self.is_admin
	def has_module_perm(self, app_label):
		return True