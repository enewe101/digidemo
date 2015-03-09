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
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as __
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.templatetags.staticfiles import static
from digidemo import abstract_models
from digidemo.settings import LANGUAGES
import re
import os


# Constants
NAME_LENGTH = 48
URL_LENGTH = 256
TITLE_LENGTH = 256
EMAIL_LENGTH = 254
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
REASON_CHOICES = (
	('AUTHOR', 'author'),
	('COMMENTER', 'commenter'),
	('SUBSCRIBED', 'actively subscribed'),
	('EDITOR', 'edited related content')
)


# *** All of the Concrete Models Follow *** # 


	# Note, models related to the notification system are defined in 
	# abstract_models.py, even though they are not actually abstract.
	# This is because they are needed to define the abstract models.
	# This includes SubscriptionId, Publication, Subscription, and 
	# Notification.


# This was used on landing page before alpha release.  No longer needed
#
class FeedbackNote(abstract_models.TimeStamped):
    ''' 
        This is for people that sign up for to receive emails on our landing
        page.
    '''
    email = models.EmailField(max_length=EMAIL_LENGTH, 
		verbose_name=_('email'))
    message = models.CharField(max_length="1024", verbose_name=_('message'))



class EmailRecipient(abstract_models.TimeStamped):
	''' 
		This is for people that sign up for to receive emails on our landing
		page.
	'''

	email = models.EmailField(max_length=EMAIL_LENGTH, verbose_name=_('email'))
	active = models.BooleanField(default=True, verbose_name=_('active'))

	class Meta:
		verbose_name = _('user on our email list')
		verbose_name_plural = _('users on our email list')


class PasswordReset(abstract_models.TimeStamped):
	'''
		This is for password reset
	'''
	email = models.EmailField(max_length=EMAIL_LENGTH, verbose_name=_('email'))
	username = models.CharField(max_length=DEFAULT_TEXT_LENGTH, 
		verbose_name=_('username'))

	class Meta:
		verbose_name = _('Password reset request')
		verbose_name_plural = _('Password reset requests')


class Sector(abstract_models.Subscribable):

	# Overriden in Subscribable to prevent auto-subscription
	def get_author(self):
		return None

	# Overridden in TriggersNotification -- we don't want to issue 
	# notifications when users make new tags
	def get_targets(self):
		return []

	short_name = models.CharField(max_length=3, verbose_name=_('short name'))
	name = models.CharField(max_length=64, verbose_name=_('name'))

	def __unicode__(self):
		return self.render()

	def render(self):
		html =  (
			'<div href="' 
				+ reverse('issue_list_sector', 
					kwargs={'sector':self.name, 'order_by':'interesting'})
				+ '" class="sector_tag ' + self.name + '_sector">' 
				+ __(self.name) 
			+ '</div>'
		)

		return mark_safe(html)

	def render_link(self):
		html =  (
			'<a href="' 
				+ reverse('issue_list_sector', 
					kwargs={'sector':self.name, 'order_by':'interesting'})
				+ '" class="sector_tag ' + self.name + '_sector">' 
				+ __(self.name)
			+ '</a>'
		)

		return mark_safe(html)

	class Meta:
		verbose_name = _('sector')
		verbose_name_plural = _('sectors')


class Tag(abstract_models.Subscribable):

	# Overriden in Subscribable to prevent auto-subscription
	def get_author(self):
		return None

	# Overridden in TriggersNotification -- we don't want to issue 
	# notifications when users make new tags
	def get_targets(self):
		return []

	name = models.CharField(max_length=48, verbose_name=_('name'))
	sector = models.ForeignKey(Sector, null=True, verbose_name=('sector'))
	target = models.ForeignKey('self', null=True, verbose_name=('target'))

	def render(self):
		html =  (
			'<div href="' 
				+ reverse('issue_list_tag', 
					kwargs={'tag':self.name, 'order_by':'interesting'})
				+ '" class="tag">' 
				+ self.name 
			+ '</div>'
		)

		return mark_safe(html)

	def render_link(self):
		html =  (
			'<a href="' 
				+ reverse('issue_list_tag', 
					kwargs={'tag':self.name, 'order_by':'interesting'})
				+ '" class="tag">' 
				+ self.name 
			+ '</a>'
		)

		return mark_safe(html)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = _('tag')
		verbose_name_plural = _('tags')


