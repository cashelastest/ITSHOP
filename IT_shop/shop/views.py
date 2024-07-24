from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

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

