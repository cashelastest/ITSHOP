from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView,PasswordResetDoneView, PasswordResetCompleteView, PasswordChangeView,PasswordChangeDoneView
from django.urls import reverse_lazy


app_name = "users"

urlpatterns = [
path('profile/', views.Edit.as_view(), name = 'edit_profile'),
path('sign_up/', views.register, name = 'sign_up'),
path('login/', views.LoginUser.as_view(), name = 'login'),
path('logout/', views.logout_user, name = 'logout'),

path('password-change/', views.UserPasswordChange.as_view(), name = 'password_change'),
path('password-change/done/', PasswordChangeDoneView.as_view(template_name = 'users/password_change_done.html'), name = 'password_change_done'),


path('password-reset/', 
	views.MyPasswordResetView.as_view(template_name = 'users/password_reset_form.html',
		email_template_name = "users/password_reset_email.html",
		success_url = reverse_lazy('users:password_reset_done')),
	name = 'password_reset'),

path('password-reset/done/', 
	PasswordResetDoneView.as_view(template_name = 'users/password_reset_done.html'), 
	name = 'password_reset_done'),

path('password-reset/<uidb64>/<token>/', 
	views.PasswordResetConfirmView.as_view(template_name = 'users/password_reset_confirm.html', success_url = reverse_lazy('users:password_reset_complete')), 
	name = 'password_reset_confirm'),

path('password-reset/complete/', 
	PasswordResetCompleteView.as_view(template_name = 'users/password_reset_complete.html'), 
	name = 'password_reset_complete'),
path('profile/<slug:profile_slug>/', views.ShowProfile.as_view(), name = 'ShowProfile')

]