class Proposal(abstract_models.Subscribable):
	is_published = models.BooleanField(default=False, 
		verbose_name=_('is published'))
	score = models.SmallIntegerField(default=0, verbose_name=_('score'))
	title = models.CharField(max_length=256, verbose_name=_('title'))
	summary = models.TextField(verbose_name=_('summary'))
	text = models.TextField(verbose_name=_('text'))
	language = models.CharField(default='en-ca', max_length=5,
		choices=LANGUAGES, verbose_name=_('language'))

	objects = models.Manager()

	# TODO: add (actors) as a many-to-many relationship

	# propogate to creation
	original_user = models.ForeignKey(
		User, related_name='initiated_proposals', 
		verbose_name=_('original author'))
	user = models.ForeignKey(
		User, related_name='proposals_rectently_edited',
		verbose_name=_('last author'))
	proposal_image = models.ImageField(
		upload_to='proposal_avatars',
		default='/digidemo/proposal-images/',
		verbose_name=_('issue image'));
	tags = models.ManyToManyField(
		Tag, related_name='proposals', blank=True, null=True,
		verbose_name=_('tags'))
	sectors = models.ManyToManyField(
		Sector, related_name='proposals', blank=True, null=True,
		verbose_name=_('sectors'))


	def get_event_type(self):

		# Proposals must be saved using save(suppress_publish=True).
		# After saving publish(event_type="ISSUE" | "EDIT") should be called 
		# directly.  This is because the proposal is either being created
		# or edited, but we can't infer that at save() time.
		if not hasattr(self, 'event_type'):
			raise ValueError('Proposals must be saved with' 
				'suppress_publish=True, and then manually published using'
				'proposal.publish(event_type="ISSUE" | "EDIT")'
			)

		return self.event_type

	def get_targets(self):
		sector_targets = [s.subscription_id for s in self.sectors.all()]
		tag_targets = [t.subscription_id for t in self.tags.all()]
		targets = sector_targets + tag_targets

		targets.append(self.subscription_id)

		return targets


	def publish(self, event_type):
		self.event_type=event_type
		super(Proposal, self).publish()


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
		verbose_name = _('issue')
		verbose_name_plural = _('issues')


class ProposalVersion(abstract_models.TimeStamped):
	proposal = models.ForeignKey(Proposal, blank=True, null=True, 
		verbose_name=_('issue'))
	title = models.CharField(max_length=256, verbose_name=_('title'))
	summary = models.TextField(verbose_name=_('summary'))
	text = models.TextField(verbose_name=_('text'))
	user = models.ForeignKey(User, verbose_name=_('user'))
	tags = models.ManyToManyField(
		Tag, related_name='proposal_versions',blank=True, null=True,
		verbose_name=_('tags'))
	sectors = models.ManyToManyField(
		Sector, related_name='proposal_versions', blank=True, null=True,
		verbose_name=_('sectors'))

	class Meta:
		verbose_name = _('issue version')
		verbose_name_plural = _('issue versions')

	@classmethod
	def get_latest(cls, proposal):
		pvs = cls.objects.filter(proposal=proposal).order_by('-creation_date')
		if len(pvs) == 0:
			raise cls.DoesNotExist('There are no proposal versions for that'
				'proposal')

		return pvs[0]


class UserProfile(abstract_models.TimeStamped):
	user = models.OneToOneField(User, related_name='profile', 
		verbose_name=_('user'))
	email_validated = models.BooleanField(default=False, 
		verbose_name=_('email validated'))
	avatar_img = models.ImageField(upload_to='avatars', 
		verbose_name=_('avatar image'))
	rep = models.IntegerField(default=0, verbose_name=_('reputation'))
	street = models.CharField(max_length=128, verbose_name=_('street'))
	zip_code = models.CharField(max_length=10, verbose_name=_('zip_code'))
	country = models.CharField(max_length=64, choices=COUNTRIES, 
		verbose_name=_('country'))
	province = models.CharField(max_length=32, choices=PROVINCES, blank=True, 
		verbose_name=_('province'))
        followedProposals = models.ManyToManyField(Proposal,null=True)
	do_email_news = models.BooleanField(default=True, 
		verbose_name=_('do email news'))
	do_email_responses = models.BooleanField(default=True, 
		verbose_name=_('do email responses'))
	do_email_petitions = models.BooleanField(default=True, 
		verbose_name=_('do email petitions'))
	do_email_watched = models.BooleanField(default=True, 
		verbose_name=_('do email watched'))

	class Meta:
		verbose_name = _('user profile')
		verbose_name_plural = _('user profiles')


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
			

