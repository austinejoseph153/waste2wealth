from django.urls import path
from .views import (LoginRegisterTemplateView, user_dashboard, 
                    logout, user_products, user_orders, user_profile, get_user_order_revenue,
                    user_add_product, register_vendor, delete_user_products)
app_name = "account"

urlpatterns = [
    path("account/register-login/", view=LoginRegisterTemplateView.as_view(), name="register_login"),
    path("user/dashboard/", view=user_dashboard, name="user_dashboard"),
    path("user/profile/", view=user_profile, name="user_profile"),
    path("user/products/", view=user_products, name="user_products"),
    path("user/orders/", view=user_orders, name="user_orders"),
    path("user/revenue/", view=get_user_order_revenue, name="user_revenue"),
    path("user/add/product/", view=user_add_product, name="user_add_product"),
    path("vendor/register/", view=register_vendor, name="vendor_register"),
    path("delete/user/product/<int:pk>/", view=delete_user_products, name="delete_user_product"),
    path("logout/", view=logout, name="logout"),
]