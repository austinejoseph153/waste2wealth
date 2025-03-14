from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from w2w.product.models import Product, Cart, CartItem
from .utils import get_cartitem_total_cost
from django.http import HttpResponseNotAllowed, JsonResponse
from w2w.account.auth import user_is_authenticated
from .forms import ShippingAddressForm
from w2w.account.utils import get_countries_from_file, get_state_by_country_code_from_file

class ProductListTemplateView(ListView):
    model = Product
    template_name = "product/waste-product-list.html"
    
    def get_queryset(self):
        queryset = super(ProductListTemplateView, self).get_queryset()
        category = self.request.GET.get("category")
        if category:
            return queryset.filter(category__category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductListTemplateView, self).get_context_data(**kwargs)
        return context

def cart_page_view(request):
    if request.method == "GET":
        context = {}
        user = user_is_authenticated(request)
        cart_items = []
        if user:
            try:
                cart = Cart.objects.get(user=user)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(user=user) 
            if CartItem.objects.filter(cart=cart).exists():
                cart_items = CartItem.objects.filter(cart=cart).order_by("-id")
                total_cost = get_cartitem_total_cost(cart_items)
                context["cart_id"] = cart.pk
                context["sub_total"] = total_cost["sub_total"]
                context["total_quantity"] = sum([x.quantity for x in cart_items])
            context["cart_items"] = cart_items
            return render(request, "cart/cart.html", context)
        else:
            return redirect("account:register_login")
    else:
        return HttpResponseNotAllowed(["GET"])

def add_to_cart(request, product_id):
    if request.method == "GET":
        product = Product.objects.get(pk=product_id)
        quantity = int(request.GET.get("quantity", 1))
        user = user_is_authenticated(request)
        if user:
            try:
                cart = Cart.objects.get(user=user)
            except:
                cart = Cart.objects.create(user=user)

            try:
                cart_item = CartItem.objects.get(cart=cart, product=product)
                cart_item.quantity += quantity
                cart_item.save()
            except CartItem.DoesNotExist:
                cart_item = CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=quantity,
                )
                cart_item.save()
            messages.success(request,_("item added to cart"))
            return redirect("product:cart_page")
        else:
            return redirect("account:register_login")            
    else:
        return HttpResponseNotAllowed(['GET'])

def delete_item_from_cart(request, pk):
    try:
        cart_item = CartItem.objects.get(pk=pk)
    except CartItem.DoesNotExist:
        messages.error(request, _("cart item does not exist"))
    else:
        cart_item.delete()
    messages.success(request,_("one item successfully deleted from cart"))
    return redirect("product:cart_page")


def update_cart(request):
    if request.method == "POST":
        cart_id = request.POST.get("cart_id")
        count = int(request.POST.get("count"))
        try:
            cart_item = CartItem.objects.get(pk=cart_id)
        except CartItem.DoesNotExist:
            return JsonResponse({"message":"cart item not found"}, status=404)
        else:
            cart_item.quantity = count
            cart_item.save()
            cart_items = CartItem.objects.filter(cart=cart_item.cart, completed=False)
            total_cost = get_cartitem_total_cost(cart_items)
            return JsonResponse({"message":"update successful",
                                "count":cart_item.quantity,
                                "single_subtotal":cart_item.calculate_amount(),
                                "single_total":cart_item.calculate_total(),
                                "cart_total_quantity":total_cost["quantity"],
                                "cart_sub_total":total_cost["sub_total"],
                             }, status=200)
    else:
        return JsonResponse({"message":"an error occured"}, status=405)
    
def checkout(request):
    user = user_is_authenticated(request)
    if user:
        context = {}
        shipping_form = ShippingAddressForm()
        cartitems = CartItem.objects.filter(cart__user=user)
        if not cartitems:
            messages.warning(request, _("cart is empty"))
            return redirect("product:products")
        cart_summary = get_cartitem_total_cost(cartitems)
        context["cart_summary"] = cart_summary
        context["shipping_form"] = shipping_form
        context["countries"] = get_countries_from_file()
        context["states"] = get_state_by_country_code_from_file("NG")
        context["cart_items"] = cartitems
        return render(request,"cart/checkout.html",context=context)
    else:
        pass

def empty_cart(request, cart_id):
    cart = Cart.objects.get(pk=cart_id)
    cart_items = cart.cartitem_set.filter(cart=cart, completed=False).delete()
    messages.success(request, _("Cart items successfully deleted"))
    return redirect("product:cart_page")

def get_states(request):
    country_code = request.GET.get("country_code", None)
    states = get_state_by_country_code_from_file(country_code)
    return JsonResponse({"states":states})

