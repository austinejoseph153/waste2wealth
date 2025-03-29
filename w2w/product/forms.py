from django import forms
from django.utils.translation import gettext_lazy as _
from .models import WasteCategory

class ShippingAddressForm(forms.Form):
    firstname = forms.CharField(max_length=100, label=_("First Name"), widget=forms.TextInput(attrs={"class": "form-control"}))
    lastname = forms.CharField(max_length=100, label=_("Last Name"), widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label=_("Email"), widget=forms.EmailInput(attrs={"class": "form-control"}))
    phone = forms.CharField(max_length=15, label=_("Phone"), widget=forms.TextInput(attrs={"class": "form-control"}))
    country = forms.CharField(max_length=100, label=_("Country"), widget=forms.TextInput(attrs={"class": "form-control"}))
    state = forms.CharField(max_length=100, label=_("State"), widget=forms.TextInput(attrs={"class": "form-control"}))
    city = forms.CharField(max_length=100, label=_("City"), widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(max_length=500, label=_("Address"), widget=forms.TextInput(attrs={"class": "form-control"}))
    order_description = forms.CharField(max_length=500, label=_("Order Description"), widget=forms.Textarea(attrs={"class": "form-control", "rows":"3", "cols":"6"}))

class ProductForm(forms.Form):
    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={"class":"form-control"}))
    description = forms.CharField(label="Description", widget=forms.TextInput(attrs={"class":"form-control"}))
    category = forms.ModelChoiceField(empty_label="Category", queryset=WasteCategory.objects.all(), widget=forms.Select(attrs={"class":"form-select"}))
    image = forms.ImageField()
    price = forms.DecimalField(label="Price", widget=forms.NumberInput(attrs={"class":"form-control"}))
    stock = forms.IntegerField(label="Quantity", widget=forms.NumberInput(attrs={"class":"form-control"}))
    weight = forms.DecimalField(label="Weight", widget=forms.NumberInput(attrs={"class":"form-control"}))
