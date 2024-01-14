from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ("product", "price")
    list_totals = [('weight', lambda field: Coalesce(Sum(field), 0, output_field=FloatField()))]
    list_display_links = ("price", "price")
    search_fields = ("product", "price")
    list_editable = ("product",)
    list_filter = ("product", "price")


admin.site.register(Product, ProductAdmin)
