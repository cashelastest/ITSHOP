from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.db import models
from django.conf import settings
from django.urls import reverse

class Profile(models.Model):
	slug = models.SlugField(max_length=100, blank = True)
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	description = models.CharField(max_length = 100, blank =True)
	photo = models.ImageField(upload_to = 'user/%Y/%m/%d/', blank = True)
	#cart = models.OneToOneField("shop.Cart", on_delete = models.PROTECT, blank = True, null = True)
	def get_absolute_url(self):
		return reverse('profile', kwargs = {'profile_slug': self.slug})
	def __str__(self):
		return self.user.username

def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user = instance)
		user_profile.slug = slugify(user_profile.user.username)
		user_profile.save()
post_save.connect(create_profile, sender = User)


