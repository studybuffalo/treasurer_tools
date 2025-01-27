"""Main Site URL Conf"""
from django.urls import path

from .views import (
    dashboard, request_payee_payers, add_payee_payer, edit_payee_payer,
    delete_payee_payer
)

app_name = "payee_payers"

urlpatterns = [
    path('retrieve-payee-payer-list/', request_payee_payers),
    path('add/', add_payee_payer, name="add"),
    path('edit/<int:payee_payer_id>/', edit_payee_payer, name="edit"),
    path('delete/<int:payee_payer_id>/', delete_payee_payer, name="delete"),
    path('', dashboard, name="dashboard"),
]
