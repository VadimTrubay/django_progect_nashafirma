from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models

from users.validators import validate_file_size


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.username, filename)


class SiteUser(AbstractUser):
    MAX_LEN_USERNAME = 20
    MIN_LEN_USERNAME = 2
    MAX_LEN_FIRST_NAME = 25
    MIN_LEN_FIRST_NAME = 2
    MAX_LEN_SECOND_NAME = 25
    MIN_LEN_SECOND_NAME = 2
    MAX_LEN_TELEPHONE_NUMBER = 15
    MIN_LEN_TELEPHONE_NUMBER = 7

    username = models.CharField(
        unique=True,
        max_length=MAX_LEN_USERNAME,
        validators=(validators.MinLengthValidator(MIN_LEN_USERNAME),),
        default="",
    )
    email = models.EmailField(
        null=False,
        blank=False,
        unique=True,
        default="",
    )
    first_name = models.CharField(
        null=True,
        blank=True,
        max_length=MAX_LEN_FIRST_NAME,
        default="",
        validators=(validators.MinLengthValidator(MIN_LEN_FIRST_NAME),),
    )
    last_name = models.CharField(
        null=True,
        blank=True,
        max_length=MAX_LEN_SECOND_NAME,
        default="",
        validators=(validators.MinLengthValidator(MIN_LEN_SECOND_NAME),),
    )
    telephone_number = models.CharField(
        null=True,
        blank=True,
        max_length=MAX_LEN_TELEPHONE_NUMBER,
        validators=(validators.MinLengthValidator(MIN_LEN_TELEPHONE_NUMBER),),
    )
    profile_picture = models.ImageField(
        upload_to=user_directory_path,
        default="profile_pictures/profile_picture_default.jpg",
        null=True,
        blank=True,
        validators=[
            validate_file_size,
            validators.FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png"]
            ),
        ],
    )
