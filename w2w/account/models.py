from django.db import models
from django.utils.translation import gettext_lazy as _

class UserRegister(models.Model):
    firstname = models.CharField(max_length=100, verbose_name=_("First Name"))
    lastname = models.CharField(max_length=100, verbose_name=_("Last Name"))
    email = models.EmailField(verbose_name=_("Email"))
    phone = models.CharField(max_length=15, verbose_name=_("Phone"))
    password = models.CharField(max_length=20, verbose_name=_("Password"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    
    def __str__(self):
        return "%s - %s" %(self.lastname, self.firstname)
    
    class Meta:
        verbose_name= "Registered Users"
        verbose_name_plural = "Registered Users"
        ordering = ["-id"]

class Vendor(models.Model):
    user = models.OneToOneField(UserRegister, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100, verbose_name=_("Vendor Shop Name"))
    shop_state = models.CharField(max_length=100, verbose_name=_("Vendor Shop State"))
    shop_city = models.CharField(max_length=100, verbose_name=_("Vendor Shop City"))
    shop_address = models.CharField(max_length=100, verbose_name=_("Vendor Shop Address"))

    def __str__(self):
        return "%s - %s" %(self.user.lastname, self.shop_name)