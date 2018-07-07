"""Main Site URL Conf"""
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views import defaults as default_views
from django.views.generic import TemplateView


urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("accounts/profile/", TemplateView.as_view(template_name="account/profile.html"), name="account_profile"),
    path("admin/", admin.site.urls),
    path("contact/", TemplateView.as_view(template_name="account/profile.html"), name="contact"),
    path("banking/", include("bank_transactions.urls", namespace="bank_transactions")),
    path("banking/reconciliation/", include("bank_reconciliation.urls", namespace="bank_reconciliation")),
    path("settings/banking/", include("bank_institutions.urls", namespace="bank_institutions")),
    path("settings/codes/", include("financial_codes.urls", namespace="financial_codes")),
    path("investments/", include("investments.urls", namespace="investments")),
    path("payee-payer/", include("payee_payers.urls", namespace="payee_payers")),
    path("reports/", include("reports.urls", namespace="reports")),
    path("transactions/", include("financial_transactions.urls", namespace="financial_transactions")),
    path("users/", include("users.urls", namespace="users")),
    path("", TemplateView.as_view(template_name="main/index.html"), name="home"),
]

if settings.DEBUG is True:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path("400/", default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        path("403/", default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        path("404/", default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        path("500/", default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
        ] + urlpatterns

    # Adds proper references for static and media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
