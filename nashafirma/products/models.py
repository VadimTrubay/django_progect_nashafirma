from django.db import models
from django.urls import reverse


class Product(models.Model):
    product = models.CharField(max_length=100, blank=True, verbose_name="product")
    price = models.FloatField(default=0, blank=True, null=True, verbose_name="price")

    def __str__(self):
        return self.product

    def get_absolute_url(self):
        return reverse("product", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "product"
        ordering = ["product", "price"]
