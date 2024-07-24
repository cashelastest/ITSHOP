from django.db import models

from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	description = models.TextField(verbose_name='description')
	photo = models.ImageField(upload_to='user/%Y/%m/%d')