"""Main Site URL Conf"""
from django.conf.urls import include, url
from django.contrib import admin

from .views import dashboard, RequestPayeePayers, add_payee_payer

urlpatterns = [
    url(r"^retrieve-payee-payer-list/$", RequestPayeePayers.as_view()),
    url(r"^add-payee-payer/$", add_payee_payer, name="add_payee_payer"),
    url(r"^$", dashboard, name="payee_payer_dashboard"),
]
