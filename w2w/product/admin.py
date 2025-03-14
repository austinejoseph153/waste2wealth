from django.contrib import admin
from .models import WasteCategory, Product, Cart, CartItem

@admin.register(WasteCategory)
class WasteCategoriesModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'category',)
    ordering = ["-id"]

@admin.register(Product)
class WasteProductModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'stock', 'vendor', 'weight')
    ordering = ["-id"]


