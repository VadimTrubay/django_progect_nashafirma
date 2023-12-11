from orders.models import Order, OrderItem
from django import forms


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["done"]


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["product", "weight", "note"]
