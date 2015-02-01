from django.db import models
from digidemo.choices import *
from django.contrib.auth.models import User
from django.utils import timezone 
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.templatetags.staticfiles import static
import re
import os


# Constants
NAME_LENGTH = 48
URL_LENGTH = 256
TITLE_LENGTH = 256
DEFAULT_COMMENT_LENGTH = 512
DEFAULT_TEXT_LENGTH = 8192
EVENT_TYPE_CHOICES = (
	('ISSUE', 'issue'),
	('EDIT_ISSUE', 'edit issue'),
	('QUESTION', 'question'),
	('ANSWER', 'answer'),
	('DISCUSSION', 'discussion'),
	('REPLY', 'reply'),
	('COMMENT', 'comment'),
	('LETTER', 'letter'),
	('SIGN_LETTER','sign letter'),
	('VOTE', 'vote'),
	('SYSTEM', 'system'),
)

# *** Abstract Models *** #

class TimeStamped(models.Model):
	creation_date = models.DateTimeField(editable=False)
	last_modified = models.DateTimeField(editable=False)

	def save(self, *args, **kwargs):
		if not self.creation_date:
			self.creation_date = timezone.now()
		
		self.last_modified = timezone.now()
		return super(TimeStamped, self).save(*args, **kwargs)

	class Meta:
		abstract = True


class ScoredPost(models.Model):
	user = models.ForeignKey(User)
	score = models.SmallIntegerField(default=0, editable=False)
	text = models.CharField(max_length=DEFAULT_TEXT_LENGTH)

	def __unicode__(self):
		return self.text[:20]

	class Meta:
		abstract = True


class TriggersNotification(TimeStamped):

	'''
		An abstract class for defining the behavior of objects which, when
		created, should trigger some kind of notification (by creating
		entries in the publication table).
		
		Objects that inherit this mixin might need to override some of the
		methods here.  For example, get_targets should yield a list of
		subscription_ids, which help identify sets of users to be notified.

		Objects that inherit from this *must* override get_event_type(),
		and yield one of the options in event_type_choices as a string.

		Subclasses of TriggersNotification can suppress this notification
		begavior by overriding get_targets() such that it returns an empty 
		list.  In this case, none of the additional methods defined here
		other than save() would be called when save is called on the subclass.
	'''

	def get_event_type(self):
		raise NotImplementedError(
			'Subclasses of TriggersNotification must override'
				+ ' get_event_type()'
		)

	def get_targets(self):
		return [self.target.subscription_id]

	def get_source_user(self):
		'''
			The user that created this object, responsible for triggering
			notifications.
		'''
		return self.user

	def get_event_data(self):
		'''
			A string that returns some kind of useful info about the 
			object triggering the notification, like the first couple
			lines of a Proposal, or a Letter.  (Can be the empty string)
		'''
		return self.text[:100]

	def get_link_back(self):
		'''
			A url that users notified can click to see this object or some
			relevant info about it.  (Can be None)
		'''
		return self.get_url()


	def save(
			self, 
			suppress_publish=False, 
			force_publish=False, 
			*args, 
			**kwargs
		):

		# Check if this is the first save, and decide whether to publish
		first_save = (self.pk is None)
		do_publish = (first_save or force_publish) and not suppress_publish

		# Let save happen normally 
		super(TriggersNotification, self).save(*args, **kwargs)

		# Now, if this was the first save, issue publication(s)
		if do_publish:
			self.publish()


	def publish(
			self,
			targets=[],
			source_user=None,
			event_data=None,
			link_back=None,
			event_type=None
		):

		# get a list of targets for this notification.  
		targets = targets or self.get_targets()

		# If there aren't any targets, there's nothing to do.
		if len(targets) == 0:
			return

		# get some information about the publication(s) to be made
		source_user = source_user or self.get_source_user()
		event_data = event_data or self.get_event_data()
		link_back = link_back or self.get_link_back()
		event_type = event_type or self.get_event_type()

		# now make all the notifications
		for subscription_id in targets:
			pub = Publication(
				source_user = source_user,
				subscription_id = subscription_id,
				event_type = event_type,
				event_data = event_data,
				link_back = link_back
			)
			pub.save()

	class Meta:
		abstract = True


class Subscribable(TriggersNotification):
	'''
		models that inheret subscribable get assigned a globally unique 
		subscription_id the first time that they are saved.  Within the app,
		the subscription_id acts as an identifier accross different kinds
		of objects (proposals, questions, petitions...) which users can
		be subscribed to.  Users are always auto-subscribed to content
		they generated.

		subscribable objects should define some kind of author which is 
		returned
		by get_author().  This is used to automatically subscribe the creator
		of a subscribable.  To suppress this behavior, simply make
		get_author() return None.

		Note that all Subclasses of Subscribable are of the type
		TriggersNotification.  The notification behavior can be suppressed
		by overriding the method get_targets to return an empty list.
	'''

	subscription_id = models.ForeignKey('SubscriptionId', editable=False)

	def _get_subscription_id(self):
		s = SubscriptionId()
		s.save()
		return s

	def get_author(self):
		return self.user

	def get_reason(self):
		'''
			Gets the reason that the person was subscribed.  Default to
			AUTHOR, because most of the time people are subscribed because
			thay created the thing.
		'''
		return 'AUTHOR'

	def save(
			self, 
			suppress_subscribe=False, 
			force_subscribe=False,
			*args, **kwargs
		):

		# Is this the first save?  Then give this object a subscription_id
		first_save = (self.pk is None)
		if first_save:
			self.subscription_id = self._get_subscription_id()
		
		# Save the object
		super(Subscribable, self).save(*args, **kwargs)

		# If this is the first save, subscribe the author to this object
		# This behavior can be suppressed by returning non from get_author()
		if (first_save or force_subscribe) and not suppress_subscribe:
			self.subscribe()


	def subscribe(self, subscriber=None, reason=None):

			# default values are assumed so that authors can be auto-susbcribed
			# when their subscribable object is saved.  This can be overridden.
			subscriber = subscriber or self.get_author()
			reason = reason or self.get_reason()

			if subscriber is not None:
				sub, created = Subscription.objects.get_or_create(
					user = subscriber,
					reason = reason,
					subscription_id = self.subscription_id
				)
				sub.save()


	class Meta:
		abstract = True


class AbstractComment(ScoredPost, Subscribable):

	def get_event_type(self):
		return 'COMMENT'

	def get_url(self):
		return None

	class Meta:
		abstract=True
	

class Vote(TriggersNotification):
	user = models.ForeignKey(User)
	valence = models.SmallIntegerField(choices=VOTE_CHOICES)

	def get_event_data(self):
		return str(self.valence)

	def get_event_type(self):
		return 'VOTE'

	def get_link_back(self):
		return None

	class Meta:
		abstract=True


# *** Models for handling Notifications ***#

	# Note, although SubscriptionId and Publication are not actually
	# abstract models,
	# They are defined in abstract_models.py because it is needed to define
	# abstract models!


class Notification(TimeStamped):
	'''
		A list of notifications to be delivered (or recently delivered)
		to users.  Existing notifications can also lead to email being sent
		to users, depending on the user's settings, and how much time has
		passed since the notification was first inserted.
	'''
	source_user = models.ForeignKey(
		User, related_name='triggered_notifications', null=True)
	target_user = models.ForeignKey(
		User, related_name='received_notifications', null=True)
	event_type = models.CharField(
			max_length=20, choices=EVENT_TYPE_CHOICES)
	event_data = models.CharField(max_length=2048)
	link_back = models.URLField(max_length=512, null=True)
	was_seen = models.BooleanField(default=False)
	was_mailed = models.BooleanField(default=False)


class Subscription(TimeStamped):
	'''
		Lists the objects that users are subscribed to.
	'''
	REASON_CHOICES = (
		('AUTHOR', 'author'),
		('COMMENTER', 'commenter'),
		('SUBSCRIBED', 'actively subscribed'),
		('EDITOR', 'edited related content')
	)
	user = models.ForeignKey(User, related_name='subscriptions')
	reason = models.CharField(max_length=20, choices=REASON_CHOICES)
	subscription_id = models.ForeignKey('SubscriptionId', 
		related_name='subscriptions')



class SubscriptionId(TimeStamped):
	'''
		this is a list of all the subscribable ids ever assigned.  It may seems
		strange to have a table that stores only primary keys!  But it 
		provides a linkage point between subscribable objects, like proposals,
		questions, discussions, etc, and user's subscriptions.
			2) By linking to the SubscriptionId, rather than the subscribable
				directly, we don't have an issue with the fact that the 
				subscribables are of heterogeneous types.
			1) We rely on the db's autoincrement to give out unique 
				subscription id's.
	'''
	subscription_id = models.AutoField(primary_key=True)

	def __unicode__(self):
		return str(self.subscription_id)


class Publication(TimeStamped):
	'''
		This logs events that should trigger notifications.  An asyncronous
		process periodically looks for unposted publications, checks which
		users are subscribed, and makes a notification entry for the 
		publication for each subscribed user.  One event makes only one
		Publication, but the publication leads to many Notifications.
	'''

	source_user = models.ForeignKey(
		User, related_name='publications', null=True)
	subscription_id = models.ForeignKey('SubscriptionId', 
		related_name='publications')
	event_type = models.CharField(
		max_length=20, choices=EVENT_TYPE_CHOICES)
	was_posted = models.BooleanField(default=False)
	event_data = models.CharField(max_length=2048)
	link_back = models.URLField(max_length=512, null=True)

