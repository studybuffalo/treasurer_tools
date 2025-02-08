"""Base settings for Treasurer Tools project.
"""
import environ


# SETUP
# ------------------------------------------------------------------------------
# Setup directory references
ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path('treasurer_tools')

# Connect to the .env file
env = environ.Env()
env.read_env(str(ROOT_DIR.path('config', 'settings', 'treasurer_tools.env')))

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', default=True)
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env('DJANGO_SECRET_KEY', default='llyJzPogLi0gjBrvU0q6yJkwIDJsgLOre2JZMzsIPSlrq5mGbuesgOYvCJLyFWAh')
# https://docs.djangoproject.com/en/stable/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])


# GENERAL
# ------------------------------------------------------------------------------
TIME_ZONE = 'UTC'
# https://docs.djangoproject.com/en/stable/ref/settings/#language-code
LANGUAGE_CODE = 'en-CA'
LANGUAGES = [
    ('en', 'English'),
    #('fr', 'French'),
]
# https://docs.djangoproject.com/en/stable/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/stable/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/stable/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/stable/ref/settings/#use-tz
USE_TZ = True


# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#databases
DATABASES = {
    'default': env.db('DJANGO_DB_URL', default='postgres:///treasurer_tools'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True


# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#root-urlconf
ROOT_URLCONF = 'config.urls'
# https://docs.djangoproject.com/en/stable/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'


# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
THIRD_PARTY_APPS = [
    'allauth',
    'allauth.account',
    'simple_history',
]
LOCAL_APPS = [
    'treasurer_tools.bank_reconciliation.apps.BankReconciliationConfig',
    'treasurer_tools.bank_institutions.apps.BankInstitutionsConfig',
    'treasurer_tools.bank_transactions.apps.BankTransactionsConfig',
    'treasurer_tools.branch_details.apps.BranchDetailsConfig',
    'treasurer_tools.documents.apps.DocumentsConfig',
    'treasurer_tools.financial_codes.apps.FinancialCodesConfig',
    'treasurer_tools.financial_transactions.apps.FinancialTransactionsConfig',
    'treasurer_tools.investments.apps.InvestmentsConfig',
    'treasurer_tools.payee_payers.apps.PayeePayersConfig',
    'treasurer_tools.reports.apps.ReportsConfig',
    'treasurer_tools.users.apps.UsersConfig',
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-user-model
AUTH_USER_MODEL = 'users.User'
# https://docs.djangoproject.com/en/stable/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = 'home'
# https://docs.djangoproject.com/en/stable/ref/settings/#login-url
LOGIN_URL = 'account_login'
LOGOUT_URL = 'account_logout'


# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/stable/topics/auth/passwords/#using-argon2-with-django
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/stable/ref/settings/#middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]


# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    'sites': 'treasurer_tools.contrib.sites.migrations'
}


# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)


# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')


# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL path.
ADMIN_URL = env('DJANGO_ADMIN_URL', default='admin/')
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    (env('DJANGO_ADMIN_OWNER_NAME'), env('DJANGO_ADMIN_OWNER_EMAIL')),
]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS


# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            APPS_DIR('templates'),
        ],
        'OPTIONS': {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = ROOT_DIR('staticfiles')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = 'static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    APPS_DIR('static')
]

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'


# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'


# PASSWORD STORAGE SETTINGS
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]


# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Some really nice defaults
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_ALLOW_REGISTRATION = False
ACCOUNT_ADAPTER = 'treasurer_tools.users.adapters.AccountAdapter'

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = 'account_login'

# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'


# OTHER STANDARD SETTINGS
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Your common stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
