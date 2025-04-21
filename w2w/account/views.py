from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic import FormView
import datetime
import uuid
from django.db.models.functions import TruncMonth
from pathlib import Path
import os
from django.db.models import Sum, Count
import json
from django.http import HttpResponseNotAllowed, JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import LoginForm, UserForm, VendorForm
from django.views.generic.edit import FormMixin
from django.utils.translation import gettext_lazy as _
from .utils import get_state_by_country_code_from_file
from .models import UserRegister, Vendor
from .auth import user_authenticate, user_login, user_logout, user_is_authenticated
from w2w.product.models import Product
from w2w.order.models import OrderItem, PaymentItem, PaymentHistory
from w2w.product.forms import ProductForm

class LoginRegisterTemplateView(TemplateView):
    template_name = "account/login_register.html"

    def render_to_response(self, context, **kwargs):
        response = super(LoginRegisterTemplateView, self).render_to_response(context, **kwargs)
        return response
    
    def get_context_data(self, **kwargs):
        context = super(LoginRegisterTemplateView, self).get_context_data(**kwargs)
        context["login_form"] = LoginForm()
        context["user_form"] = UserForm()
        context["vendor_form"] = VendorForm()
        context["user"] = user_is_authenticated(self.request)
        context["states"] = get_state_by_country_code_from_file("NG")
        return context
    
    def post(self, request, **kwargs): 
        context = {}
        action = request.POST.get("action")
        if action == "login":
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = user_authenticate(request, login_form.cleaned_data['email'], login_form.cleaned_data['password'])
                if user:
                    if user.is_active:
                        user_login(request, user)
                        return redirect("account:user_dashboard")
                    else:
                        context["login_form"] = login_form
                        context["user_form"] = UserForm()
                        context["vendor_form"] = VendorForm()
                        messages.error(request,_("this account has been disabled from logging in"))    
                else:
                    context["login_form"] = login_form
                    context["user_form"] = UserForm()
                    context["vendor_form"] = VendorForm()
                    messages.error(request,_("Invalid Email or password!"))    
            else:
                context["login_form"] = login_form
                context["user_form"] = UserForm()
                context["vendor_form"] = VendorForm()
                messages.error(request,_("Invalid Email or password!"))
            return super(LoginRegisterTemplateView, self).render_to_response(context)
        else:
            user_form = UserForm(request.POST)
            vendor_form = VendorForm(request.POST)
            password_1 = request.POST.get("password")
            password_2 = request.POST.get("password_2")
            if password_1 != password_2:
                context["user_form"] = user_form
                context["vendor_form"] = vendor_form
                context["login_form"] = LoginForm()
                messages.error(request, _("passwords do not match!"))
                return super(LoginRegisterTemplateView, self).render_to_response(context)
            
            if user_form.is_valid():
                if UserRegister.objects.filter(email=user_form.cleaned_data["email"]).exists():
                    context["user_form"] = user_form
                    context["vendor_form"] = vendor_form
                    context["login_form"] = LoginForm()
                    messages.error(request, _("user with email already exists"))
                    return redirect("account:register_login")
                user = UserRegister(**user_form.cleaned_data)
                if request.POST.get("user_type") == "i_am_vendor":
                    if vendor_form.is_valid():
                        user.save()
                        vendor = Vendor(**vendor_form.cleaned_data)
                        vendor.user = user
                        vendor.save()
                        messages.success(request, _("Account created succesfully. login to your account"))
                        return redirect("account:register_login")
                    else:
                        context["user_form"] = user_form
                        context["vendor_form"] = vendor_form
                        context["login_form"] = LoginForm()
                        user.delete()
                        messages.error(request, _("invalid form data"))
                        return super(LoginRegisterTemplateView, self).render_to_response(context)
                else:
                    user.save()
                    messages.success(request, _("Account created succesfully. login to your account"))
                    return redirect("account:register_login")
            else:
                context["user_form"] = user_form
                context["vendor_form"] = vendor_form
                context["login_form"] = LoginForm()
                messages.error(request, _("invalid form data"))
                return super(LoginRegisterTemplateView, self).render_to_response(context)    

def logout(request):
    user_logout(request)
    messages.success(request, _('Logout was successful'))
    return redirect('account:register_login')

def delete_user_products(request, pk):
    user = user_is_authenticated(request)
    if user:
        product = Product.objects.get(pk=pk)
        vendor = Vendor.objects.get(user=user)
        
        if product.vendor != vendor:
            messages.error(request,"you do not have permission to delete this product")
            return redirect("account:user_products")
        
        product.delete()
        messages.success(request, "item deleted successfully")
        return redirect("account:user_products")
    else:
        pass 

