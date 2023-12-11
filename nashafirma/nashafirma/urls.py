from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from orders.views import (HomeView,
                          AboutView,
                          ContactsView,
                          pageNotFound)

urlpatterns = [
                  path("admin/", admin.site.urls),
                  path("captcha/", include("captcha.urls")),
                  path("", HomeView.as_view(), name="home"),
                  path("about/", AboutView.as_view(), name="about"),
                  path("products/", include("products.urls")),
                  path("orders/", include("orders.urls")),
                  path("users/", include("users.urls")),
                  path("contacts/", ContactsView.as_view(), name="contacts"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound
