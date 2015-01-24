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

NAME_LENGTH = 48
URL_LENGTH = 256
TITLE_LENGTH = 256
DEFAULT_COMMENT_LENGTH = 512
DEFAULT_TEXT_LENGTH = 8192
EVENT_TYPE_CHOICES = (
	('EDIT_ISSUE', 'edit issue'),
	('QUESTION', 'question'),
	('ANSWER', 'answer'),
	('DISCUSSION', 'discussion'),
	('REPLY', 'reply'),
	('COMMENT', 'comment'),
	('LETTER', 'letter'),
	('SIGN_LETTER','sign letter'),
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


class Vote(TimeStamped):
	user = models.ForeignKey(User)
	valence = models.SmallIntegerField(choices=VOTE_CHOICES)

	class Meta:
		abstract=True


class Subscribable(TimeStamped):
	'''
		models that inheret subscribable get assigned a globally unique 
		subscription_id the first time that they are saved.  Within the app,
		the subscription_id acts as an identifier accross different kinds
		of objects (proposals, questions, petitions...) which users can
		be subscribed to.  Users are always auto-subscribed to content
		they generated.
	'''
		
	subscription_id = models.ForeignKey('SubscriptionId', editable=False)


	def _get_subscription_id(self):
		s = SubscriptionId()
		s.save()
		return s

	def save(self, *args, **kwargs):
		if not hasattr(self, 'subscription_id'):
			self.subscription_id = self._get_subscription_id()
		
		return super(Subscribable, self).save(*args, **kwargs)

	class Meta:
		abstract = True


# *** Concrete Models *** # 


class Sector(TimeStamped):
	short_name = models.CharField(max_length=3)
	name = models.CharField(max_length=64)

	def __unicode__(self):
		return self.render()

	def render(self):
		html =  (
			'<div class="sector_tag ' + self.name + '_sector">' 
				+ self.name + 
			'</div>'
		)

		return mark_safe(html)


class Tag(TimeStamped):
	name = models.CharField(max_length=48)
	sector = models.ForeignKey(Sector, null=True)
	target = models.ForeignKey('self', null=True)

	def __unicode__(self):
		return self.name


class Proposal(Subscribable):
	is_published = models.BooleanField(default=False)
	score = models.SmallIntegerField(default=0)
	title = models.CharField(max_length=256)
	summary = models.TextField()
	text = models.TextField()

	# TODO: add (actors) as a many-to-many relationship

	# propogate to creation
	original_user = models.ForeignKey(
		User, related_name='initiated_proposals')
	user = models.ForeignKey(
		User, related_name='proposals_rectently_edited') 
	proposal_image = models.ImageField(
		upload_to='proposal_avatars',default='/digidemo/proposal-images/');
	tags = models.ManyToManyField(
		Tag, related_name='proposals', blank=True, null=True)
	sectors = models.ManyToManyField(
		Sector, related_name='proposals', blank=True, null=True)

	def get_latest(self):
		return ProposalVersion.get_latest(self)

	def __unicode__(self):
		return self.title

	def get_url(self, view_name):
		url_stub = reverse(view_name, kwargs={'proposal_id': self.pk})
		return url_stub + slugify(self.title)

	def get_question_url(self):
		url_stub = reverse('ask_question', kwargs={'target_id': self.pk})
		return url_stub + slugify(self.title)

	def get_question_list_url(self):
		url_stub = reverse('questions', kwargs={'proposal_id': self.pk})
		return url_stub + slugify(self.title)

	def get_open_discussions_url(self):
		url_stub = reverse('editors_area', 
			kwargs={'issue_id': self.pk, 'open_status': 'open'})
		return url_stub + slugify(self.title)

	def get_closed_discussions_url(self):
		url_stub = reverse('editors_area', 
			kwargs={'issue_id': self.pk, 'open_status': 'closed'})
		return url_stub + slugify(self.title)

	def get_start_discussion_url(self):
		url_stub = reverse('start_discussion', kwargs={'target_id': self.pk})
		return url_stub + slugify(self.title)

	def get_start_petition_url(self):
		url_stub = reverse('start_petition', kwargs={'target_id': self.pk})
		return url_stub + slugify(self.title)

	def get_petitions_url(self):
		url_stub = reverse('petitions', kwargs={'proposal_id': self.pk})
		return url_stub + slugify(self.title)

	def get_edit_url(self):
		url_stub = reverse('edit', kwargs={'issue_id': self.pk})
		return url_stub + slugify(self.title)
 
	def get_proposal_url(self):
		return self.get_url('proposal')

	class Meta:
		get_latest_by = 'creation_date'


class ProposalVersion(TimeStamped):
	proposal = models.ForeignKey(Proposal, blank=True, null=True)
	title = models.CharField(max_length=256)
	summary = models.TextField()
	text = models.TextField()
	user = models.ForeignKey(User)
	tags = models.ManyToManyField(
		Tag, related_name='proposal_versions',blank=True, null=True)
	sectors = models.ManyToManyField(
		Sector, related_name='proposal_versions', blank=True, null=True)

	@classmethod
	def get_latest(cls, proposal):
		pvs = cls.objects.filter(proposal=proposal).order_by('-creation_date')
		if len(pvs) == 0:
			raise cls.DoesNotExist('There are no proposal versions for that'
				'proposal')

		return pvs[0]


class UserProfile(TimeStamped):
	user = models.OneToOneField(User, related_name='profile')
	email_validated = models.BooleanField(default=False)
	avatar_img = models.ImageField(upload_to='avatars')
	rep = models.IntegerField(default=0)
	street = models.CharField(max_length=128)
	zip_code = models.CharField(max_length=10)
	country = models.CharField(max_length=64, choices=COUNTRIES)
	province = models.CharField(max_length=32, choices=PROVINCES, blank=True)
        followedProposals = models.ManyToManyField(Proposal,null=True)
	do_email_news = models.BooleanField(default=True)
	do_email_responses = models.BooleanField(default=True)
	do_email_petitions = models.BooleanField(default=True)
	do_email_watched = models.BooleanField(default=True)
	
	# non-field class attributes
	rep_events = {
		'up_proposal': 10,
		'dn_proposal': -2,
		'up_letter': 10,
		'dn_letter': -2,
		'do_downvote': -2,
		'up_comment': 5,
		'dn_comment': -2,
		'up_discussion': 10,
		'dn_discussion': -2,
		'up_question': 10,
		'dn_question': -2,
		'up_answer': 10,
		'dn_answer': -2,
		'up_reply': 10,
		'dn_reply': -2,
	}
                
	def __unicode__(self):
		return self.user.username


	def get_rep_delta(self, event_name):
		# Validation: event_name should be a string
		if not isinstance(event_name, basestring):
			raise ValueError('UserProfile.apply_score: event_name should'
				'be string-like.') 

		try:
			rep_delta = self.rep_events[event_name]

		except KeyError as e:
			raise ValueError('UserProfile: there is no %s rep-event.' % 
					str(event_name))

		return rep_delta


	def apply_rep(self, event_name):
		self.rep += self.get_rep_delta(event_name)


	def undo_rep(self, event_name):
		self.rep -= self.get_rep_delta(event_name)

	def get_user_url(self):
                url_stub = reverse('userProfile', kwargs={'userName': self.user.username})
                return url_stub;
	

	def get_avatar_img_url(self):

		if self.avatar_img:
			return self.avatar_img.url

		else:
			return static('digidemo/images/avatar_not_found.png')
			

class Person(TimeStamped):
	fname = models.CharField(max_length=NAME_LENGTH)
	lname = models.CharField(max_length=NAME_LENGTH)
	portrait_url = models.CharField(max_length=URL_LENGTH)
	wikipedia_url = models.CharField(max_length=URL_LENGTH)
	bio_summary = models.TextField()

	
class Organization(TimeStamped):
	short_name = models.CharField(max_length=64)
	legal_name = models.CharField(max_length=128)
	legal_classification = models.CharField(
		max_length=48, choices=LEGAL_CLASSIFICATIONS)
	revenue = models.BigIntegerField()
	operations_summary = models.TextField()


# Rename this "Actor"
class Position(TimeStamped):
	name = models.CharField(max_length=128) # name of position (i.e. title)
	person = models.ForeignKey(Person)
	organization = models.ForeignKey(Organization)
	salary = models.DecimalField(max_digits=11, decimal_places=2)
	telephone = models.CharField(max_length=14)
	email = models.EmailField(max_length=254)
	mandate_summary = models.TextField()

	def __unicode__(self):
		return "%s, %s %s" %(self.name, self.person.fname, 
			self.person.lname)


class Letter(Subscribable):
	parent_letter = models.ForeignKey('self', blank=True, null=True, 
		related_name='resent_letters')
	target = models.ForeignKey(Proposal)
	valence = models.SmallIntegerField(choices=VALENCE_CHOICES)
	user = models.ForeignKey(User)
	score = models.SmallIntegerField(default=1)
	title = models.CharField(max_length=TITLE_LENGTH)
	recipients = models.ManyToManyField(Position, related_name='letters')
	text = models.TextField()

	def __unicode__(self):
		return "%s-%s" %(
			self.user.username,
			get_choice(VALENCE_CHOICES, self.valence))

	def get_url(self):
		url = reverse('view_petition', kwargs={'petition_id': self.pk})
		return url + slugify(self.title)

	def increment_score(self):
		self.score += 1
		self.save()


class Discussion(ScoredPost, Subscribable):
	target = models.ForeignKey(Proposal, null=True)
	title = models.CharField(max_length=TITLE_LENGTH)
	is_open = models.BooleanField(default=False)

	def __unicode__(self):
		return self.title

	def get_url(self):
		url = reverse('view_discussion', kwargs={'post_id': self.pk})
		return url + slugify(self.title)


class Reply(ScoredPost, Subscribable):
	target = models.ForeignKey(Discussion, null=True, related_name='replies')
	is_open = models.BooleanField(default=False)

	def __unicode__(self):
		return self.user.username


class Question(ScoredPost, Subscribable):
	title = models.CharField('question title', max_length=TITLE_LENGTH)
	target = models.ForeignKey(Proposal)

	def get_url(self):
		url = reverse('view_question', kwargs={'post_id':self.pk})
		return url + slugify(self.title)


class Answer(ScoredPost, Subscribable):
	target = models.ForeignKey(Question, related_name='replies')


# This should be renamed "LetterComment"
class Comment(ScoredPost, TimeStamped):
	target = models.ForeignKey(Letter, related_name='comment_set')


class QuestionComment(ScoredPost, TimeStamped):
	target = models.ForeignKey(Question, related_name='comment_set')
	

class AnswerComment(ScoredPost, TimeStamped):
	target = models.ForeignKey(Answer, related_name='comment_set')


class DiscussionComment(ScoredPost, TimeStamped):
	target = models.ForeignKey(Discussion, related_name='comment_set')


class ReplyComment(ScoredPost, TimeStamped):
	target = models.ForeignKey(Reply, related_name='comment_set')


class DiscussionVote(Vote):
	target = models.ForeignKey(Discussion)

	class Meta:
		unique_together = ('user', 'target')

class ProposalVote(Vote):
	target = models.ForeignKey(Proposal)

	class Meta:
		unique_together	= ('user', 'target')

class LetterVote(Vote):
	target = models.ForeignKey(Letter)

	class Meta:
		unique_together = ('user', 'target')

class ReplyVote(Vote):
	target = models.ForeignKey(Reply)

	class Meta:
		unique_together = ('user', 'target')

class QuestionVote(Vote):
	target = models.ForeignKey(Question)

	class Meta:
		unique_together = ('user', 'target')

class AnswerVote(Vote):
	target = models.ForeignKey(Answer)

	class Meta:
		unique_together = ('user', 'target')

class CommentVote(Vote):
	target = models.ForeignKey(Comment)

	class Meta:
		unique_together = ('user', 'target')


# *** Models for handling Notifications ***#

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


class Notifications(TimeStamped):
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


class Subscriptions(TimeStamped):
	'''
		Lists the objects that users are subscribed to.
	'''
	REASON_CHOICES = (
		('AUTHOR', 'author'),
		('COMMENTER', 'commenter'),
		('SUBSCRIBED', 'actively subscribed'),
	)
	user_id = models.ForeignKey(User, related_name='subscriptions')
	reason = models.CharField(max_length=20, choices=REASON_CHOICES)
	subscription_id = models.ForeignKey('SubscriptionId', 
		related_name='subscriptions')


