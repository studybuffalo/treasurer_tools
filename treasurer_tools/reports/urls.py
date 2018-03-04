"""Main Site URL Conf"""
from django.conf.urls import url

from .views import (
    dashboard, balance_sheet_dashboard, account_summary_dashboard,
    retrieve_dates, retrieve_account_summary
)

# pylint: disable=invalid-name
urlpatterns = [
    url(r"balance-sheet/$", balance_sheet_dashboard, name="balance_sheet"),
    url(r"^account-summary/retrieve-dates/", retrieve_dates),
    url(r"^account-summary/retrieve-report/", retrieve_account_summary),
    url(r"^account-summary/$", account_summary_dashboard, name="account_summary"),
    url(r"^$", dashboard, name="dashboard"),
]
