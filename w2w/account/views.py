from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic import FormView
import datetime
import uuid
from pathlib import Path
import os
import json
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import LoginForm, UserForm, VendorForm
from django.views.generic.edit import FormMixin
from django.utils.translation import gettext_lazy as _
from .utils import get_state_by_country_code_from_file
from .models import UserRegister, Vendor
from .auth import user_authenticate, user_login, user_logout, user_is_authenticated

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
                        messages.success(request, _("Login successful"))
                        return redirect("account:register_login")
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
                        vendor = Vendor(user=user, **vendor_form.cleaned_data)
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
