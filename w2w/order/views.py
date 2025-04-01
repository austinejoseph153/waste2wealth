# import all neccesary modules for to be used in this file
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.conf import settings
import requests
from w2w.account.auth import user_is_authenticated
from w2w.order.models import ShippingAddress
from w2w.product.forms import ShippingAddressForm
from w2w.product.models import Cart
from w2w.product.utils import delete_cart_items
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import SuspiciousOperation
from .utils import create_order_and_payment_instance_for_cartitems
from django.contrib import messages
import paystack
from .models import PaymentHistory, PaymentItem, OrderItem
from paystackease import PayStackBase, Currency, convert_to_subunit

paystack_client = PayStackBase()

"""
this function process orders and payment using paystack
"""
def stripe_payment_checkout(request):
    source_url = request.META.get("HTTP_REFERER")
    
    # verify if user ia authenticated, if not redirect them back to login page
    user = user_is_authenticated(request)
    if not user:
        messages.error(request, _("user is not Authenticated"))
        return redirect(source_url)
    
    shipping_form = ShippingAddressForm(request.POST)
    if shipping_form.is_valid():
        shipping_address = ShippingAddress(**shipping_form.cleaned_data)
        shipping_address.save()
    else:
        messages.error(request, _("shipping address form not valid"))
        return redirect(source_url)
    try:
        cart = Cart.objects.get(user=user)
        cart_items = cart.cartitem_set.filter(completed=False)
    except:
        messages.error(request, _("you do not have any items in cart"))
        return redirect(source_url)
    
    try:
        payment_request = create_order_and_payment_instance_for_cartitems(
            cartitems=cart_items,
            user=user,
            shipping_address=shipping_address
        )
    except ValidationError as e:
        messages.error(request, _(e.message))
        return redirect(source_url)
    
    # delete items in cart
    for item in cart_items:
        item.delete()
    
    success_url = 'http://127.0.0.1:8000' + reverse(
                    'order:stripe_payment_success', kwargs={'slug': payment_request.uuid}) + '?session_id={CHECKOUT_SESSION_ID}'
    cancel_url = 'http://127.0.0.1:8000' + reverse('order:process_order')
        
    metadata = {
            'mode':'payment',
            'client_reference_id': str(payment_request.uuid),
            'cancel_action': cancel_url,
            "customer_email": user.email,
    }
    # convert to kobo
    amount = convert_to_subunit(int(payment_request.subtotal), currency=Currency.NGN)
    try:
        # call the transaction instance and the initialize() method
        # to initialize or start a transaction.
        session = paystack_client.transactions.initialize(
            email=user.email, amount=amount, currency="NGN", callback_url=success_url,
            metadata=metadata, reference=str(payment_request.uuid)
        )
        request.session["client_ref"] = str(payment_request.uuid)
        return redirect(session.data["authorization_url"], code=301)
    except Exception as error:
        # send message of failure to the template
        messages.error(request, f"An error occurred {error}")
        return redirect(source_url)

def stripe_payment_success(request, slug):
    slug_field = 'uuid'
    payment_details = get_object_or_404(PaymentHistory, uuid=slug)
    o_id = OrderItem.objects.all()
    context = {}
    if request.GET.get('session_id'):
        try:
            context['paymentrequest'] = payment_details
            paymentrequestitem = PaymentItem.objects.filter(payment_history=payment_details)
            for item in paymentrequestitem:
                item.item.payment_status = item.item.PAID
                item.item.save()

            # change payment history to verified  
            payment_details.status = PaymentHistory.PAYMENT_VERIFIED
            payment_details.save()
            return render(request, "order/payment-success.html" ,context)
        except:
            context['customer'] = None
            context['session_stripe'] = None
            context['error_session'] = True
            return render(request, "order/payment-success.html", context)
    else:
        raise SuspiciousOperation(_("Bad request. Session required!"))
