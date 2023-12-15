from django.db import models
from django.urls import reverse


class Product(models.Model):
    product = models.CharField(max_length=100, verbose_name="продукт")
    price = models.FloatField(default=0, verbose_name="ціна")

    def __str__(self):
        return self.product

    def get_absolute_url(self):
        return reverse("product", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукт"
        ordering = ["product", "price"]
