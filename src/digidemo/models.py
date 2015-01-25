'''
	This defines the core objects for the application, and thus, much of its
	core behavior.

	It accomplishes a few things

		1) the database is set up based on the models here, so for every
			model, there is a database table that is made (thanks to Django)

		2) much of the application logic is defined by the behaviors that
			are given to these models through there methods.  
			
			As an example,
			the fact that, when a user creates a new Question, she will be
			notified when someone answers it, occurs by virtue of the fact 
			that, the Question model inherits the Subscribable abstract
			model, which causes a subscription to be made by the author
			of the question.

	There is a lot of important logic that is also defined in 
	abstract_models.py, and in general, all of the models described here
	extend some kind of abstract model.  The most basic abstract model is
	Timestamped.  Objects that are instances of Any model extending 
	Timestamped will always record the timestamp of their initial creation 
	and of subsequent modifications. (All models extend Timestamped, but 
	sometimes indirectly)
'''


# Includes
from django.db import models
from digidemo.choices import *
from django.contrib.auth.models import User
from django.utils import timezone 
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.templatetags.staticfiles import static
from digidemo import abstract_models
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


# *** All of the Concrete Models Follow *** # 


	# Note, models related to the notification system are defined in 
	# abstract_models.py, even though they are not actually abstract.
	# This is because they are needed to define the abstract models.
	# This includes SubscriptionId, Publication, Subscription, and 
	# Notification.


class EmailRecipient(abstract_models.TimeStamped):
    ''' 
        This is for people that sign up for to receive emails on our landing
        page.
    '''
    email = models.EmailField(max_length=254)
    active = models.BooleanField(default=True)


class Sector(abstract_models.Subscribable):
	# Overriden in Subscribable to prevent auto-subscription
	def get_author(self):
		return None

	# Overridden in TriggersNotification -- we don't want to issue 
	# notifications when users make new tags
	def get_targets(self):
		return []

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


class Tag(abstract_models.Subscribable):

	# Overriden in Subscribable to prevent auto-subscription
	def get_author(self):
		return None

	# Overridden in TriggersNotification -- we don't want to issue 
	# notifications when users make new tags
	def get_targets(self):
		return []

	name = models.CharField(max_length=48)
	sector = models.ForeignKey(Sector, null=True)
	target = models.ForeignKey('self', null=True)

	def __unicode__(self):
		return self.name


class Proposal(abstract_models.Subscribable):
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

	def get_event_type(self):
		return 'ISSUE'

	def get_targets(self):
		sector_targets = [s.subscription_id for s in self.sectors.all()]
		tag_targets = [t.subscription_id for t in self.tags.all()]
		targets = sector_targets + tag_targets

		return targets

	def get_latest(self):
		return ProposalVersion.get_latest(self)

	def __unicode__(self):
		return self.title

	def get_url(self):
		return self.get_url_by_view_name('proposal')

	def get_url_by_view_name(self, view_name):
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
		return self.get_url_by_view_name('proposal')

	class Meta:
		get_latest_by = 'creation_date'


class ProposalVersion(abstract_models.TimeStamped):
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


class UserProfile(abstract_models.TimeStamped):
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
			

class Person(abstract_models.TimeStamped):
	fname = models.CharField(max_length=NAME_LENGTH)
	lname = models.CharField(max_length=NAME_LENGTH)
	portrait_url = models.CharField(max_length=URL_LENGTH)
	wikipedia_url = models.CharField(max_length=URL_LENGTH)
	bio_summary = models.TextField()

	
class Organization(abstract_models.TimeStamped):
	short_name = models.CharField(max_length=64)
	legal_name = models.CharField(max_length=128)
	legal_classification = models.CharField(
		max_length=48, choices=LEGAL_CLASSIFICATIONS)
	revenue = models.BigIntegerField()
	operations_summary = models.TextField()


# Rename this "Actor"
class Position(abstract_models.TimeStamped):
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


