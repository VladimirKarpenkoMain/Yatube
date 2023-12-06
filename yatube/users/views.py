from django.views.generic import CreateView
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView

from django.urls import reverse_lazy

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('posts:index')


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')


class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    success_url = reverse_lazy('users:password_reset_done')


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:email_reset_done')
