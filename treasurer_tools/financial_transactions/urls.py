"""Expense Transaction URLs"""
from django.urls import path, re_path

from .views import (
    dashboard, request_transactions_list, transaction_add,
    transaction_edit, transaction_delete, transaction_pdf,
)

app_name = "financial_transactions"

urlpatterns = [
    re_path(r'(?P<t_type>(expense|revenue))/add/$', transaction_add, name="add",),
    re_path(r'^(?P<t_type>(expense|revenue))/edit/(?P<transaction_id>\d+)/$', transaction_edit, name="edit",),
    re_path(r'^(?P<t_type>(expense|revenue))/delete/(?P<transaction_id>\d+)/$', transaction_delete, name="delete",),
    path('pdf/<int:transaction_id>/', transaction_pdf, name="pdf",),
    path('retrieve-transactions/', request_transactions_list),
    path('', dashboard, name="dashboard"),
]
