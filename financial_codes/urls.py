"""Financial Code URLs"""
from django.conf.urls import url

from .views import (
    dashboard, system_add, system_edit, system_delete
)

# pylint: disable=invalid-name
urlpatterns = [
    url(r"^system/add", system_add, name="system_add"),
    url(r"^system/edit/(?P<id>\d+)$", system_edit, name="system_edit"),
    url(r"^system/delete/(?P<id>\d+)$", system_delete, name="system_delete"),
    url(r"^year/add", system_add, name="year_add"),
    url(r"^group/add", system_add, name="group_add"),
    url(r"^code/add", system_add, name="code_add"),
    url(r"^$", dashboard, name="financial_codes_dashboard"),
]
