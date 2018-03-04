"""Main Site URL Conf"""
from django.conf.urls import url

from .views import dashboard

# pylint: disable=invalid-name
urlpatterns = [
    url(r"^$", dashboard, name="dashboard"),
]
