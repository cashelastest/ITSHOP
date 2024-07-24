from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import *
from IT_shop.settings import *
class Edit(UpdateView):
	form_class=UserEditForm
	template_name = 'users/EditProfile.html'
	success_url = reverse_lazy('home')
	extra_context = {
	'default_image':settings.DEFAULT_USER_IMAGE,
	}
	def get_object(self):
		return self.request.user


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegisterUserForm()
    return render(request, 'users/regist.html', {'form': form})
# Create your views here.
# Create your views here.
class LoginUser(LoginView):
	form_class=LoginUserForm
	template_name = 'users/login.html'
	success_url = reverse_lazy('home')
	login_url = reverse_lazy('home')

	def get_context_data(self,*,object_list =None, **kwargs):
		context = super().get_context_data(**kwargs)

		return context


def logout_user(request):
	logout(request)
	return redirect('home')
# Create your views here.
