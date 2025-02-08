"""Production settings for Treasurer Tools project."""
import logging

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *
from .base import env


# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = env.bool('DJANGO_CSRF_COOKIE_HTTPONLY', default=True)
# https://docs.djangoproject.com/en/stable/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = env.bool('DJANGO_CSRF_COOKIE_SECURE', default=True)
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = env.bool('DJANGO_SECURE_BROWSER_XSS_FILTER', default=True)
# https://docs.djangoproject.com/en/stable/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env.bool('DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = env.bool('DJANGO_SECURE_HSTS_PRELOAD', default=True)
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-hsts-seconds
SECURE_HSTS_SECONDS = env.int('DJANGO_SECURE_HSTS_SECONDS', default=60)
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = None # Site not served through proxy at this time
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
# https://docs.djangoproject.com/en/stable/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = env.bool('DJANGO_SESSION_COOKIE_HTTPONLY', default=True)
# https://docs.djangoproject.com/en/stable/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = env.bool('DJANGO_SESSION_COOKIE_SECURE', default=True)
# https://docs.djangoproject.com/en/stable/ref/settings/#x-frame-options
X_FRAME_OPTIONS = env('DJANGO_X_FRAME_OPTIONS', default='DENY')


# DATABASES
# ------------------------------------------------------------------------------
DATABASES['default']['CONN_MAX_AGE'] = env.int('DJANGO_DB_CONN_MAX_AGE', default=60)


# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'{env("REDIS_URL", default="redis://127.0.0.1:6379")}/{0}',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            # Mimicing memcache behavior.
            # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
            'IGNORE_EXCEPTIONS': True,
        }
    }
}


# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#templates
TEMPLATES[0]['OPTIONS']['loaders'] = [
    (
        'django.template.loaders.cached.Loader',
        [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]
    ),
]


# STORAGES
# ------------------------------------------------------------------------------
# https://whitenoise.readthedocs.io/en/latest/django.html#enable-whitenoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
_AWS_EXPIRY = 60 * 60 * 24 * 7,

STORAGES = {
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#configuration-settings
    'default': {
        'BACKEND': 'storages.backends.s3.S3Storage',
        'OPTIONS': {
            'access_key': env('AWS_ACCESS_KEY_ID'),
            'secret_key': env('AWS_SECRET_ACCESS_KEY'),
            'bucket_name': env('AWS_STORAGE_BUCKET_NAME'),
            'querystring_auth': False,
            'object_parameters': {
                'CacheControl': f'max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate',
            }
        }
    },

    # https://whitenoise.readthedocs.io/en/latest/django.html#add-compression-and-caching-support
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}


# EMAIL SETTINGS
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env('EMAIL_BACKEND')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True if env('EMAIL_USE_TLS') == 'True' else False
EMAIL_PORT = env('EMAIL_PORT')


# Sentry
# ------------------------------------------------------------------------------
sentry_sdk.init(
    dsn=env('DJANGO_SENTRY_DSN'),
    integrations=[DjangoIntegration()],
)
LOGGING_CONFIG = None
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': env.int('DJANGO_SENTRY_LOG_LEVEL'),
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console',],
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console',],
            'propagate': False,
        },
    },
})
