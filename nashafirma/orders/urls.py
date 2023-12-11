from django.urls import path
from orders.views import (AddOrderView,
                          ViewOrderView,
                          AllOrdersView,
                          DeleteOrderView,
                          DeleteItemProductView,
                          EditItemProductView,
                          AddItemView,
                          SearchResultsOrderView,
                          EditOrderView)

urlpatterns = [
    path("add_order/", AddOrderView.as_view(), name="add_order"),
    path("view_order/<int:pk>/", ViewOrderView.as_view(), name="view_order"),
    path("all_orders/", AllOrdersView.as_view(), name="all_orders"),
    path("delete_order/<int:pk>/", DeleteOrderView.as_view(), name="delete_order"),
    path("delete_item_product/<int:pk>/", DeleteItemProductView.as_view(), name="delete_item_product"),
    path("edit_item_product/<int:pk>/", EditItemProductView.as_view(), name="edit_item_product"),
    path("edit_order/<int:pk>/", EditOrderView.as_view(), name="edit_order"),
    path("add_item/<int:pk>/", AddItemView.as_view(), name="add_item"),
    path("search_order/", SearchResultsOrderView.as_view(), name="search_results_order"),
]
