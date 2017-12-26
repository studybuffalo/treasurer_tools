"""Financial Code URLs"""
from django.conf.urls import url

from .views import (
    dashboard, system_add, system_edit, system_delete, group_add, group_edit,
    group_delete, year_add, year_edit, year_delete, code_add, code_edit,
    code_delete,
)

# pylint: disable=invalid-name
urlpatterns = [
    url(r"^system/add", system_add, name="system_add"),
    url(r"^system/edit/(?P<id>\d+)$", system_edit, name="system_edit"),
    url(r"^system/delete/(?P<id>\d+)$", system_delete, name="system_delete"),
    url(r"^group/add", group_add, name="group_add"),
    url(r"^group/edit/(?P<id>\d+)$", group_edit, name="group_edit"),
    url(r"^group/delete/(?P<id>\d+)$", group_delete, name="group_delete"),
    url(r"^year/add", year_add, name="year_add"),
    url(r"^year/edit/(?P<id>\d+)$", year_edit, name="year_edit"),
    url(r"^year/delete/(?P<id>\d+)$", year_delete, name="year_delete"),
    url(r"^code/add", code_add, name="code_add"),
    url(r"^code/edit/(?P<id>\d+)$", code_edit, name="code_edit"),
    url(r"^code/delete/(?P<id>\d+)$", code_delete, name="code_delete"),
    url(r"^$", dashboard, name="financial_codes_dashboard"),
]
