"""
Local settings for Treasurer Tools project.

- Runs in debug mode
- Uses console backend for emails
"""

from .base import *
# pylint: skip-file

import environ

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = True if env("DEBUG") == "True" else False

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env("SECRET_KEY", default='S>}{t(v|~SNz|uS%o:?8oMqJjmnR^q~00BYjc#wBr99,W.V*u;')

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env("SERVER_ADDRESS").split(" ")
# END SITE CONFIGURATION


# Mail settings
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env('EMAIL_BACKEND')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True if env('EMAIL_USE_TLS') == "True" else False
EMAIL_PORT = env('EMAIL_PORT')

# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}
