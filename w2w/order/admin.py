from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem, PaymentHistory, PaymentItem

class PaymentRequestItemInline(admin.TabularInline):
    model = PaymentItem
    extra = 0

@admin.register(PaymentHistory)
class PaymentHistoryModelAdmin(admin.ModelAdmin):

    list_display = ('pk', 'uuid', 'payment_type', 'status', 'subtotal',)                    
    readonly_fields = ('uuid', 'payment_date',)

    inlines = [
        PaymentRequestItemInline
    ]

@admin.register(PaymentItem)
class PaymentItemModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount']


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'order_date']

@admin.register(OrderItem)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'sub_total', 'order_status']