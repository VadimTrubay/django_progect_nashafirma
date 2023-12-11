from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import (
    ListView,
    CreateView,
    TemplateView,
    DeleteView,
    UpdateView,
    DetailView,
)
from django.urls import reverse_lazy, reverse
from django.db.models import Q

from utils.utils import DataMixin
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm


class HomeView(DataMixin, TemplateView):
    title = "Home"
    template_name = "orders/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class AboutView(DataMixin, TemplateView):
    title = "About"
    template_name = "orders/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class AddOrderView(DataMixin, CreateView):
    title = "+ Add new order"
    form_class = OrderForm
    template_name = "orders/add_order.html"
    success_url = reverse_lazy("all_orders")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_menu = self.get_menu_context(title=self.title)
        context = dict(list(context.items()) + list(context_menu.items()))
        return context


class ViewOrderView(DetailView):
    title = "View order"
    model = Order
    template_name = "orders/view_order.html"
    context_object_name = "order"
    success_url = reverse_lazy("all_orders")

    def get_queryset(self):
        if self.request.user.username == "admin":
            object_list = self.model.objects.all().reverse()
        else:
            object_list = self.model.objects.filter(user=self.request.user).reverse()
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class AllOrdersView(ListView):
    title = "All orders"
    paginate_by = 5
    model = Order
    template_name = "orders/all_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        if self.request.user.username == "admin":
            object_list = self.model.objects.all().reverse()
        else:
            object_list = self.model.objects.filter(user=self.request.user).reverse()
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class EditOrderView(UpdateView):
    title = "Edit order"
    form_class = OrderForm
    template_name = "orders/edit_order.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def get_success_url(self):
        # Получаем предыдущий URL-адрес из сессии
        referer = self.request.session.get("previous_url")
        if referer:
            return referer
        return reverse_lazy("all_orders")

    def get(self, request, *args, **kwargs):
        previous_url = self.request.META.get("HTTP_REFERER")
        self.request.session["previous_url"] = previous_url
        return super().get(request, *args, **kwargs)

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Order, pk=pk)


class EditItemProductView(UpdateView):
    title = "Edit product"
    form_class = OrderItemForm
    template_name = "orders/edit_item_product.html"
    context_object_name = "order"
    success_url = reverse_lazy("all_orders")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(OrderItem, pk=pk)

    def get_success_url(self):
        order_id = self.object.order.id
        return reverse("view_order", kwargs={"pk": order_id})


class DeleteOrderView(DeleteView):
    title = "Delete order"
    model = Order
    template_name = "orders/delete_order.html"
    success_url = reverse_lazy("all_orders")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class DeleteItemProductView(DeleteView):
    title = "Delete product"
    model = OrderItem
    template_name = "orders/delete_item_product.html"
    success_url = reverse_lazy("all_orders")

    def get_success_url(self):
        order_id = self.object.order.id
        return reverse("view_order", kwargs={"pk": order_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class AddItemView(CreateView):
    title = "+ Add new product to order"
    form_class = OrderItemForm
    template_name = "orders/add_item.html"
    success_url = reverse_lazy("all_orders")

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        order = Order.objects.get(pk=pk, user=self.request.user, done=False)
        form.instance.order = order
        return super().form_valid(form)

    def get_success_url(self):
        order_id = self.object.order.id
        return reverse("view_order", kwargs={"pk": order_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class SearchResultsOrderView(ListView):
    title = "Result search order"
    model = Order
    template_name = "orders/search_results_order.html"
    context_object_name = "orders"

    def get_queryset(self):
        query = self.request.GET.get("search_order")
        if self.request.user.username == "admin":
            if query:
                queryset = self.model.objects.all().filter(
                    Q(user__username__icontains=query)
                    | Q(created_at__day__icontains=query)
                    | Q(created_at__month__icontains=query)
                    | Q(created_at__year__icontains=query)
                    | Q(done__icontains=query)
                )
                queryset = queryset.reverse()
                return queryset
            return self.model.objects.none()
        else:
            user_orders = self.model.objects.filter(user=self.request.user)
            if query:
                queryset = user_orders.filter(
                    Q(user__username__icontains=query)
                    | Q(created_at__day__icontains=query)
                    | Q(created_at__month__icontains=query)
                    | Q(created_at__year__icontains=query)
                    | Q(done__icontains=query)
                )
                queryset = queryset.reverse()
                return queryset
            return self.model.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class ContactsView(DataMixin, TemplateView):
    title = "Contacts"
    template_name = "orders/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


def pageNotFound(request, exception):
    return render(request, "404.html", status=404)
