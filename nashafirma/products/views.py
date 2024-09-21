from django.utils.translation import gettext as _

from utils.utils import GetContextDataMixin
from .models import Product
from .forms import ProductForm
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect

from django.db.models import Q


class AddProductView(GetContextDataMixin, CreateView):
    title = _("Додати новий продукт")
    form_class = ProductForm
    template_name = "products/add_product.html"
    success_url = reverse_lazy("all_products")


class AllProductsView(GetContextDataMixin, ListView):
    title = _("Всі продукти")
    paginate_by = 40
    model = Product
    template_name = "products/all_products.html"
    context_object_name = "products"


class DeleteProductView(GetContextDataMixin, DeleteView):
    title = _("Видалити продукт")
    model = Product
    template_name = "products/delete_product.html"
    success_url = reverse_lazy("all_products")

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('all_products')


class EditProductView(GetContextDataMixin, UpdateView):
    title = _("Змінити продукт")
    model = Product
    fields = ["product", "price"]
    template_name = "products/edit_product.html"

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('all_products')


class SearchResultsProductView(GetContextDataMixin, ListView):
    title = _("Результати пошуку продукту")
    paginate_by = 40
    model = Product
    template_name = "products/search_results_product.html"
    context_object_name = "products"

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('search_product')

    def get_queryset(self):
        query = self.request.GET.get("search_product")
        if query:
            queryset = self.model.objects.filter(
                Q(product__icontains=query) |
                Q(price__icontains=query)
            )
            if query == " " or query == "":
                queryset = self.model.objects.all()
            return queryset
        return self.model.objects.none()
