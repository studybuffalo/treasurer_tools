"""Expense Transaction URLs"""
from django.conf.urls import url

from .views import (
    dashboard, investment_add, investment_edit, investment_delete,
    detail_add, detail_edit, detail_delete,
)

app_name = "investments"

urlpatterns = [
    url(r"^add/$", investment_add, name="investment_add"),
    url(r"^edit/(?P<investment_id>\d+)/$", investment_edit, name="investment_edit"),
    url(r"^delete/(?P<investment_id>\d+)/$", investment_delete, name="investment_delete"),
    url(r"^detail/add/(?P<investment_id>\d+)/$", detail_add, name="detail_add"),
    url(r"^detail/edit/(?P<detail_id>\d+)/$", detail_edit, name="detail_edit"),
    url(r"^detail/delete/(?P<detail_id>\d+)/$", detail_delete, name="detail_delete"),
    url(r"^$", dashboard, name="dashboard"),
]
