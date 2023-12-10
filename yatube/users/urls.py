from django.urls import path

from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeDoneView, PasswordResetDoneView,PasswordResetCompleteView
from .views import SignUp, UserPasswordChangeView, UserPasswordResetView, UserPasswordResetConfirmView

from django.contrib.auth.decorators import login_required

app_name = 'users'

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logged_out.html'), name='logout'),

    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='email_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='email_reset_done'),

    path('password_change/', login_required(UserPasswordChangeView.as_view()), name='password_change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
]