def user_dashboard(request):
    user = user_is_authenticated(request)
    if user:
        context = {}
        context["user"] = user
        if Vendor.objects.filter(user=user).exists():
            vendor = Vendor.objects.get(user=user)
            context["vendor"] = vendor
        orders = OrderItem.objects.filter(order__buyer=user)
        total_orders = orders.count()
        total_revenue = orders.aggregate(Sum('sub_total'))['sub_total__sum']
        pending_orders = orders.filter(order_status='pending').count()
        processing_orders = orders.filter(order_status='processing').count()
        shipped_orders = orders.filter(order_status='shipped').count()
        delivered_orders = orders.filter(order_status='delivered').count()
        cancelled_orders = orders.filter(order_status='cancelled').count()

        payments = PaymentItem.objects.filter(payment_history__order__buyer=user)
        pending_payments = orders.filter(payment_status=OrderItem.PAID).count()
        paid_payments = orders.filter(payment_status=OrderItem.NOT_PAID).count()
        refunded_payments = orders.filter(payment_status=OrderItem.REFUNDED).count()
        
        total_payments = payments.aggregate(Sum('amount'))['amount__sum']
        

        context["total_orders"] = total_orders
        context["total_revenue"] = total_revenue
        context["pending_orders"] = pending_orders
        context["shipped_orders"] = shipped_orders
        context["delivered_orders"] = delivered_orders
        context["processing_orders"] = processing_orders
        context["cancelled_orders"] = cancelled_orders
        context["total_payments"] = total_payments
        context["pending_payments"] = pending_payments
        context["paid_payments"] = paid_payments
        context["refunded_payments"] = refunded_payments
        return render(request,"account/dashboard/index.html", context=context)
    else:
        return redirect("account:register_login")

def get_user_order_revenue(request):
    user = user_is_authenticated(request)
    if user:
        orders_by_month = OrderItem.objects.filter(order__buyer=user).annotate(
            month=TruncMonth('order__order_date')
            ).values('month').annotate(subtotal=Sum('sub_total')).order_by('month')

        order_data = []
        for order in orders_by_month:
            month_name = order['month'].strftime('%b')
            data = {
                'month': str(month_name),
                'revenue': int(order['subtotal'])
            }
            order_data.append(data)
        return JsonResponse({"order_data":order_data})

def user_profile(request):
    user = user_is_authenticated(request)
    if user:
        context = {}
        context["user"] = user
        if Vendor.objects.filter(user=user).exists():
            vendor = Vendor.objects.get(user=user)
            context["vendor"] = vendor
        return render(request,"account/dashboard/user_profile.html", context=context)
    else:
        return redirect("account:register_login")
    

def user_products(request):
    user = user_is_authenticated(request)
    if user:
        context = {}
        if Vendor.objects.filter(user=user).exists():
            vendor = Vendor.objects.get(user=user)
            user_products = Product.objects.filter(vendor=vendor).order_by("-id")
            context["user_products"] = user_products
            context["vendor"] = vendor
        context["user"] = user
        return render(request, "account/dashboard/user_products.html", context=context)
    else:
        return redirect("account:register_login")

def user_add_product(request):
    user = user_is_authenticated(request)
    if user:
        context = {}
        context["user"] = user
        
        # check if user is a vendor
        if Vendor.objects.filter(user=user).exists():
            vendor = Vendor.objects.get(user=user)
            context["vendor"] = vendor
        
        if request.method == "POST":
            form = ProductForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                if Product.objects.filter(name=form.cleaned_data.get("name")).exists():
                    messages.error(request, "product with name already exist!")
                    context["form"] = form
                    return render(request, "account/dashboard/add_product.html", context=context)
                product = Product(**form.cleaned_data)
                product.image = request.FILES.get("image")
                product.vendor = vendor
                product.save()
                messages.success(request,"Product added successfully")
                return redirect("account:user_products")
            else:        
                context["form"] = form
                messages.error(request, "an error with the form you submitted")
                return render(request, "account/dashboard/add_product.html", context=context)
        else: 
            context["form"] = ProductForm()
            return render(request, "account/dashboard/add_product.html", context=context)
    else:
        return redirect("account:register_login")


def user_orders(request):
    user = user_is_authenticated(request)
    if user:
        context = {}
        context["user"] = user
        order_items = OrderItem.objects.filter(order__buyer=user).order_by("-id")
        # check if user is a vendor
        if Vendor.objects.filter(user=user).exists():
            vendor = Vendor.objects.get(user=user)
            context["vendor"] = vendor
        context["order_items"] = order_items
        return render(request, "account/dashboard/order_items.html", context=context)
    else:
        return redirect("account:register_login")

def register_vendor(request):
    user = user_is_authenticated(request)
    if user:
        context = {}
        context["user"] = user
        context["states"] = get_state_by_country_code_from_file("NG")
        # check if user is a vendor
        if Vendor.objects.filter(user=user).exists():
            vendor = Vendor.objects.get(user=user)
            context["vendor"] = vendor
        if request.method == "POST":
            form = VendorForm(request.POST or None)
            if form.is_valid():
                if Vendor.objects.filter(shop_name=form.cleaned_data.get("shop_name")).exists():
                    messages.error(request, "Shop name already exist!")
                    context["form"] = form
                    return render(request, "account/dashboard/vendor_register.html", context=context)
                else:
                    vendor = Vendor(**form.cleaned_data)
                    vendor.save()
                    messages.success(request, "Registration successful")
                    return redirect("account:user_dashboard")
            else:
                context["form"] = form
                messages.error("invalid form data")
                return render(request, "account/dashboard/vendor_register.html", context=context)
        else:
            context["form"] = VendorForm()
            return render(request, "account/dashboard/vendor_register.html", context=context)
    else:
        return redirect("account:register_login")

# def user_products(request):
#     user = user_is_authenticated(request)
#     if user:
#         context = {}
#         context["user"] = user
#         return render(request, "account/dashboard/user_product.html")
#     else:
#         return redirect("account:login_register")