"""Main Site URL Conf"""
from django.conf.urls import url

from .views import (
    dashboard, request_payee_payers, add_payee_payer, edit_payee_payer,
    delete_payee_payer
)

# pylint: disable=invalid-name
urlpatterns = [
    url(r"^retrieve-payee-payer-list/$", request_payee_payers),
    url(r"^add/$", add_payee_payer, name="add"),
    url(r"^edit/(?P<payee_payer_id>\d+)$", edit_payee_payer, name="edit"),
    url(r"^delete/(?P<payee_payer_id>\d+)$", delete_payee_payer, name="delete"),
    url(r"^$", dashboard, name="dashboard"),
]
