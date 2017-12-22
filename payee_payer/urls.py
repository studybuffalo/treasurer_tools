"""Main Site URL Conf"""
from django.conf.urls import include, url
from django.contrib import admin

from .views import dashboard, RequestPayeePayers

urlpatterns = [
    url(r"^retrieve-payee-payer-list/$", RequestPayeePayers.as_view()),
    url(r"^$", dashboard, name="payee_payer_dashboard"),
]
