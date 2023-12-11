from .models import Order, OrderItem
from django.utils import timezone
from datetime import timedelta
from admin_totals.admin import ModelAdminTotals
from django.contrib import admin
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models import FloatField
from django.utils.html import format_html


class DateYesterdayFieldListFilter(admin.DateFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)

        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
        yesterday = today - timedelta(days=1)

        self.links = list(self.links)
        self.links.insert(
            2,
            (
                "Yesterday",
                {
                    self.lookup_kwarg_since: str(yesterday),
                    self.lookup_kwarg_until: str(today),
                },
            ),
        )

        self.links = list(self.links)
        self.links.insert(
            2,
            (
                "Yesterday and Today",
                {
                    self.lookup_kwarg_since: str(yesterday),
                    self.lookup_kwarg_until: str(tomorrow),
                },
            ),
        )


class MyModelAdmin(admin.ModelAdmin):
    list_display = ["created_at", "user", "done", "id"]
    search_fields = ("created_at", "user", "done", "products", "id")
    list_display_links = ("created_at", "user")
    # list_editable = ()
    list_filter = (("created_at", DateYesterdayFieldListFilter), "user", "done", "id")


class OrderItemAdmin(MyModelAdmin, ModelAdminTotals, admin.ModelAdmin):
    def order_user(self, obj):
        return obj.order.user if obj.order else None

    def order_done(self, obj):
        return obj.order.done if obj.order else None

    def order_done_icon(self, obj):
        if obj.order.done:
            return format_html(
                '<span style="color: green;">&#10004;</span>'
            )  # Checkmark icon
        else:
            return format_html(
                '<span style="color: red;">&#10008;</span>'
            )  # Cross icon

    order_done_icon.short_description = "done"

    order_user.short_description = "user"
    order_done.short_description = "done"

    list_display = [
        "product",
        "weight",
        "note",
        "order_done_icon",
        "order_user",
        "order",
        "id",
    ]
    search_fields = (
        "order__done",
        "order__user",
        "order",
        "product",
        "weight",
        "note",
        "id",
    )
    list_display_links = ("product", "weight", "note")
    list_totals = [
        ("weight", lambda field: Coalesce(Sum(field), 0, output_field=FloatField()))
    ]
    # list_editable = ()
    list_filter = (
        "order__done",
        "order__user",
        ("order__created_at", DateYesterdayFieldListFilter),
        "product",
        "weight",
        "id",
    )


admin.site.register(Order, MyModelAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
