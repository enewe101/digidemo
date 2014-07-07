from django.db import models
from digidemo.choices import *
from django.contrib.auth.models import User


NAME_LENGTH = 48
URL_LENGTH = 256
TITLE_LENGTH = 256

class Sector(models.Model):
	short_name = models.CharField(max_length=3)
	name = models.CharField(max_length=64)


class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True, related_name='profile')
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




class Proposal(models.Model):
	name = models.CharField(max_length=256)
	title = models.CharField(max_length=256)
	text = models.TextField()
	is_published = models.BooleanField(default=False)
	last_modified = models.DateField(auto_now=True)
	creation_date = models.DateField()
	author = models.ForeignKey(User)
	score = models.SmallIntegerField(default=0)
	sector = models.ManyToManyField(Sector, related_name='proposals')
	proposal_image = models.ImageField(upload_to='proposal_avatars',default='/digidemo/proposal-images/');
	
	def __unicode__(self):
		return self.title

	class Meta:
		get_latest_by = 'creation_date'


class Discussion(models.Model):
	proposal = models.ForeignKey(Proposal)
	title = models.CharField(max_length=TITLE_LENGTH)
	body = models.TextField()
	user = models.ForeignKey(User)
	score = models.SmallIntegerField(default=0)
	is_open = models.BooleanField(default=False)
	creation_date = models.DateField(auto_now_add=True)
	last_activity_date = models.DateField(auto_now=True)

	def __unicode__(self):
		return self.title


class DiscussionVote(models.Model):
	user = models.ForeignKey(User)
	discussion = models.ForeignKey(Discussion)
	valence = models.SmallIntegerField(choices=VOTE_CHOICES)

	class Meta:
		unique_together	= ('user', 'discussion')


class Reply(models.Model):
	discussion = models.ForeignKey(Discussion)
	body = models.TextField()
	user = models.ForeignKey(User)
	score = models.SmallIntegerField(default=0)
	is_open = models.BooleanField(default=False)
	creation_date = models.DateField(auto_now_add=True)

	def __unicode__(self):
		return self.user.username



class ProposalVote(models.Model):
	user = models.ForeignKey(User)
	proposal = models.ForeignKey(Proposal)
	valence = models.SmallIntegerField(choices=VOTE_CHOICES)

	class Meta:
		unique_together	= ('user', 'proposal')


class Capability(models.Model):
	name = models.CharField(max_length=64)
	description = models.CharField(max_length=512)
	sector = models.ForeignKey(Sector)


class Factor(models.Model):
	proposal = models.ForeignKey(Proposal)
	description = models.CharField(max_length=256)
	capability = models.ForeignKey(Capability)
	valence = models.SmallIntegerField(choices=FACTOR_CHOICES)


class Person(models.Model):
	fname = models.CharField(max_length=NAME_LENGTH)
	lname = models.CharField(max_length=NAME_LENGTH)
	portrait_url = models.CharField(max_length=URL_LENGTH)
	wikipedia_url = models.CharField(max_length=URL_LENGTH)
	bio_summary = models.TextField()

	
class Organization(models.Model):
	short_name = models.CharField(max_length=64)
	legal_name = models.CharField(max_length=128)
	legal_classification = models.CharField(
		max_length=48, choices=LEGAL_CLASSIFICATIONS)
	revenue = models.BigIntegerField()
	operations_summary = models.TextField()


class Position(models.Model):
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


class Letter(models.Model):
	parent_letter = models.ForeignKey('self', blank=True, null=True)
	proposal = models.ForeignKey(Proposal)
	valence = models.SmallIntegerField(choices=VALENCE_CHOICES)
	sender = models.ForeignKey(User)
	body = models.TextField()
	recipients = models.ManyToManyField(Position, related_name='letters')
	score = models.SmallIntegerField(default=0)

	def __unicode__(self):
		return "%s-%s" %(
			self.sender.username,
			get_choice(VALENCE_CHOICES, self.valence))


class LetterVote(models.Model):
	user = models.ForeignKey(User)
	letter = models.ForeignKey(Letter)
	valence = models.SmallIntegerField(choices=VOTE_CHOICES)

	class Meta:
		unique_together = ('user', 'letter')


class Comment(models.Model):
	author = models.ForeignKey(User)
	letter = models.ForeignKey(Letter)
	body = models.CharField(max_length=512)
	score = models.SmallIntegerField(default=0)

	def __unicode__(self):
		return self.author.username



