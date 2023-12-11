from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_file_size(value):
    max_size = 5 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError(_("File size cannot exceed 5 MB."))
