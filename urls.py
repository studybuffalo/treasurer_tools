"""Main Site URL Conf"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

# pylint: disable=invalid-name
urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^accounts/", include("allauth.urls")),
    url(r"^accounts/profile", TemplateView.as_view(template_name="account/profile.html"), name="account_profile"),
    url(r"^contact/$", TemplateView.as_view(template_name="account/profile.html"), name="contact"),
    url(r"^banking/", include("bank_transactions.urls")),
    url(r"^settings/banking/", include("bank_transactions.urls_settings")),
    url(r"^settings/codes/", include("financial_codes.urls")),
    url(r"^investments/", include("investments.urls")),
    url(r"^payee-payer/", include("payee_payer.urls")),
    url(r"^transactions/", include("transactions.urls")),
    url(r"^$", TemplateView.as_view(template_name="main/index.html"), name="home"),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
