from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage
from digidemo.views import get_notification_message
from digidemo.abstract_models import Subscription

class Command(BaseCommand):

	help = 'Finds and removes duplicate subscriptions' 
	
	def handle(self, *args, **options):
		subscriptions = Subscription.objects.all()
		seen_subscriptions = set()

		total_subscriptions = subscriptions.count()
		print 'There are %d subscriptions.' % total_subscriptions
		num_kept = 0
		num_deleted = 0

		# Iterate over subscriptions.  Add unseen subscriptions to 
		# seen_subscriptions.  Delete subscriptions that were already seen.
		# subscription is considered seen if has same user and subscription_id
		for s in subscriptions:
			sub_record = (s.user.username, s.subscription_id.pk)

			if sub_record in seen_subscriptions:
				s.delete()
				num_deleted += 1

			else:
				seen_subscriptions.add(sub_record)
				num_kept += 1

		print 'Deleted %d subscriptions.  kept %d.' % (num_deleted, num_kept)

