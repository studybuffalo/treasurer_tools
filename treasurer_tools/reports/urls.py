"""Main Site URL Conf"""
from django.conf.urls import url

from .views import (
    dashboard, balance_sheet_dashboard, income_statement_dashboard,
    retrieve_dates, retrieve_income_statement
)

# pylint: disable=invalid-name
urlpatterns = [
    url(r"balance-sheet/$", balance_sheet_dashboard, name="balance_sheet"),
    url(r"^income-statement/retrieve-dates/", retrieve_dates),
    url(r"^income-statement/retrieve-report/", retrieve_income_statement),
    url(r"^income-statement/$", income_statement_dashboard, name="income_statement"),
    url(r"^$", dashboard, name="dashboard"),
]
