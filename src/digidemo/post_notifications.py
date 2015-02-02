#! /usr/bin/env python

import sys
sys.path.append('/Users/enewe101/projects/digidemo/src')
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "digidemo.settings")

from digidemo.models import * 
from digidemo.abstract_models import *

def post_notifications():
	'''
		Notify subscribed users of recent events.
	'''
	num_notifications = 0
	num_publications = 0
	unposted = Publication.objects.filter(was_posted=False)
	for pub in unposted:
		subscriptions = Subscription.objects.filter(
			subscription_id=pub.subscription_id 
		).exclude(
			user=pub.source_user
		)

		for sub in subscriptions:
			note = Notification(
				source_user = pub.source_user,
				target_user = sub.user,
				event_type = pub.event_type,
				reason = sub.reason,
				event_data = pub.event_data,
				link_back = pub.link_back
			)
			note.save()
			num_notifications += 1

		num_publications += 1
		pub.was_posted = True
		pub.save()

	print '%d publications generated %d new notifications.' % (
			num_publications, num_notifications)


if __name__ == '__main__':
	post_notifications()
