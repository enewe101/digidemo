from django.db import models
from digidemo.choices import *
from django.contrib.auth.models import User
from django.utils import timezone 
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
import re

NAME_LENGTH = 48
URL_LENGTH = 256
TITLE_LENGTH = 256
DEFAULT_COMMENT_LENGTH = 512
DEFAULT_TEXT_LENGTH = 65536

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


class ScoredComment(TimeStamped):
	user = models.ForeignKey(User)
	score = models.SmallIntegerField(default=0, editable=False)
	text = models.CharField(max_length=DEFAULT_COMMENT_LENGTH)

	def __unicode__(self):
		return self.text[:20]

	class Meta:
		abstract = True


class ScoredPost(TimeStamped):
	user = models.ForeignKey(User)
	score = models.SmallIntegerField(default=0, editable=False)
	title = models.CharField(max_length=TITLE_LENGTH)
	text = models.TextField(max_length=DEFAULT_TEXT_LENGTH)

	def __unicode__(self):
		return self.title[:20]

	class Meta:
		abstract = True


class ScoredReply(TimeStamped):
	user = models.ForeignKey(User)
	score = models.SmallIntegerField(default=0, editable=False)
	text = models.TextField(max_length=DEFAULT_TEXT_LENGTH)

	def __unicode__(self):
		return self.text[:20]

	class Meta:
		abstract = True


class Sector(TimeStamped):
	short_name = models.CharField(max_length=3)
	name = models.CharField(max_length=64)

	def __unicode__(self):
		return self.short_name


class UserProfile(TimeStamped):
	user = models.OneToOneField(User, related_name='profile')
	email_validated = models.BooleanField(default=False)
	avatar_img = models.ImageField(upload_to='avatars')
	rep = models.IntegerField(default=0)
	street = models.CharField(max_length=128)
	zip_code = models.CharField(max_length=10)
	country = models.CharField(max_length=64, choices=COUNTRIES)
	province = models.CharField(max_length=32, choices=PROVINCES, blank=True)
	
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


class Tag(TimeStamped):
	name = models.CharField(max_length=48)

	def __unicode__(self):
		return self.name

class Proposal(TimeStamped):
	is_published = models.BooleanField(default=False)
	score = models.SmallIntegerField(default=0)
	title = models.CharField(max_length=256)
	summary = models.TextField()
	text = models.TextField()

	# propogate to creation
	original_user = models.ForeignKey(
		User, related_name='initiated_proposals')
	user = models.ForeignKey(
		User, related_name='proposals_rectently_edited') 
	proposal_image = models.ImageField(
		upload_to='proposal_avatars',default='/digidemo/proposal-images/');
	tags = models.ManyToManyField(
		Tag, related_name='proposals', blank=True, null=True)

	def get_latest(self):
		return ProposalVersion.get_latest(self)

	def __unicode__(self):
		return self.title

	def get_url(self, view_name):
		url_stub = reverse(view_name, kwargs={'proposal_id': self.pk})
		return url_stub + slugify(self.title)

	def get_overview_url(self):
		return self.get_url('overview')

	def get_question_url(self):
		return self.get_url('ask_question')

	def get_question_list_url(self):
		return self.get_url('proposal_question_list')

	def get_discussion_url(self):
		return self.get_url('discussion')

	def get_edit_url(self):
		return self.get_url('edit')

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

	@classmethod
	def get_latest(cls, proposal):
		pvs = cls.objects.filter(proposal=proposal).order_by('-creation_date')
		if len(pvs) == 0:
			raise cls.DoesNotExist('There are no proposal versions for that'
				'proposal')

		return pvs[0]


class Discussion(TimeStamped):
	proposal = models.ForeignKey(Proposal)
	title = models.CharField(max_length=TITLE_LENGTH)
	body = models.TextField()
	user = models.ForeignKey(User)
	score = models.SmallIntegerField(default=0)
	is_open = models.BooleanField(default=False)

	def __unicode__(self):
		return self.title



class Reply(TimeStamped):
	discussion = models.ForeignKey(Discussion)
	body = models.TextField()
	user = models.ForeignKey(User)
	score = models.SmallIntegerField(default=0)
	is_open = models.BooleanField(default=False)

	def __unicode__(self):
		return self.user.username


class Question(ScoredPost):
	proposal = models.ForeignKey(Proposal)

	def get_url(self):
		url = reverse('view_question', kwargs={'question_id':self.pk})
		return url + slugify(self.title)


class QuestionComment(ScoredComment):
	question = models.ForeignKey(Question)
	

class Answer(ScoredReply):
	question = models.ForeignKey(Question)


class AnswerComment(ScoredComment):
	answer = models.ForeignKey(Answer)


class Factor(TimeStamped):
	proposal = models.ForeignKey(Proposal)
	description = models.CharField(max_length=256)
	valence = models.SmallIntegerField(choices=FACTOR_CHOICES)
	sector = models.ForeignKey(Sector)
	deleted = models.BooleanField('delete')


	def __unicode__(self):
		latest = self.get_latest()
		return '%s %d' % (str(latest.sector), latest.valence)

	def get_latest(self):
		return FactorVersion.get_latest(self)


class FactorVersion(TimeStamped):
	factor = models.ForeignKey(
		Factor, related_name='version', blank=True, null=True)
	proposal_version = models.ForeignKey(
		ProposalVersion, blank=True, null=True)
	description = models.CharField(max_length=256)
	valence = models.SmallIntegerField(choices=FACTOR_CHOICES)
	sector = models.ForeignKey(Sector)
	deleted = models.BooleanField('delete')

	def __unicode__(self):
		return self.description[:14]

	@classmethod
	def get_latest(cls, factor):

		factor_versions = cls.objects.filter(
			factor=factor).order_by('-creation_date')

		if len(factor_versions) == 0:
			raise cls.DoesNotExist('There are no proposal versions for that'
				'proposal')

		return factor_versions[0]


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


class Letter(TimeStamped):
	parent_letter = models.ForeignKey('self', blank=True, null=True)
	proposal = models.ForeignKey(Proposal)
	valence = models.SmallIntegerField(choices=VALENCE_CHOICES)
	user = models.ForeignKey(User)
	body = models.TextField()
	recipients = models.ManyToManyField(Position, related_name='letters')
	score = models.SmallIntegerField(default=0)

	def __unicode__(self):
		return "%s-%s" %(
			self.sender.username,
			get_choice(VALENCE_CHOICES, self.valence))


class Comment(TimeStamped):
	user = models.ForeignKey(User)
	letter = models.ForeignKey(Letter)
	body = models.CharField(max_length=512)
	score = models.SmallIntegerField(default=0)

	def __unicode__(self):
		return self.author.username


class Vote(TimeStamped):
	user = models.ForeignKey(User)
	valence = models.SmallIntegerField(choices=VOTE_CHOICES)

	class Meta:
		abstract=True

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

class CommentVote(Vote):
	target = models.ForeignKey(Comment)

	class Meta:
		unique_together = ('user', 'target')

