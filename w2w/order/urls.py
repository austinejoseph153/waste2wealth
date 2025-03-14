from django.urls import path
from .views import stripe_payment_checkout, stripe_payment_success


app_name = "order"

urlpatterns = [
    path("process_order/", stripe_payment_checkout, name="process_order"),
    path("payment/stripe/<uuid:slug>/success/", stripe_payment_success, name="stripe_payment_success"),
]