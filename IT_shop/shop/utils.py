from .models import *

class DataMixin:
	def get_user_context(self, **kwargs):
		context = kwargs
		category= Category.objects.all()
		profile = get_object_or_404(Profile, user=self.request.user)
		context['category'] = category
		context['profile'] = profile
		return context