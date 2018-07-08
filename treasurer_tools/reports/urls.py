"""Main Site URL Conf"""
from django.urls import path

from .views import (
    dashboard, balance_sheet_dashboard, income_statement_dashboard,
    retrieve_income_statement
)

app_name = "reports"

urlpatterns = [
    path("balance-sheet/", balance_sheet_dashboard, name="balance_sheet"),
    path("balance-sheet/retrieve-report", retrieve_balance_sheet),
    path("income-statement/retrieve-report/", retrieve_income_statement),
    path("income-statement/", income_statement_dashboard, name="income_statement"),
    path("", dashboard, name="dashboard"),
]
