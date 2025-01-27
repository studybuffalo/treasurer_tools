"""Expense Transaction URLs"""
from django.urls import path

from .views import dashboard, add, edit, delete

app_name = "bank_institutions"

urlpatterns = [
    path('institution/add/', add, name="add"),
    path('institution/edit/<int:institution_id>', edit, name="edit"),
    path('institution/delete/<int:institution_id>', delete, name="delete"),
    path('', dashboard, name="dashboard"),
]
