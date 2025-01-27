"""Expense Transaction URLs"""
from django.urls import path

from .views import (
    dashboard, statement_add, statement_edit, statement_delete
)

app_name = "bank_transactions"

urlpatterns = [
    path('statement/add/', statement_add, name="add"),
    path('statement/edit/<int:statement_id>', statement_edit, name="edit"),
    path('statement/delete/<int:statement_id>', statement_delete, name="delete"),
    path('', dashboard, name="dashboard"),
]
