from django.urls import path
from .views import AddProductView, SearchResultsProductView, AllProductsView, DeleteProductView, EditProductView

urlpatterns = [
    path("add_product/", AddProductView.as_view(), name="add_product"),
    path("all_products/", AllProductsView.as_view(), name="all_products"),
    path("delete_product/<int:pk>/", DeleteProductView.as_view(), name="delete_product"),
    path("edit_product/<int:pk>/", EditProductView.as_view(), name="edit_product"),
    path("search_product/", SearchResultsProductView.as_view(), name="search_results_product"),
]
