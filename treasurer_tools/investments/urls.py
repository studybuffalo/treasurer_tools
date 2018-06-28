"""Expense Transaction URLs"""
from django.conf.urls import url

from .views import (
    dashboard, investment_add, investment_edit, investment_delete
)

app_name = "investments"

urlpatterns = [
    url(r"^add/$", investment_add, name="add"),
    url(r"^edit/(?P<investment_id>\d+)$", investment_edit, name="edit"),
    url(r"^delete/(?P<investment_id>\d+)$", investment_delete, name="delete"),
    url(r"^$", dashboard, name="dashboard"),
]
