from django.db import models
import datetime
from decimal import  Decimal
from django.utils.translation import gettext_lazy as _
from w2w.account.models import UserRegister, Vendor

class WasteCategory(models.Model):
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category/images")

    def __str__(self):
        return self.category
    
    class Meta:
        verbose_name = "waste categories"
        verbose_name_plural = "waste categories"

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Product Name"))
    description = models.TextField(verbose_name=_("Product Description"))
    category = models.ForeignKey(WasteCategory, on_delete=models.CASCADE, verbose_name=_("Product Category"))
    image = models.ImageField(upload_to="product/images", verbose_name=_("Product Image"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Product Price"))
    stock = models.IntegerField(verbose_name=_("Product Stock"))
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name=_("Product Vendor"))
    weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Product Weight"))

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE, verbose_name=_("Cart User"))
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" %(self.user.firstname, self.created_at)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name=_("Cart"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"))
    created_at = models.DateTimeField(default=datetime.datetime.now)
    completed = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1, verbose_name=_("Cart Items"))

    def calculate_amount(self):
        cost = self.product.price * Decimal(self.quantity)
        return cost
    
    def calculate_total(self):
        cost = self.calculate_amount()
        return cost

    def __str__(self):
        return "%s - %s" %(self.cart.user.firstname, self.product.name)