class EmailVerification(abstract_models.TimeStamped):
	user = models.ForeignKey(User, verbose_name=_('user'))
	code = models.CharField(max_length=60, verbose_name=_('code'))

	class Meta:
		verbose_name = _('email verification')
		verbose_name_plural = _('email verifications')

class Person(abstract_models.TimeStamped):
	fname = models.CharField(max_length=NAME_LENGTH, 
		verbose_name=_('first name'))
	lname = models.CharField(max_length=NAME_LENGTH, 
		verbose_name=_('last name'))
	portrait_url = models.CharField(max_length=URL_LENGTH, 
		verbose_name=_('portrait url'))
	wikipedia_url = models.CharField(max_length=URL_LENGTH, 
		verbose_name=_('wikipedia url'))
	bio_summary = models.TextField(verbose_name=_('bio summary'))

	class Meta:
		verbose_name = _('person')
		verbose_name_plural = _('people')
	
class Organization(abstract_models.TimeStamped):
	short_name = models.CharField(max_length=64, verbose_name=_('short name'))
	legal_name = models.CharField(max_length=128, verbose_name=_('legal name'))
	legal_classification = models.CharField(
		max_length=48, choices=LEGAL_CLASSIFICATIONS, 
		verbose_name=_('legal classification'))
	revenue = models.BigIntegerField(verbose_name=_('revenue'))
	operations_summary = models.TextField(verbose_name=_('operations summary'))

	class Meta:
		verbose_name = _('organization')
		verbose_name_plural = _('organizations')


# Rename this "Actor"
class Position(abstract_models.TimeStamped):
	# name of position (i.e. title)
	name = models.CharField(max_length=128, verbose_name=_('name'))

	person = models.ForeignKey(Person, verbose_name=_('person'))
	organization = models.ForeignKey(Organization, 
		verbose_name=_('organization'))
	salary = models.DecimalField(max_digits=11, decimal_places=2, 
		verbose_name=_('salary'))
	telephone = models.CharField(max_length=14, verbose_name=_('telephone'))
	email = models.EmailField(max_length=254, verbose_name=_('email'))
	mandate_summary = models.TextField(verbose_name=_('mandate summary'))

	class Meta:
		verbose_name = _('position')
		verbose_name_plural = _('positions')

	def __unicode__(self):
		return "%s, %s %s" %(self.name, self.person.fname,
			self.person.lname)


class Letter(abstract_models.Subscribable):
	parent_letter = models.ForeignKey('self', blank=True, null=True, 
		verbose_name=_('parent letter'), related_name='resent_letters')
	target = models.ForeignKey(Proposal, verbose_name=_('target'))
	valence = models.SmallIntegerField(choices=VALENCE_CHOICES, null=True, 
		verbose_name=_('valence'))
	user = models.ForeignKey(User, verbose_name=_('user'))
	score = models.SmallIntegerField(default=1, verbose_name=_('score'))
	title = models.CharField(max_length=TITLE_LENGTH, verbose_name=_('title'))
	recipients = models.ManyToManyField(Position, related_name='letters', 
		verbose_name=_('recipients'))
	text = models.TextField(verbose_name=_('text'))

	class Meta:
		verbose_name = _('letter')
		verbose_name_plural = _('letters')

	def get_targets(self):
		targets = [self.target.subscription_id]
		if self.parent_letter is not None:
			targets.append(self.parent_letter.subscription_id)

		return targets

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
	target = models.ForeignKey(Proposal, null=True, verbose_name=_('target'))
	title = models.CharField(max_length=TITLE_LENGTH, verbose_name=_('title'))
	is_open = models.BooleanField(default=True, verbose_name=_('is open'))

	class Meta:
		verbose_name = _('discussion')
		verbose_name_plural = _('discussions')

	def get_event_type(self):
		return 'DISCUSSION'

	def __unicode__(self):
		return self.title

	def get_url(self):
		url = reverse('view_discussion', kwargs={'post_id': self.pk})
		return url + slugify(self.title)


class Reply(abstract_models.ScoredPost, abstract_models.Subscribable):
	target = models.ForeignKey(Discussion, null=True, related_name='replies', 
		verbose_name=_('target'))
	is_open = models.BooleanField(default=False, verbose_name=_('is open'))

	class Meta:
		verbose_name = _('reply')
		verbose_name_plural = _('replies')

	def get_event_type(self):
		return 'REPLY'

	def get_url(self):
		return self.target.get_url()

	def __unicode__(self):
		return self.user.username


