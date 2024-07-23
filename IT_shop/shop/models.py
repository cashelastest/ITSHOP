from django.db import models
from django.urls import reverse


class Product(models.Model):
	name =models.CharField(max_length = 255, verbose_name ='name')
	slug= models.SlugField(max_length = 255, unique=True, db_index = True, verbose_name = "URL")
	content = models.TextField(verbose_name="description")


# Create your models here.
