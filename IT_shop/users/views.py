from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.views import LoginView, PasswordChangeView,PasswordResetConfirmView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordResetView
from IT_shop.settings import DEFAULT_USER_IMAGE
from django.contrib.auth.mixins import LoginRequiredMixin





class MyPasswordResetView(PasswordResetView):
    form_class = MyPasswordResetForm


class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'  # Custom template
    form_class = MyPasswordResetConfirmForm  # You can customize this form if needed
    success_url = reverse_lazy('users:password_reset_complete')  # Redirect after successful password reset

    def form_valid(self, form):
        # Add any custom logic here before the form is saved
        return super().form_valid(form)

class Edit(LoginRequiredMixin ,UpdateView):
    model = Profile
    form_class = UserEditForm
    template_name = 'users/EditProfile.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')
    extra_context = {
        'default_image': settings.DEFAULT_USER_IMAGE,
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user instance to the form
        return kwargs

    def get_object(self):
        return self.request.user.profile


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            if not Profile.objects.filter(user=user).exists():
                Profile.objects.create(user=user)


            return redirect('users:login')
    else:
        form = RegisterUserForm()
    return render(request, 'users/regist.html', {'form': form})
# Create your views here.
# Create your views here.
class LoginUser(LoginView):
	form_class=LoginUserForm
	template_name = 'users/login.html'
	success_url = reverse_lazy('home')



	def get_context_data(self,*,object_list =None, **kwargs):
		context = super().get_context_data(**kwargs)

		return context


def logout_user(request):
	logout(request)
	return redirect('users:login')



class UserPasswordChange(PasswordChangeView):

    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = 'users/password_change_form.html'

    def get_context_data(self, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        return context

class ShowProfile(DetailView):
	model = Profile
	slug_url_kwarg = 'profile_slug'
	template_name = 'users/show_profile.html'
	context_object_name='profile'