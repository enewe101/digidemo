"""
	Django settings for the digidemo project.
"""

import os
import sys
from digidemo import local_settings
from django.utils.translation import ugettext_lazy as _


	####################
	#                  #
	#   DEFINE PATHS   #
	#                  #
	####################

PROJECT_DIR = local_settings.PROJECT_DIR
BASE_DIR = os.path.join(PROJECT_DIR, 'src')
TEMP_DIR = os.path.join(PROJECT_DIR, 'temp')
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static/')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media/')

DATA_FIXTURE = 'production_data'
if hasattr(local_settings, 'DATA_FIXTURE'):
	DATA_FIXTURE = local_settings.DATA_FIXTURE

TEST_FIXTURE = 'test_data'

	##########################################
	#                                        #
	#   TESTING, DEBUGGING, AND STRICTNESS   #
	#                                        #
	##########################################

TEST_MODE = 'test' in sys.argv
TEMPLATE_DEBUG = not TEST_MODE
DEBUG =  local_settings.DEBUG_TEST if TEST_MODE else local_settings.DEBUG

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


	################
	#              #
	#   SECURITY   #
	#              #
	################

SECRET_KEY = local_settings.SECRET_KEY
ALLOWED_HOSTS = local_settings.ALLOWED_HOSTS


	#########################
	#                       #
	#   LOADED COMPONENTS   #
	#                       #
	#########################

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.contrib.messages.context_processors.messages',
	'django.core.context_processors.request',
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.i18n'	
)

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
AUTH_USER_MODEL = 'auth.User'

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.locale.LocaleMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)



	#####################
	#                   #
	#   URLS AND WSGI   #
	#                   #
	#####################

ROOT_URLCONF = 'digidemo.urls'
WSGI_APPLICATION = 'digidemo.wsgi.application'


	#####################################
	#                                   #
	#   CONNECTIONS TO OTHER SOFTWARE   #
	#                                   #
	#####################################

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


	#########################################
	#                                       #
	#   LANGUAGE AND INTERNATIONALIZATION   #
	#                                       #
	#########################################

LANGUAGE_CODE = 'en-ca'
LANGUAGES = (
		('en-ca', _('English')),
		('fr-ca', _('French'))
)
LOCALE_PATHS = (
	os.path.join(BASE_DIR, 'digidemo/locale/')
)

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

