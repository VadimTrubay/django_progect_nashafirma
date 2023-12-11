from django.urls import path, include
from django.contrib.auth.views import (PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)

from users.views import (TermsView, UserLoginView,
                         UserLogOutView,
                         ProfileDetailView,
                         EditProfileView,
                         DeleteProfileView,
                         ResetPasswordView,
                         UserRegistrationView)

urlpatterns = [
    path("terms/", TermsView.as_view(), name="terms"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegistrationView.as_view(), name='register'),
    path("logout/", UserLogOutView.as_view(), name="logout"),
    path("profile/<int:pk>/", include(
        [path("", ProfileDetailView.as_view(), name="profile details"),
         path("edit/", EditProfileView.as_view(), name="edit profile"),
         path("delete/", DeleteProfileView.as_view(), name="delete profile"), ]
    ),
         ),
    path("reset-password/", ResetPasswordView.as_view(), name="password_reset"),
    path("reset-password/done/", PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path("reset-password/confirm/<uidb64>/<token>/",
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                          success_url='users/reset-password/complete/'),
         name='password_reset_confirm'),
    path('reset-password/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
