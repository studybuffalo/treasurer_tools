"""Financial Code URLs"""
from django.urls import path

from . import views

app_name = "financial_codes"

urlpatterns = [
    path('system/add/', views.system_add, name="system_add"),
    path('system/edit/<int:system_id>/', views.system_edit, name="system_edit"),
    path('system/delete/<int:system_id>/', views.system_delete, name="system_delete"),
    path('group/add/', views.group_add, name="group_add"),
    path('group/edit/<int:group_id>/', views.group_edit, name="group_edit"),
    path('group/delete/<int:group_id>/', views.group_delete, name="group_delete"),
    path('year/add/', views.year_add, name="year_add"),
    path('year/edit/<int:year_id>/', views.year_edit, name="year_edit"),
    path('year/delete/<int:year_id>/', views.year_delete, name="year_delete"),
    path('year/copy/<int:year_id>/', views.year_copy, name="year_copy"),
    path('code/add/', views.code_add, name="code_add"),
    path('code/edit/<int:code_id>/', views.code_edit, name="code_edit"),
    path('code/delete/<int:code_id>/', views.code_delete, name="code_delete"),
    path('', views.dashboard, name="dashboard"),
]
