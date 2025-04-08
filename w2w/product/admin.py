from django.contrib import admin
from .models import WasteCategory, Product, Cart, CartItem
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

@admin.register(WasteCategory)
class WasteCategoriesModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'category',)
    ordering = ["-id"]

@admin.register(Product)
class WasteProductModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'vendor', 'weight')
    ordering = ["-id"]
    actions = ["correspond_weight_with_availability"]

    def correspond_weight_with_availability(self, request, queryset):
        quantity = len(queryset)
        for obj in queryset:
            obj.available = int(obj.weight)
            obj.save()
        messages.success(request,_(f"Action completed successfully for {quantity} instances"))
    correspond_weight_with_availability.short_description = _("correspond available with weight")
    correspond_weight_with_availability.allowed_permissions = ('change',)



