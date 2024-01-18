from django.contrib import admin

from .models import Feedback
from .models import SiteUser


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """
    Админ-панель модели профиля
    """
    list_display = ('email', 'ip_address', 'user')
    list_display_links = ('email', 'ip_address')


@admin.register(SiteUser)
class UserAdmin(admin.ModelAdmin):
    """
    Админ-панель модели SiteUser
    """
    list_display = ('username', 'is_staff', 'email', 'first_name', 'last_name', 'telephone_number')
    list_display_links = ('username', 'is_staff', 'email', 'first_name', 'last_name', 'telephone_number')
