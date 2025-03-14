from django.db import models
from w2w.account.models import UserRegister, Vendor
from w2w.product.models import Product
import uuid
from decimal import Decimal
from django.utils.translation import gettext_lazy as _

class ShippingAddress(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    country = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    order_description = models.TextField()

    def __str__(self):
        return "%s %s" %(self.lastname, self.firstname)
    
    class Meta:
        verbose_name = "shipping Address"
        verbose_name_plural = "Shipping Address"

class Order(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    buyer = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    seller = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    Shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" %(self.buyer.lastname, self.buyer.firstname)
    


class OrderItem(models.Model):
    ORDER_STATUS = (
        ("pending","Pending"),
        ("processing","Processing"),
        ("Shipped","Shipped"),
        ("Delivered","Delivered"),
        ("Cancelled","Cancelled"),
    )
    PAID = "paid"
    NOT_PAID = "not paid"
    REFUNDED = "refunded"
    PAYMENT_OPTIONS = (
        (PAID,"Paid"),
        (NOT_PAID,"Not Paid"),
        (REFUNDED,"Refunded"),
    )
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default="Pending")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_("Order"), null=True)
    quantity = models.PositiveIntegerField(default=1)
    payment_status = models.CharField(default=NOT_PAID, max_length=10, choices=PAYMENT_OPTIONS)
    sub_total = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal(0.0), verbose_name=_("Subtotal"),)
    delivery_date = models.DateField(verbose_name=_("Date Of Delivery"), blank=True, null=True)

class PaymentHistory(models.Model):
    CUR_NGN = 'NGN'
    CURRENCY_CHOICES = (
        (CUR_NGN, 'NGN'),
    )
    PAYMENT_STRIPE = 1
    PAYMENTREQUEST_TYPES_CHOICES = (
        (0, '-'),
        (PAYMENT_STRIPE, 'Stripe'),
    )
    PAYMENT_ACTIVE = 1
    PAYMENT_PENDING_VERIFICATION = 2
    PAYMENT_VERIFIED = 3
    PAYMENT_FAILED = 4
    PAYMENT_CANCELED = 5
    PAYMENT_STATUS_CHOICES = (
        (PAYMENT_ACTIVE, _("Active")),
        (PAYMENT_PENDING_VERIFICATION, _("Pending verification")),
        (PAYMENT_VERIFIED, _("Verified")),
        (PAYMENT_FAILED, _("Failed")),
        (PAYMENT_CANCELED, _("Canceled"))
    )
    uuid = models.UUIDField(unique=True)
    slug = models.SlugField(unique=True, max_length=300)
    status = models.PositiveIntegerField(choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_ACTIVE, verbose_name=_("Status"))
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=CUR_NGN)
    order = models.ForeignKey(Order, verbose_name=_("Default Oder"), on_delete=models.CASCADE)
    description = models.TextField(verbose_name=_("Description"), help_text=_("will only display the first 127 chars."), blank=True, null=True)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal(0.0), verbose_name=_("Subtotal"), help_text=_("Automatic if payment requests items"))
    transaction_fee = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(0.0), blank=True, verbose_name=_("Stripe transaction fee"))
    automatic_fee = models.BooleanField(default=False, verbose_name=_("Automatic calculation of the  or Stripe transaction fee"))
    payment_type = models.PositiveIntegerField(choices=PAYMENTREQUEST_TYPES_CHOICES, default="Stripe",  verbose_name=_("Payment type"))
    payment_date = models.DateTimeField(blank=True, null=True, verbose_name=_("Payment date"))

class PaymentItem(models.Model):
    payment_history = models.ForeignKey(PaymentHistory, on_delete=models.CASCADE)
    item = models.ForeignKey(OrderItem, blank=True, null=True, verbose_name=_("product ordered"), on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_('Amount'))
