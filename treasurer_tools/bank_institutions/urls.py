"""Expense Transaction URLs"""
from django.conf.urls import url

from .views import dashboard, add, edit, delete

# pylint: disable=invalid-name
urlpatterns = [
    url(r"^institution/add/$", add, name="add"),
    url(r"^institution/edit/(?P<institution_id>\d+)$", edit, name="edit"),
    url(r"^institution/delete/(?P<institution_id>\d+)$", delete, name="delete"),
    url(r"^$", dashboard, name="dashboard"),
]
