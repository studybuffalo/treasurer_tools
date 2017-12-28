"""Main Site URL Conf"""
from django.conf.urls import url

from .views import (
    dashboard, request_payee_payers, add_payee_payer, edit_payee_payer,
    delete_payee_payer
)

# pylint: disable=invalid-name
urlpatterns = [
    url(r"^retrieve-payee-payer-list/$", request_payee_payers),
    url(r"^add-payee-payer/$", add_payee_payer, name="add_payee_payer"),
    url(r"^edit-payee-payer/(?P<id>\d+)$", edit_payee_payer, name="edit_payee_payer"),
    url(r"^delete-payee-payer/(?P<id>\d+)$", delete_payee_payer, name="delete_payee_payer"),
    url(r"^$", dashboard, name="payee_payer_dashboard"),
]
