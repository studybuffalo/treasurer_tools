"""Main Site URL Conf"""
from django.conf.urls import url

from .views import (
    dashboard, request_payee_payers, add_payee_payer, edit_payee_payer,
    delete_payee_payer
)

# pylint: disable=invalid-name
urlpatterns = [
    url(r"^retrieve-payee-payer-list/$", request_payee_payers),
    url(r"^add/$", add_payee_payer, name="payee_payer_add"),
    url(r"^edit/(?P<id>\d+)$", edit_payee_payer, name="payee_payer_edit"),
    url(r"^delete/(?P<id>\d+)$", delete_payee_payer, name="payee_payer_delete"),
    url(r"^$", dashboard, name="payee_payer_dashboard"),
]
