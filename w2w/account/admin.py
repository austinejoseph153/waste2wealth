from django.contrib import admin
from .models import UserRegister, Vendor

@admin.register(UserRegister)
class UserRegisterModelAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Customer Info", {
            'fields': (
                ('firstname', 'lastname', 'email', 'phone', 'is_active'),
                ('password'),
            ),
        }),
    )

    list_display = ('id', 'firstname', 'lastname', 'email', 'phone',)

@admin.register(Vendor)
class VendorModelAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                ('shop_name', 'shop_state',),
                ('shop_city','shop_address',),
            ),
        }),
    )

    list_display = ('id', 'user', 'shop_name', 'shop_state', 'shop_city')
    
