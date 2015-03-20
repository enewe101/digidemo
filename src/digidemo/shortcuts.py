# -*- coding: utf-8 -*-
import hashlib

from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as __
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse

from digidemo.models import *
from digidemo.settings import DEBUG, LANGUAGES


def get_profile(user):
	return UserProfile.objects.get(user=user)


def login_user(username, password, request):

		# if the username contains an '@', then its actually an email
		if '@' in username:
			username = User.objects.get(email=username).username

		# try to authenticate the user
		user = authenticate(
			username=username,
			password=password
		)

		# If successful, get the original login-required url, which was
		# concatenated onto the login-required url, as the 'next' kwarg.
		if user:
			login(request, user)

			if get_profile(user).email_validated:
				return 'LOGIN_VALID_EMAIL'

			else:
				return 'LOGIN_INVALID_EMAIL'

		else:
			return 'LOGIN_FAILED'


def get_domain_and_language(request):
	return 'https://luminocracy.org/%s' % request.LANGUAGE_CODE


def url_patch_lang(url, language_code=None):
	'''
		if the incoming url has a prefix, corresponding to a language code 
		listed in settings.LANGUAGES, strip this language code and replace it
		with language_code.  It does not matter whether language_code or
		url have starting or ending slashes.  The final result will have a 
		starting slash.  If language_code is Falsy (e.g. '' or None)
		then the result is simply to strip the language.
	'''
	if not language_code:
		language_code = ''

	else:
		lang_finder = '/?(%s)/?' % '|'.join([l[0] for l in LANGUAGES])
		lang_match = re.compile(lang_finder).match(language_code)
		if lang_match is None:
			raise ValueError(
				'language_code should be language code listed in '
				'settings.LANGUAGES.'
			)

		language_code = '/' + lang_match.group(1)

	lang_match_stripper = re.compile('/?(en|fr)-(ca|us)')
	no_lang_url = lang_match_stripper.sub('', url)
	if not no_lang_url.startswith('/'):
		no_lang_url = '/' + no_lang_url

	return language_code + no_lang_url


def send_email_confirmation(user, request):
	# send registration email
	random_hash = hashlib.sha256(
		'af612da003486b687' + user.username
	).hexdigest()[:32]

	# make a verification entry
	verification, created = EmailVerification.objects.get_or_create(
		user=user, code=random_hash
	)

	# send an email
	message = (
		__('To verify your account, click this link: ' 
			+ 'https://luminocracy.org'
			+ reverse('verify_email', kwargs={'code': random_hash})
		)
	)

	send_mail(__('Welcome to luminocracy'), message, 
		__('welcome@luminocracy.org'), [user.email], 
		fail_silently=DEBUG
	)

