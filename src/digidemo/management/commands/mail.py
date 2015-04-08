import os
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage
from digidemo.views import get_notification_message
from digidemo.abstract_models import Notification
from digidemo.models import User
from digidemo.settings import BASE_DIR
from django.utils import timezone
from digidemo.shortcuts import create_unsubscribe_link

class Command(BaseCommand):

	help = 'Sends mail for all open notifications'

	def handle(self, *args, **options):


		# get all the notifications that haven't yet been seen or mailed
		notifications = Notification.objects.filter(
			was_seen=False, was_mailed=False)

		# we'll keep track of the number of emails the script sends out
		num_sent = 0

		# take a look at each notification, and possibly send an email for it
		for n in notifications:

			# only mail users whose email preferences allow it
			user = n.target_user
			if not user.profile.do_email_responses:

				# mark notification as mailed anyway (so we don't try to send 
				# it again later)
				n.was_mailed = True
				n.save()
				continue

			# gather some info needed to make the email
			note_msg = get_notification_message(n)
			fname, user_email = user.first_name, user.email
			subject = note_msg
			link = 'https://luminocracy.org' + n.link_back
			from_address = 'notifications@luminocracy.org'

			# compose the email message.  Email format depends on event_type.
			if n.event_type not in ['VOTE', 'SIGN_LETTER', 'SYSTEM']:
				email_message = 'Hey %s,<br/><br/>%s.' % (fname, note_msg)
				email_message += '<br/><a href="%s">' % link
				email_message += 'Come see what they said</a>!' 
				email_message += '<br/><br/>Bye now!<br/>~mailbot'

			elif n.event_type == 'VOTE':
				email_message = 'Hey %s,<br/><br/>%s' % (fname, note_msg)
				email_message += '<br/><a href="%s">' % link
				email_message += 'See your post here</a>!' 
				email_message += '<br/><br/>Bye now!<br/>~mailbot'

			elif n.event_type == 'SIGN_LETTER':
				email_message = 'Hey %s,<br/><br/>%s!' % (fname, note_msg)
				email_message += '<br/><a href="%s">' % link
				email_message += 'Have a look</a>!' 
				email_message += '<br/><br/>Bye now!<br/>~mailbot'

			elif n.event_type == 'SYSTEM':
				email_message = 'Hey %s,<br/><br/>%s.' % (fname, note_msg)
				email_message += '<br/><a href="%s">' % link
				email_message += 'Have a look</a>!' 
				email_message += '<br/><br/>Bye now!<br/>~mailbot'

			# add an unsubscribe link to the email
			unsubscribe_link = create_unsubscribe_link(user)
			email_message += '<br/><hr/><a href="%s">' % unsubscribe_link
			email_message += 'unsubscribe</a>'

			# make and send the email
			msg = EmailMessage(
				subject, email_message, from_address, [user_email])
			msg.content_subtype = 'html'
			msg.send()
			num_sent += 1

			# mark notification as mailed
			n.was_mailed = True
			n.save()

		# log the fact that the email script was run
		log_fname = os.path.join(BASE_DIR, 'mail_log.txt')
		log_fh = open(log_fname, 'a')
		log_fh.write('%s sent %d mails.\n' % (str(timezone.now()), num_sent))
		log_fh.close()

