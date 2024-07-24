from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import *

@login_required
def home(request):
 return render(request, 'shop/home.html')

def edit(request):
	if request.method == 'POST':
		user_form = UserEditForm(request.POST, instance = request.user)
		profile_form = SellerEditForm(instance = request.user.seller)
		if user_form.is_valid() and profile.is_valid():
			user_form.save()
			profile_form.save()
	else:
		user_form = UserEditForm(instance = request.user)

		profile_form = SellerEditForm(instance = request.user.seller)  
		return render(request, 'shop/EditProfile.html', {'user_form': user_form, 'profile_form':profile_form})

class Edit(UpdateView):
	form_class=UserEditForm
	template_name = 'shop/EditProfile.html'
	success_url = reverse_lazy('home')
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
    return render(request, 'shop/regist.html', {'form': form})
# Create your views here.
# Create your views here.
class LoginUser(LoginView):
	form_class=LoginUserForm
	template_name = 'shop/login.html'
	success_url = reverse_lazy('home')
	login_url = reverse_lazy('home')

	def get_context_data(self,*,object_list =None, **kwargs):
		context = super().get_context_data(**kwargs)

		return context


def logout_user(request):
	logout(request)
	return redirect('home')