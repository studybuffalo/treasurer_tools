"""Expense Transaction URLs"""
from django.urls import path

from .views import (
    dashboard, investment_add, investment_edit, investment_delete,
    detail_add, detail_edit, detail_delete,
)

app_name = "investments"

urlpatterns = [
    path('add/', investment_add, name="investment_add"),
    path('edit/<int:investment_id>/', investment_edit, name="investment_edit"),
    path('delete/<int:investment_id>/', investment_delete, name="investment_delete"),
    path('detail/add/<int:investment_id>/', detail_add, name="detail_add"),
    path('detail/edit/<int:detail_id>/', detail_edit, name="detail_edit"),
    path('detail/delete/<int:detail_id>/', detail_delete, name="detail_delete"),
    path('', dashboard, name="dashboard"),
]
