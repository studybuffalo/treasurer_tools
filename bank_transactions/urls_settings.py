"""Expense Transaction URLs"""
from django.conf.urls import url

from .views_settings import (
    settings, institution_add, institution_edit, institution_delete
)

# pylint: disable=invalid-name
urlpatterns = [
    url(r"^institution/add$", institution_add, name="institution_add"),
    url(
        r"^institution/edit/(?P<institution_id>\d+)$",
        institution_edit,
        name="institution_edit"
    ),
    url(
        r"^institution/delete/(?P<institution_id>\d+)$",
        institution_delete,
        name="institution_delete"
    ),
    url(r"^$", settings, name="bank_settings"),
]