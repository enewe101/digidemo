import hashlib
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as __
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from digidemo.models import *


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


def send_email_confirmation(user):
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
		__('To verify your account, click this link: https:/'
		+ reverse('verify_email', kwargs={'code': random_hash}))
	)

	send_mail(__('Welcome to luminocracy'), message, 
		__('welcome@luminocracy.org'), [user.email], 
		fail_silently=False
	)