class Letter(abstract_models.Subscribable):
	parent_letter = models.ForeignKey('self', blank=True, null=True, 
		related_name='resent_letters')
	target = models.ForeignKey(Proposal)
	valence = models.SmallIntegerField(choices=VALENCE_CHOICES)
	user = models.ForeignKey(User)
	score = models.SmallIntegerField(default=1)
	title = models.CharField(max_length=TITLE_LENGTH)
	recipients = models.ManyToManyField(Position, related_name='letters')
	text = models.TextField()

	def get_event_type(self):
		return 'LETTER'

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


class Discussion(abstract_models.ScoredPost, abstract_models.Subscribable):
	target = models.ForeignKey(Proposal, null=True)
	title = models.CharField(max_length=TITLE_LENGTH)
	is_open = models.BooleanField(default=False)

	def get_event_type(self):
		return 'DISCUSSION'

	def __unicode__(self):
		return self.title

	def get_url(self):
		url = reverse('view_discussion', kwargs={'post_id': self.pk})
		return url + slugify(self.title)


class Reply(abstract_models.ScoredPost, abstract_models.Subscribable):
	target = models.ForeignKey(Discussion, null=True, related_name='replies')
	is_open = models.BooleanField(default=False)

	def get_event_type(self):
		return 'REPLY'

	def get_url(self):
		return None

	def __unicode__(self):
		return self.user.username


class Question(abstract_models.ScoredPost, abstract_models.Subscribable):
	title = models.CharField('question title', max_length=TITLE_LENGTH)
	target = models.ForeignKey(Proposal)

	def get_event_type(self):
		return 'QUESTION'	

	def get_url(self):
		url = reverse('view_question', kwargs={'post_id':self.pk})
		return url + slugify(self.title)


class Answer(abstract_models.ScoredPost, abstract_models.Subscribable):
	target = models.ForeignKey(Question, related_name='replies')

	def get_event_type(self):
		return 'ANSWER'

	def get_url(self):
		return None

	def __unicode__(self):
		return self.user.username


# TODO: These Comments should be collapsed into one type, and use a 
#	point-of-connection table (like SubscriptionId) to handle the 
#	type-heterogeneity of their targets

# TODO: This should be renamed "LetterComment"
class Comment(abstract_models.AbstractComment):
	target = models.ForeignKey(Letter, related_name='comment_set')

class QuestionComment(abstract_models.AbstractComment):
	target = models.ForeignKey(Question, related_name='comment_set')
	
class AnswerComment(abstract_models.AbstractComment):
	target = models.ForeignKey(Answer, related_name='comment_set')

class DiscussionComment(abstract_models.AbstractComment):
	target = models.ForeignKey(Discussion, related_name='comment_set')

class ReplyComment(abstract_models.AbstractComment):
	target = models.ForeignKey(Reply, related_name='comment_set')


# TODO: These Votes should be collapsed into one type, and use a 
#	point-of-connection table (like SubscriptionId) to handle the 
#	type-heterogeneity of their targets
class DiscussionVote(abstract_models.Vote):
	target = models.ForeignKey(Discussion)

	class Meta:
		unique_together = ('user', 'target')

class ProposalVote(abstract_models.Vote):
	target = models.ForeignKey(Proposal)

	class Meta:
		unique_together	= ('user', 'target')

class LetterVote(abstract_models.Vote):
	target = models.ForeignKey(Letter)

	class Meta:
		unique_together = ('user', 'target')

class ReplyVote(abstract_models.Vote):
	target = models.ForeignKey(Reply)

	class Meta:
		unique_together = ('user', 'target')

class QuestionVote(abstract_models.Vote):
	target = models.ForeignKey(Question)

	class Meta:
		unique_together = ('user', 'target')

class AnswerVote(abstract_models.Vote):
	target = models.ForeignKey(Answer)

	class Meta:
		unique_together = ('user', 'target')

class CommentVote(abstract_models.Vote):
	target = models.ForeignKey(Comment)

	class Meta:
		unique_together = ('user', 'target')


