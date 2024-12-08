from django.utils.translation import gettext as _
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
from django.utils import timezone
from utils.utils import DataMixin, GetContextDataMixin
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm
from datetime import timedelta


class HomeView(GetContextDataMixin, DataMixin, TemplateView):
    title = _("Головна")
    template_name = "orders/index.html"


class AboutView(GetContextDataMixin, DataMixin, TemplateView):
    title = _("Про нас")
    template_name = "orders/about.html"


class AddOrderView(GetContextDataMixin, DataMixin, CreateView):
    title = _("Додати нове замовлення")
    form_class = OrderForm
    template_name = "orders/add_order.html"
    success_url = reverse_lazy("all_orders")

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        new_order_id = self.object.id
        self.success_url = reverse("view_order", args=[new_order_id])
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_menu = self.get_menu_context(title=self.title)
        context = dict(list(context.items()) + list(context_menu.items()))
        return context


class ViewOrderView(GetContextDataMixin, DetailView):
    title = _("Переглянути замовлення")
    model = Order
    template_name = "orders/view_order.html"
    context_object_name = "order"
    success_url = reverse_lazy("all_orders")

    def get_queryset(self):
        if self.request.user.username == "admin":
            object_list = self.model.objects.all().reverse()
        else:
            object_list = self.model.objects.filter(
                user=self.request.user).reverse()
        return object_list


class AllOrdersView(GetContextDataMixin, ListView):
    title = _("Всі замовлення")
    paginate_by = 40
    model = Order
    template_name = "orders/all_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        time_period = self.request.GET.get('time', 'day')
        queryset = self.model.objects.all()
        now = timezone.now()
        if time_period == 'day':
            result = queryset.filter(created_at__gte=now - timedelta(days=1))
        elif time_period == 'week':
            result = queryset.filter(created_at__gte=now - timedelta(weeks=1))
        elif time_period =='month':
            result = queryset.filter(created_at__gte=now - timedelta(days=31))
        elif time_period == 'year':
            result = queryset.filter(created_at__gte=now - timedelta(days=365))
        elif time_period == 'all':
            result = queryset
        if self.request.user.is_superuser:
            object_list = result.order_by('-created_at')
        else:
            object_list = result.filter(user=self.request.user).order_by('-created_at')
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем выбранный период в контекст
        context['selected_period'] = self.request.GET.get('time', 'day')
        return context


class EditOrderDoneView(GetContextDataMixin, UpdateView):
    title = _("Змінити статус замовлення")
    form_class = OrderForm
    template_name = "orders/edit_order_done.html"
    context_object_name = "order"


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


class EditItemProductView(GetContextDataMixin, UpdateView):
    title = _("Змінити продукт")
    form_class = OrderItemForm
    template_name = "orders/edit_item_product.html"
    context_object_name = "order"
    success_url = reverse_lazy("all_orders")

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(OrderItem, pk=pk)

    def get_success_url(self):
        order_id = self.object.order.id
        return reverse("view_order", kwargs={"pk": order_id})


class DeleteOrderView(GetContextDataMixin, DeleteView):
    title = _("Видалити замовлення")
    model = Order
    template_name = "orders/delete_order.html"
    success_url = reverse_lazy("all_orders")

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('all_orders')


class DeleteItemProductView(GetContextDataMixin, DeleteView):
    title = _("Видалити продукт")
    model = OrderItem
    template_name = "orders/delete_item_product.html"
    success_url = reverse_lazy("all_orders")

    def get_success_url(self):
        order_id = self.object.order.id
        return reverse("view_order", kwargs={"pk": order_id})


class AddItemView(GetContextDataMixin, CreateView):
    title = _("Додати новий продукт до замовлення")
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


class SearchResultsOrderView(GetContextDataMixin, ListView):
    title = _("Результати пошуку замовлення")
    paginate_by = 40
    model = Order
    template_name = "orders/search_results_order.html"
    context_object_name = "orders"

    def get_queryset(self):
        query = self.request.GET.get("search_order")
        if self.request.user.username == "admin":
            if query:
                queryset = self.model.objects.all().filter(
                    Q(user__username__icontains=query)
                    | Q(created_at__icontains=query)
                    | Q(created_at__day__icontains=query)
                    | Q(created_at__month__icontains=query)
                    | Q(created_at__year__icontains=query)
                    | Q(done__icontains=query)
                )
                queryset = queryset.reverse()
                if query == " ":
                    queryset = self.model.objects.all()
                    queryset = queryset.reverse()
                return queryset
            return self.model.objects.none()
        else:
            user_orders = self.model.objects.filter(user=self.request.user)
            if query:
                queryset = user_orders.filter(
                    Q(user__username__icontains=query)
                    | Q(created_at__icontains=query)
                    | Q(created_at__day__icontains=query)
                    | Q(created_at__month__icontains=query)
                    | Q(created_at__year__icontains=query)
                    | Q(done__icontains=query)
                )
                queryset = queryset.reverse()
                if query == " ":
                    queryset = self.model.objects.filter(
                        user=self.request.user)
                    queryset = queryset.reverse()
                return queryset
            return self.model.objects.none()


class SortOrdersByNameView(GetContextDataMixin, ListView):
    title = _("Сортування за імям")
    paginate_by = 40
    model = Order
    template_name = "orders/sort_by_name.html"
    context_object_name = "orders"

    def get_queryset(self):
        user = self.kwargs.get('user')
        if self.request.user.username == "admin":
            if user:
                queryset = self.model.objects.all().filter(
                    Q(user__username__icontains=user))
                queryset = queryset.reverse()
                return queryset
            return self.model.objects.none()


class SortOrdersByDateView(GetContextDataMixin, ListView):
    title = _("Сортування за датою")
    paginate_by = 40
    model = Order
    template_name = "orders/sort_by_date.html"
    context_object_name = "orders"

    def get_queryset(self):
        created_at = self.kwargs.get('created_at')
        if self.request.user.username == "admin":
            if created_at:
                queryset = self.model.objects.all().filter(Q(created_at__icontains=created_at))
                queryset = queryset.reverse()
                return queryset
            return self.model.objects.none()
        else:
            if created_at:
                user_orders = self.model.objects.filter(user=self.request.user)
                queryset = user_orders.filter(
                    Q(created_at__icontains=created_at))
                queryset = queryset.reverse()
                return queryset
            return self.model.objects.none()


class SortOrdersByDoneView(GetContextDataMixin, ListView):
    title = _("Сортування за статусом")
    paginate_by = 40
    model = Order
    template_name = "orders/sort_by_done.html"
    context_object_name = "orders"

    def get_queryset(self):
        done = self.kwargs.get('done')
        if self.request.user.username == "admin":
            if done:
                queryset = self.model.objects.all().filter(done=done)
                queryset = queryset.reverse()
                return queryset
            return self.model.objects.none()
        else:
            if done:
                user_orders = self.model.objects.filter(user=self.request.user)
                queryset = user_orders.filter(done=done)
                queryset = queryset.reverse()
                return queryset
            return self.model.objects.none()


def pageNotFound(request, exception):
    return render(request, "404.html", status=404)
