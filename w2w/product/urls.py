from django.urls import path
from .views import (
    ProductListTemplateView,
    cart_page_view,
    update_cart, empty_cart,
    add_to_cart, get_states,
    delete_item_from_cart, checkout
)

app_name = "product"

urlpatterns = [
    path("products/", ProductListTemplateView.as_view(), name="products"),
    path("cartitems/", cart_page_view, name="cart_page"),
    path("update-cart/", view=update_cart, name="update_cart"),
    path("add-to-cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart-delete/item/<int:pk>/", view=delete_item_from_cart, name="delete_cart_item"),
    path("checkout/", view=checkout, name="checkout"),
    path("empty-cart/<int:cart_id>/", view=empty_cart, name="empty_cart"),
    path('get/states/', view=get_states, name="get_states"),
]