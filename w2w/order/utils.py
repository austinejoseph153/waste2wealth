from .models import Order, OrderItem, PaymentHistory, PaymentItem
from w2w.product.models import Cart, CartItem
from w2w.account.models import Vendor
from decimal import Decimal
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

def create_order_and_payment_instance_for_cartitems(cartitems, user, shipping_address):
    """
    @param
    cart_items
    user
    shipping_info
    """

    order_total = Decimal(0.0)
    # create an order instance to be used to create order items
    try:
        order = Order(
            Shipping_address=shipping_address,
            buyer=user,
        )
        order.save()
    except:
        print("order")
        raise ValidationError(_("sorry the server was unable to process your request!"))
    
    # loop through each cartitems and create order items respectively
    try:
        for cartitem in cartitems:
            order_item = OrderItem(
                order=order,
                product=cartitem.product,
                quantity=cartitem.quantity,
                seller=cartitem.product.vendor,
                sub_total=cartitem.calculate_total()
            )
            order_item.save()
            order_total+=order_item.sub_total
    except:
        print("orderitem")
        raise ValidationError(_("sorry the server was unable to process your request!"))
    
    # create payment history instance
    try:
        payment_history = PaymentHistory.objects.create(
            uuid=order.uuid,
            slug=order.uuid,
            payment_type=PaymentHistory.PAYMENT_STRIPE,
            order=order,
            subtotal=order_total,
            description=order.Shipping_address.order_description,
        )
    except:
        print("paymenthistory")
        raise ValidationError(_("sorry the server was unable to process your request!"))
    try:
        for orderitem in order.orderitem_set.all():        
            payment_order_item = PaymentItem.objects.create(
                payment_history=payment_history,
                item=orderitem,
                amount=orderitem.sub_total
            )
            payment_order_item.save()
    except:
        print("paymenitem")
        raise ValidationError(_("sorry the server was unable to process your request!"))
    return payment_history

