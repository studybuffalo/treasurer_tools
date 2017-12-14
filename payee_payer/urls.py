"""Main Site URL Conf"""
from django.conf.urls import include, url
from django.contrib import admin

from .views import dashboard

urlpatterns = [
    url(r"^$", dashboard, name="payee_payer_dashboard"),
]
