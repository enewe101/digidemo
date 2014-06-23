from django.db import models
from digidemo.choices import *


NAME_LENGTH = 48
URL_LENGTH = 256


VALENCE_CHOICES = [
	(-1, 'oppose'),
	(0, 'ammend'),
	(1, 'support'),
]

VOTE_CHOICES = [
	(-1, 'down vote'),
	(1, 'up vote'),
]

FACTOR_CHOICES = [
	(-1, 'risk'),
	(1, 'benefit')
]


class Sector(models.Model):
	short_name = models.CharField(max_length=3)
	name = models.CharField(max_length=64)


class User(models.Model):
	email = models.EmailField(max_length=254)
	email_validated = models.BooleanField(default=False)
	avatar_img = models.ImageField(upload_to='avatars')
	avatar_name = models.CharField(max_length=NAME_LENGTH)
	fname = models.CharField(max_length=NAME_LENGTH)
	lname = models.CharField(max_length=NAME_LENGTH)
	rep = models.IntegerField(default=0)
	street = models.CharField(max_length=128)
	zip_code = models.CharField(max_length=10)
	country = models.CharField(max_length=64, choices=COUNTRIES)
	province = models.CharField(max_length=32, choices=PROVINCES, blank=True)

	def __unicode__(self):
		return self.avatar_name


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
	
	def __unicode__(self):
		return self.title

	class Meta:
		get_latest_by = 'creation_date'


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
	valence = models.SmallIntegerField(default=1, choices=VALENCE_CHOICES)
	sender = models.ForeignKey(User)
	resenders = models.ManyToManyField(User, related_name='resent_letters')
	body = models.TextField()
	recipients = models.ManyToManyField(Position, related_name='letters')
	score = models.SmallIntegerField(default=0)

	def __unicode__(self):
		return "%s-%s" %(
			self.sender.avatar_name,
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
		return self.author.avatar_name



