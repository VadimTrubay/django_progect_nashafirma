from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField,
)

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

    # def __init__(self, *args, **kwargs):
    #     super(RegistrationForm, self).__init__(*args, **kwargs)
    #     self.fields["username"].widget.attrs["placeholder"] = "Enter username"
    #     self.fields["first_name"].widget.attrs["placeholder"] = "Enter first name"
    #     self.fields["last_name"].widget.attrs["placeholder"] = "Enter last name"
    #     self.fields["email"].widget.attrs["placeholder"] = "Enter email"
    #     self.fields["telephone_number"].widget.attrs[
    #         "placeholder"
    #     ] = "Enter phone number"
    #     self.fields["password1"].widget.attrs["placeholder"] = "Enter password"
    #     self.fields["password2"].widget.attrs["placeholder"] = "Confirm password"


class LoginForm(AuthenticationForm):
    captcha = CaptchaField()
    username = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True, "placeholder": "Username"})
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "placeholder": "Password"}
        ),
    )

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

        # widgets = {
        #     "first_name": forms.TextInput(
        #         attrs={"class": "form-control", "placeholder": "Enter your first name"}
        #     ),
        #     "last_name": forms.TextInput(
        #         attrs={"class": "form-control", "placeholder": "Enter your last name"}
        #     ),
        #     "username": forms.TextInput(
        #         attrs={"class": "form-control", "placeholder": "Enter your username"}
        #     ),
        #     "telephone_number": forms.TextInput(
        #         attrs={"class": "form-control", "placeholder": "Enter your number"}
        #     ),
        #     "email": forms.EmailInput(
        #         attrs={
        #             "class": "form-control",
        #             "placeholder": "Enter your email address",
        #         }
        #     ),
        #     "profile_picture": forms.ClearableFileInput(
        #         attrs={"class": "form-control"}
        #     ),
        # }
