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

# Mail settings
# ------------------------------------------------------------------------------

EMAIL_PORT = 1025

EMAIL_HOST = 'localhost'
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')


# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}
