from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models

from users.validators import validate_file_size


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.username, filename)


class SiteUser(AbstractUser):
    MAX_LEN_USERNAME = 50
    MIN_LEN_USERNAME = 2
    MAX_LEN_FIRST_NAME = 50
    MIN_LEN_FIRST_NAME = 2
    MAX_LEN_SECOND_NAME = 50
    MIN_LEN_SECOND_NAME = 2
    MAX_LEN_TELEPHONE_NUMBER = 20
    MIN_LEN_TELEPHONE_NUMBER = 7

    username = models.CharField(
        unique=True,
        max_length=MAX_LEN_USERNAME,
        validators=(validators.MinLengthValidator(MIN_LEN_USERNAME),),
        default='',
        verbose_name=_('логін'),
    )
    email = models.EmailField(
        unique=True,
        default='',
        verbose_name=_('email'),
    )
    first_name = models.CharField(
        max_length=MAX_LEN_FIRST_NAME,
        default='',
        validators=(validators.MinLengthValidator(MIN_LEN_FIRST_NAME),),
        verbose_name=_('імя'),
    )
    last_name = models.CharField(
        max_length=MAX_LEN_SECOND_NAME,
        default='',
        validators=(validators.MinLengthValidator(MIN_LEN_SECOND_NAME),),
        verbose_name=_('прізвище'),
    )
    telephone_number = models.CharField(
        max_length=MAX_LEN_TELEPHONE_NUMBER,
        default='',
        validators=(validators.MinLengthValidator(MIN_LEN_TELEPHONE_NUMBER),),
        verbose_name=_('телефон'),
    )
    profile_picture = models.ImageField(
        upload_to=user_directory_path,
        default='profile_pictures/profile_picture_default.jpg',
        validators=[
            validate_file_size,
            validators.FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png']
            ),
        ],
        verbose_name=_('фото'),
    )


class Feedback(models.Model):
    subject = models.CharField(max_length=255, verbose_name=_('тема листа'))
    email = models.EmailField(
        max_length=255, verbose_name=_('ваш email'))
    content = models.TextField(verbose_name=_('зміст листа'))
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name=_('дата відправки'))
    ip_address = models.GenericIPAddressField(
        verbose_name=_('IP адреса відправника'),  blank=True, null=True)
    user = models.ForeignKey(SiteUser, verbose_name=_('користувач'),
                             on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _('зворотній звязок')
        verbose_name_plural = _('зворотній звязок')
        ordering = ['-time_create']
        db_table = 'app_feedback'

    def __str__(self):
        return f'вам лист від {self.email}'
