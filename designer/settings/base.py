import os
from os.path import join, abspath, dirname

from designer.settings.utils import get_logger_config

# PATH vars
here = lambda *x: join(abspath(dirname(__file__)), *x)
PROJECT_ROOT = here("..")
root = lambda *x: join(abspath(PROJECT_ROOT), *x)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'SET-ME-PLEASE'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'drf_yasg',
    'edx_api_doc_tools',
    'release_util',
    'rest_framework',
    'social_django',
    'waffle',
    'modelcluster',
    'taggit',
)

PROJECT_APPS = (
    'designer.apps.core',
    'designer.apps.api',
    'designer.apps.pages',
    'designer.apps.branding',
)

WAGTAIL_APPS = (
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',
    'wagtail.api.v2',
)

INSTALLED_APPS += THIRD_PARTY_APPS
INSTALLED_APPS += PROJECT_APPS
INSTALLED_APPS += WAGTAIL_APPS

MIDDLEWARE = (
    'edx_django_utils.monitoring.CookieMonitoringMiddleware',
    'edx_django_utils.monitoring.DeploymentMonitoringMiddleware',
    'edx_django_utils.cache.middleware.RequestCacheMiddleware',
    'waffle.middleware.WaffleMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'edx_rest_framework_extensions.middleware.RequestCustomAttributesMiddleware',
)

ROOT_URLCONF = 'designer.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'designer.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
# Set this value in the environment-specific files (e.g. local.py, production.py, test.py)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': 'designer',
        'USER': 'designer001',
        'PASSWORD': 'password',
        'HOST': 'localhost',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
        'ATOMIC_REQUESTS': False,
        'CONN_MAX_AGE': 60,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_DEPRECATED_PYTZ = True

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    root('conf', 'locale'),
)

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = root('media')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
# END MEDIA CONFIGURATION


# STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = root('assets')
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    root('static'),
)

# TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/1.11/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': (
            root('templates'),
        ),
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'designer.apps.core.context_processors.core',
            ),
            'debug': True,  # Django will only display debug pages if the global DEBUG setting is set to True.
        }
    },
]
# END TEMPLATE CONFIGURATION


# COOKIE CONFIGURATION
# The purpose of customizing the cookie names is to avoid conflicts when
# multiple Django services are running behind the same hostname.
# Detailed information at: https://docs.djangoproject.com/en/dev/ref/settings/
SESSION_COOKIE_NAME = 'designer_sessionid'
CSRF_COOKIE_NAME = 'designer_csrftoken'
LANGUAGE_COOKIE_NAME = 'openedx-language-preference'
# END COOKIE CONFIGURATION

# AUTHENTICATION CONFIGURATION
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'

AUTH_USER_MODEL = 'core.User'

AUTHENTICATION_BACKENDS = (
    'auth_backends.backends.EdXOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

ENABLE_AUTO_AUTH = False
AUTO_AUTH_USERNAME_PREFIX = 'auto_auth_'

SOCIAL_AUTH_STRATEGY = 'auth_backends.strategies.EdxDjangoStrategy'

 # Set these to the correct values for your OAuth2 provider (e.g., devstack)
SOCIAL_AUTH_EDX_OAUTH2_KEY = 'designer-sso-key'
SOCIAL_AUTH_EDX_OAUTH2_SECRET = 'designer-sso-key'
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = 'replace-me'
SOCIAL_AUTH_EDX_OAUTH2_ISSUER = "http://127.0.0.1:8000"
SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL = 'replace-me'
BACKEND_SERVICE_EDX_OAUTH2_KEY = 'designer-backend-service-key'
BACKEND_SERVICE_EDX_OAUTH2_SECRET = 'designer-backend-service-secret'
BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL = "http://127.0.0.1:8000/oauth2"

JWT_AUTH = {
    'JWT_ISSUERS': [],
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': lambda d: d.get('preferred_username'),
    'JWT_LEEWAY': 1,
    'JWT_DECODE_HANDLER': 'edx_rest_framework_extensions.auth.jwt.decoder.jwt_decode_handler',
    'JWT_ISSUER': [
        {
            'AUDIENCE': 'SET-ME-PLEASE',
            'ISSUER': 'http://127.0.0.1:8000/oauth2',
            'SECRET_KEY': 'SET-ME-PLEASE'
        }
    ],
    'JWT_PUBLIC_SIGNING_JWK_SET': None,
    'JWT_AUTH_COOKIE_HEADER_PAYLOAD': 'edx-jwt-cookie-header-payload',
    'JWT_AUTH_COOKIE_SIGNATURE': 'edx-jwt-cookie-signature',
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

# Request the user's permissions in the ID token
EXTRA_SCOPE = ['permissions']

LOGIN_REDIRECT_URL = '/cms/'
# END AUTHENTICATION CONFIGURATION


# OPENEDX-SPECIFIC CONFIGURATION
PLATFORM_NAME = 'Your Platform Name Here'
# END OPENEDX-SPECIFIC CONFIGURATION

# Set up logging for development use (logging to stdout)
LOGGING = get_logger_config(debug=DEBUG, dev_env=True, local_loglevel='DEBUG')

WAGTAIL_SITE_NAME = 'Designer'

CERTIFICATE_LANGUAGES= {
    'en': 'English',
    'es_419': 'Spanish'
}
DESIGNER_SERVICE_USER = 'designer_service_user'
CSRF_COOKIE_SECURE = False

EXTRA_APPS = []
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

EDX_DRF_EXTENSIONS = {
    "OAUTH2_USER_INFO_URL": "http://127.0.0.1:8000/oauth2/user_info"
}
API_ROOT = None
MEDIA_STORAGE_BACKEND = {
    'DEFAULT_FILE_STORAGE': 'django.core.files.storage.FileSystemStorage',
    'MEDIA_ROOT': MEDIA_ROOT,
    'MEDIA_URL': MEDIA_URL
}

WAGTAILADMIN_RICH_TEXT_EDITORS = {
    'default': {
        'WIDGET': 'designer.rich_text.RichTextArea'
    }
}
