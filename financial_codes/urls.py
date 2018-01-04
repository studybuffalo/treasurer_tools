"""Financial Code URLs"""
from django.conf.urls import url

from . import views

# pylint: disable=invalid-name
urlpatterns = [
    url(r"^system/add/", views.system_add, name="financial_code_system_add"),
    url(r"^system/edit/(?P<system_id>\d+)$", views.system_edit, name="financial_code_system_edit"),
    url(r"^system/delete/(?P<system_id>\d+)$", views.system_delete, name="financial_code_system_delete"),
    url(r"^group/add/", views.group_add, name="group_add"),
    url(r"^group/edit/(?P<group_id>\d+)$", views.group_edit, name="group_edit"),
    url(r"^group/delete/(?P<group_id>\d+)$", views.group_delete, name="group_delete"),
    url(r"^year/add/", views.year_add, name="year_add"),
    url(r"^year/edit/(?P<year_id>\d+)$", views.year_edit, name="year_edit"),
    url(r"^year/delete/(?P<year_id>\d+)$", views.year_delete, name="year_delete"),
    url(r"^code/add/", views.code_add, name="code_add"),
    url(r"^code/edit/(?P<code_id>\d+)$", views.code_edit, name="code_edit"),
    url(r"^code/delete/(?P<code_id>\d+)$", views.code_delete, name="code_delete"),
    url(r"^$", views.dashboard, name="financial_codes_dashboard"),
]
