from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

from orders.views import (HomeView,
                          AboutView,
                          pageNotFound)


i18n_urls = (
    path("i18n", include("django.conf.urls.i18n")),
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("products/", include("products.urls")),
    path("orders/", include("orders.urls")),
    path("users/", include("users.urls")),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n", include("django.conf.urls.i18n")),
    path("captcha/", include("captcha.urls")),
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("products/", include("products.urls")),
    path("orders/", include("orders.urls")),
    path("users/", include("users.urls")),
]

handler404 = pageNotFound

urlpatterns.extend(i18n_patterns(*i18n_urls, prefix_default_language=False))
urlpatterns.extend(
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
