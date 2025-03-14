from django.urls import path
from .views import (LoginRegisterTemplateView)
app_name = "account"

urlpatterns = [
    path("account/register-login/", LoginRegisterTemplateView.as_view(), name="register_login"),
]