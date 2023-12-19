from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import (PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)

from users.views import (TermsView, UserLoginView,
                         UserLogOutView,
                         ProfileDetailView,
                         EditProfileView,
                         DeleteProfileView,
                         ResetPasswordView,
                         UserRegistrationView,
                         FeedbackCreateView,
                         FeedbackSuccessView,)

urlpatterns = [
    path("terms/", TermsView.as_view(), name="terms"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegistrationView.as_view(), name='register'),
    path("logout/", UserLogOutView.as_view(), name="logout"),
    path('feedback/', FeedbackCreateView.as_view(), name='feedback'),
    path('feedback_success/', FeedbackSuccessView.as_view(),
         name='feedback_success'),

    path("profile/<int:pk>/", include(
        [path("", ProfileDetailView.as_view(), name="profile_details"),
         path("edit/", EditProfileView.as_view(), name="profile_edit"),
         path("delete/", DeleteProfileView.as_view(), name="profile_delete"), ]
    ),
    ),
    path("reset_password/", ResetPasswordView.as_view(), name="password_reset"),
    path("reset_password/done/", PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path("reset_password/confirm/<uidb64>/<token>/",
         PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html',
             success_url=reverse_lazy('password_reset_confirm')),
         name='password_reset_confirm'),
    path('reset_password/complete/',
         PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
