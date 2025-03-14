from django import forms
from django.utils.translation import gettext_lazy as _

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

class UserForm(forms.Form):
    firstname = forms.CharField(label=_('First Name'), widget=forms.TextInput(attrs={'class':'form-control'}))
    lastname = forms.CharField(label=_('Last Name'), widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label=_('Email'), widget=forms.EmailInput(attrs={'class':'form-control'}))
    phone = forms.CharField(label=_('Phone'), widget=forms.TextInput(attrs={'class':'form-control', "placeholder":"+234 9078645372"}))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={"class":"form-control"}))
    
class VendorForm(forms.Form):
    # shop informations
    shop_name = forms.CharField(required=False, label=_('Shop Name'), widget=forms.TextInput(attrs={'class':'form-control'}))
    shop_state = forms.CharField(required=False, label=_('Shop State'), widget=forms.TextInput(attrs={'class':'form-control'}))
    shop_city = forms.CharField(required=False, label=_('Shop City'), widget=forms.TextInput(attrs={'class':'form-control'}))
    shop_address = forms.CharField(required=False, label=_('Shop Address'), widget=forms.TextInput(attrs={'class':'form-control'}))

    