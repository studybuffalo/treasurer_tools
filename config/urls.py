"""Main Site URL Conf"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from django.views.generic import TemplateView


urlpatterns = [
    url(r"^accounts/", include("allauth.urls")),
    url(r"^accounts/profile", TemplateView.as_view(template_name="account/profile.html"), name="account_profile"),
    url(r"^contact/$", TemplateView.as_view(template_name="account/profile.html"), name="contact"),
    url(r"^banking/", include("bank_transactions.urls")),
    url(r"^banking/reconciliation/", include("bank_reconciliation.urls")),
    url(r"^settings/banking/", include("bank_transactions.urls_settings")),
    url(r"^settings/codes/", include("financial_codes.urls")),
    url(r"^investments/", include("investments.urls")),
    url(r"^payee-payer/", include("payee_payers.urls")),
    url(r"^transactions/", include("financial_transactions.urls")),
    url(r"^users/", include("users.urls", namespace="users")),
    url(r"^$", TemplateView.as_view(template_name="main/index.html"), name="home"),
]

if settings.DEBUG is True:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

    # Adds proper references for static and media files    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