class Question(abstract_models.ScoredPost, abstract_models.Subscribable):
	title = models.CharField(max_length=TITLE_LENGTH, 
		verbose_name=_('title'))
	target = models.ForeignKey(Proposal, verbose_name=_('target'))

	class Meta:
		verbose_name = _('question')
		verbose_name_plural = _('questions')

	def get_event_type(self):
		return 'QUESTION'	

	def get_url(self):
		url = reverse('view_question', kwargs={'post_id':self.pk})
		return url + slugify(self.title)


class Answer(abstract_models.ScoredPost, abstract_models.Subscribable):
	target = models.ForeignKey(Question, related_name='replies', 
		verbose_name=_('target'))

	class Meta:
		verbose_name = _('answer')
		verbose_name_plural = _('answers')

	def get_event_type(self):
		return 'ANSWER'

	def get_url(self):
		return self.target.get_url()

	def __unicode__(self):
		return self.user.username


# TODO: These Comments should be collapsed into one type, and use a 
#	point-of-connection table (like SubscriptionId) to handle the 
#	type-heterogeneity of their targets

# TODO: This should be renamed "LetterComment"
class Comment(abstract_models.AbstractComment):
	target = models.ForeignKey(Letter, related_name='comment_set', 
		verbose_name=_('target'))

	class Meta:
		verbose_name = _('comment')
		verbose_name_plural = _('comments')

class QuestionComment(abstract_models.AbstractComment):
	target = models.ForeignKey(Question, related_name='comment_set', 
		verbose_name=_('target'))

	class Meta:
		verbose_name = _('comment')
		verbose_name_plural = _('comments')
	
class AnswerComment(abstract_models.AbstractComment):
	target = models.ForeignKey(Answer, related_name='comment_set', 
		verbose_name=_('target'))

	class Meta:
		verbose_name = _('comment')
		verbose_name_plural = _('comments')
	
class DiscussionComment(abstract_models.AbstractComment):
	target = models.ForeignKey(Discussion, related_name='comment_set', 
		verbose_name=_('target'))

	class Meta:
		verbose_name = _('comment')
		verbose_name_plural = _('comments')
	
class ReplyComment(abstract_models.AbstractComment):
	target = models.ForeignKey(Reply, related_name='comment_set', 
		verbose_name=_('target'))

	class Meta:
		verbose_name = _('comment')
		verbose_name_plural = _('comments')
	

# TODO: These Votes should be collapsed into one type, and use a 
#	point-of-connection table (like SubscriptionId) to handle the 
#	type-heterogeneity of their targets
class DiscussionVote(abstract_models.Vote):
	target = models.ForeignKey(Discussion, verbose_name=_('target'))

	class Meta:
		unique_together = ('user', 'target')
		verbose_name = _('vote')
		verbose_name_plural = _('vote')

class ProposalVote(abstract_models.Vote):
	target = models.ForeignKey(Proposal, verbose_name=_('target'))

	class Meta:
		unique_together	= ('user', 'target')
		verbose_name = _('vote')
		verbose_name_plural = _('vote')

class LetterVote(abstract_models.Vote):
	target = models.ForeignKey(Letter, verbose_name=_('target'))

	class Meta:
		unique_together = ('user', 'target')
		verbose_name = _('vote')
		verbose_name_plural = _('vote')

class ReplyVote(abstract_models.Vote):
	target = models.ForeignKey(Reply, verbose_name=_('target'))

	class Meta:
		unique_together = ('user', 'target')
		verbose_name = _('vote')
		verbose_name_plural = _('vote')

class QuestionVote(abstract_models.Vote):
	target = models.ForeignKey(Question, verbose_name=_('target'))

	class Meta:
		unique_together = ('user', 'target')
		verbose_name = _('vote')
		verbose_name_plural = _('vote')

class AnswerVote(abstract_models.Vote):
	target = models.ForeignKey(Answer, verbose_name=_('target'))

	class Meta:
		unique_together = ('user', 'target')
		verbose_name = _('vote')
		verbose_name_plural = _('vote')

class CommentVote(abstract_models.Vote):
	target = models.ForeignKey(Comment, verbose_name=_('target'))

	class Meta:
		unique_together = ('user', 'target')
		verbose_name = _('vote')
		verbose_name_plural = _('vote')


