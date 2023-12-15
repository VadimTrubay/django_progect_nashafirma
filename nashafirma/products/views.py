from .models import Product
from .forms import ProductForm
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect

from django.db.models import Q


class AddProductView(CreateView):
    title = "Додати новий продукт"
    form_class = ProductForm
    template_name = "products/add_product.html"
    success_url = reverse_lazy("all_products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class AllProductsView(ListView):
    title = "Всі продукти"
    paginate_by = 5
    model = Product
    template_name = "products/all_products.html"
    context_object_name = "products"
    # ordering = 'product'

    # def get_queryset(self):
    #     return self.model.objects.order_by(self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class DeleteProductView(DeleteView):
    title = "Видалити продукт"
    model = Product
    template_name = "products/delete_product.html"
    success_url = reverse_lazy("all_products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class EditProductView(UpdateView):
    title = "Редагувати продукт"
    model = Product
    fields = ["product", "price"]
    template_name = "products/edit_product.html"

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        print(next_url)
        if next_url:
            return next_url
        else:
            return reverse_lazy('all_products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class SearchResultsProductView(ListView):
    title = "Результати пошуку продукту"
    model = Product
    template_name = "products/search_results_product.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def get_queryset(self):
        query = self.request.GET.get("search_product")
        if query:
            queryset = self.model.objects.filter(
                Q(product__icontains=query) |
                Q(price__icontains=query)
            )
            if query == " ":
                queryset = self.model.objects.all()
            return queryset
        return self.model.objects.none()
