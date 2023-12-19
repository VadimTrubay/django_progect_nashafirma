from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField,
)
from users.models import Feedback
from captcha.fields import CaptchaField

UserModel = get_user_model()


class RegistrationForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta:
        model = UserModel
        fields = (
            "username",
            # "first_name",
            # "last_name",
            "email",
            # "telephone_number",
            "password1",
            "password2",
        )


class LoginForm(AuthenticationForm):
    captcha = CaptchaField()

    class Meta:
        model = UserModel
        fields = ['username', 'password']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = [
            "first_name",
            "last_name",
            "username",
            "telephone_number",
            "email",
            "profile_picture",
        ]


class FeedbackCreateForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Feedback
        fields = ('subject', 'email', 'content')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'form-control', 'autocomplete': 'off'})
