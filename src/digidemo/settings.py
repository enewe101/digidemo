"""
Django settings for digidemo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
import sys
from digidemo import local_settings
from django.utils.translation import ugettext_lazy as _

TESTING_MODE = 'test' in sys.argv
TEMPLATE_DEBUG = not TESTING_MODE
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = local_settings.DEBUG

class InvalidString(str):
    def __mod__(self, other):
        from django.template.base import TemplateSyntaxError
        raise TemplateSyntaxError(
            "Undefined variable or unknown value for: \"%s\"" % other)

STRICT_TEMPLATE = local_settings.STRICT_TEMPLATE
if STRICT_TEMPLATE:
	TEMPLATE_STRING_IF_INVALID = InvalidString("%s")
else:
	TEMPLATE_STRING_IF_INVALID = ''
	
PROJECT_DIR = local_settings.PROJECT_DIR
BASE_DIR = PROJECT_DIR + '/src'
TEMP_DIR = PROJECT_DIR + '/temp'
AUTH_USER_MODEL = 'auth.User'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = local_settings.SECRET_KEY

ALLOWED_HOSTS = local_settings.ALLOWED_HOSTS

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.contrib.messages.context_processors.messages',
	'django.core.context_processors.request',
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.i18n'	
)

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'digidemo',
	'haystack',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'digidemo.urls'
WSGI_APPLICATION = 'digidemo.wsgi.application'
DATABASES = local_settings.DATABASES

HAYSTACK_CONNECTIONS = {
	'default': {
		'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
		'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
	},
}

EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = local_settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = local_settings.EMAIL_HOST_PASSWORD
EMAIL_PORT = 587
EMAIL_USE_TLS = True

LANGUAGE_CODE = 'en-ca'
LANGUAGES = (
		('en-ca', _('English')),
		('fr-ca', _('French'))
)
LOCALE_PATHS = (
	os.path.join(BASE_DIR, '/digidemo/locale/')
)

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = (BASE_DIR + '/digidemo/static',)
STATIC_ROOT = PROJECT_DIR + '/static'
MEDIA_URL = '/media/'
MEDIA_ROOT = PROJECT_DIR + '/media/'
