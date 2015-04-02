from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage
from digidemo.views import get_notification_message
from digidemo.abstract_models import Notification

class Command(BaseCommand):

	help = 'Sends mail for all open notifications'
	

	def handle(self, *args, **options):
		num_sent = 0

		notifications = Notification.objects.filter(
			was_seen=False, was_mailed=False)

		for n in notifications:
			note_msg = get_notification_message(n)
			user = n.target_user
			fname, user_email = user.first_name, user.email
			subject = note_msg
			link = 'https://luminocracy.org' + n.link_back
			
			if n.event_type not in ['VOTE', 'SIGN_LETTER', 'SYSTEM']:
				email_message = 'Hey %s,<br/><br/>%s.' % (fname, note_msg)
				email_message += '<br/><a href="%s">' % link
				email_message += 'Come see what they said</a>!' 
				email_message += '<br/><br/>Bye now!<br/>~mailbot'

			if n.event_type == 'VOTE':
				email_message = 'Hey %s,<br/><br/>%s' % (fname, note_msg)
				email_message += '<br/><a href="%s">' % link
				email_message += 'See your post here</a>!' 
				email_message += '<br/><br/>Bye now!<br/>~mailbot'

			if n.event_type == 'SIGN_LETTER':
				email_message = 'Hey %s,<br/><br/>%s!' % (fname, note_msg)
				email_message += '<br/><a href="%s">' % link
				email_message += 'Have a look</a>!' 
				email_message += '<br/><br/>Bye now!<br/>~mailbot'

			if n.event_type == 'SYSTEM':
				email_message = 'Hey %s,<br/><br/>%s.' % (fname, note_msg)
				email_message += '<br/><a href="%s">' % link
				email_message += 'Have a look</a>!' 
				email_message += '<br/><br/>Bye now!<br/>~mailbot'

			from_address = 'notifications@luminocracy.org'

			msg = EmailMessage(
				subject, email_message, from_address, [user_email])
			msg.content_subtype = 'html'
			msg.send()
			num_sent += 1

			# mark notification as mailed
			n.was_mailed = True
			n.save()

		log_fh = open('mail_log.txt', 'a')
		log_fh.write('%s sent %d mails.' % (str(timezone.now()), num_sent))
		log_fh.close()
		
