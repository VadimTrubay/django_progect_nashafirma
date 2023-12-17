from django.db import models
from django.urls import reverse
from products.models import Product
from users.models import SiteUser


class Order(models.Model):
    created_at = models.DateField(auto_now_add=True, verbose_name="створено")
    user = models.ForeignKey(
        SiteUser,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="користувач",
    )
    products = models.ManyToManyField(
        Product,
        through="OrderItem",
        verbose_name="продукти"
    )
    done = models.BooleanField(default=False, verbose_name="статус")

    def __str__(self):
        formatted_date_time = self.created_at.strftime("%d %B %Y")
        return formatted_date_time

    def get_absolute_url(self):
        return reverse("view_order", kwargs={"pk": self.pk})

    def calculate_sum_weight(self):
        return sum(item.weight for item in self.orderitem_set.all())

    def calculate_sum_total(self):
        return round(
            sum(item.calculate_total() for item in self.orderitem_set.all()), 2
        )

    class Meta:
        verbose_name = "замовлення"
        verbose_name_plural = "замовлення"
        ordering = ["created_at", "user"]


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name="замовлення",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="продукт"
    )
    weight = models.FloatField(default=0, verbose_name="вага")
    note = models.CharField(max_length=100, blank=True, verbose_name="нотатка")

    def __str__(self):
        return f"{self.order}"

    def get_absolute_url(self):
        return reverse("view_order", kwargs={"pk": self.pk})

    def calculate_total(self):
        return round(self.product.price * self.weight, 2)

    class Meta:
        verbose_name = "продукти"
        verbose_name_plural = "продукти"
        ordering = ["order", "product", "weight"]
