from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse
from products.models import Product
from users.models import SiteUser


class Order(models.Model):
    created_at = models.DateField(
        auto_now_add=True, verbose_name=_("створено"))
    user = models.ForeignKey(
        SiteUser,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_("користувач"),
    )
    products = models.ManyToManyField(
        Product,
        through="OrderItem",
        verbose_name=_("продукти")
    )
    done = models.BooleanField(default=False, verbose_name=_("статус"))

    def __str__(self):
        formatted_date_time = self.created_at.strftime("%d %b %Y")
        return formatted_date_time

    def get_absolute_url(self):
        return reverse("view_order", kwargs={"pk": self.pk})

    def calculate_sum_weight(self):
        return round(sum(item.weight for item in self.orderitem_set.all()), 2)

    def calculate_sum_total(self):
        return round(sum(item.calculate_total() for item in self.orderitem_set.all()), 2)

    class Meta:
        verbose_name = _("замовлення")
        verbose_name_plural = _("замовлення")
        ordering = ["created_at", "user"]


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_("замовлення"),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("продукт")
    )
    weight = models.FloatField(default=0, verbose_name=_("вага"))
    note = models.CharField(max_length=100, blank=True,
                            verbose_name=_("нотатка"))

    def __str__(self):
        return f"{self.order}"

    def get_absolute_url(self):
        return reverse("view_order", kwargs={"pk": self.pk})

    def calculate_total(self):
        return round(self.product.price * self.weight, 2)

    class Meta:
        verbose_name = _("продукти")
        verbose_name_plural = _("продукти")
        ordering = ["order", "product", "weight"]
