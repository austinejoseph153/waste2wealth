from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import FormView
import datetime
from tempfile import NamedTemporaryFile
from django.core.files import File
import uuid
from pathlib import Path
import os
import json
import requests
from bs4 import BeautifulSoup
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormMixin
from django.utils.translation import gettext_lazy as _
from w2w.product.models import WasteCategory, Product
from w2w.account.models import Vendor
from w2w.account.auth import user_is_authenticated

base_dir = Path(__file__).parent.parent
base_dir = os.path.join(base_dir, "w2wpages/fixtures/")


class HomeTemplateView(TemplateView):
    template_name = "w2wpages/index.html"

    def render_to_response(self, context, **kwargs):
        response = super(HomeTemplateView, self).render_to_response(context, **kwargs)
        return response
    
    def get_context_data(self, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        context["waste_categories"] = WasteCategory.objects.all()
        context["user"] = user_is_authenticated(self.request)
        return context

class ContactTemplateView(TemplateView):
    template_name = "w2wpages/contact.html"

    def render_to_response(self, context, **kwargs):
        response = super(ContactTemplateView, self).render_to_response(context, **kwargs)
        return response
    
    def get_context_data(self, **kwargs):
        context = super(ContactTemplateView, self).get_context_data(**kwargs)
        context["user"] = user_is_authenticated(self.request)
        return context



# url = "https://waste2wealth.africa/product-category/animal-feedstock/"
# response = requests.get(url)
# soap = BeautifulSoup(response.content, "html.parser")
# products = soap.findAll("li", attrs={"class":"product"})

# datas = []
# if products:
#     for product in products:
#         data = {}
#         data["name"] = product.a.h2.text
#         data["category"] = "Animal Feedstock"
#         data["product_url"] = product.a["href"]
#         data["image_url"] = product.a.img["src"]
        
#         with open(base_dir+"products.json", "r") as file:
#             datas = json.load(file)
#         datas.append(data)
        
#         with open(base_dir+"products.json", "w") as file_2:
#             json.dump(datas, file_2, indent=6)
    

# data = requests.get("https://waste2wealth.africa/")
# soap = BeautifulSoup(data.content, "html.parser")
# categories = soap.findAll("h4", attrs={"class":"et_pb_module_header"})
# images = soap.findAll("img", attrs={"class":"et-waypoint"})
# tires_list = []
# for x,y in zip(images, categories):
#     data = {}
#     data["category"] =  y.span.text
#     data["image_url"] = x["src"]
#     tires_list.append(data)
# with open(base_dir+"waste-categories.json", "w") as file:
#     json.dump(tires_list, file, indent=6)

# https://waste2wealth.africa/product-category/biomass/
# https://waste2wealth.africa/product-category/soap-stock/
# https://waste2wealth.africa/product-category/fatty-acids/sludge/

# from tempfile import NamedTemporaryFile
# from django.core.files import File

# base_dir = str(Path(__file__).parent.parent)

# def load_waste_categories():
#     responses = []
#     count = 0
#     with open(base_dir+"waste-categories.json", "r") as file:
#         responses = json.loads(file.read())
#     for category in responses:
#         image_path = category["image_url"]
#         name = category["category"]
#         image_name = image_path.split("/")[-1]
#         count+=1
#         if not WasteCategory.objects.filter(category=name).exists():
#             try:
#                 image_file = requests.get(image_path)
#                 lf = NamedTemporaryFile(mode="w+b")
#                 lf.write(image_file.content)
#                 Tire_brand = WasteCategory(category=name)
#                 Tire_brand.image = File(lf, name=image_name)
#                 Tire_brand.save()
#             except:
#                 continue
#         print(count)
# load_waste_categories()

# def load_waste_products():
#     responses = []
#     count = 0
#     with open(base_dir+"products.json", "r") as file:
#         responses = json.loads(file.read())
#     for product in responses:
#         image_path = product["image_url"]
#         name = product["name"]
#         category = product["category"]
#         image_name = image_path.split("/")[-1]
#         count+=1
#         if not Product.objects.filter(name=name).exists():
#             # try:
#                 image_file = requests.get(image_path)
#                 lf = NamedTemporaryFile(mode="w+b")
#                 lf.write(image_file.content)
#                 category = WasteCategory.objects.get(category=category)
#                 vendor = Vendor.objects.get(pk=6)
#                 waste_product = Product(
#                             name=name, 
#                             category=category,
#                             description="""
#                                             Lorem ipsum dolor, sit amet consectetur adipisicing elit. 
#                                             Necessitatibus sed magnam perferendis soluta! Non error 
#                                             veniam nobis quas possimus omnis perspiciatis ex? Consequatur,
#                                             asperiores error. Dicta voluptatum dolor unde esse.
#                                         """,
#                             price=165,
#                             stock=1,
#                             weight=24.56,
#                             vendor=vendor

#                         )
#                 waste_product.image = File(lf, name=image_name)
#                 waste_product.save()
#             # except:
#             #     continue
#         print(count)
# load_waste_products()
