from django.urls import path
from .views import (HomeTemplateView, ContactTemplateView)
app_name = "pages"

urlpatterns = [
    path("", HomeTemplateView.as_view(), name="home"),
    path("contact/", ContactTemplateView.as_view(), name="contact"),
]