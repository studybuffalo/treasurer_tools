"""Main Site URL Conf"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^accounts/", include("allauth.urls")),
    url(r"^accounts/profile", TemplateView.as_view(template_name="account/profile.html"), name="account_profile"),
    url(r"^$", TemplateView.as_view(template_name="main/index.html")),
]
