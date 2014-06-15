from django.db import models
from digidemo.util import PROVINCES, COUNTRIES, get_choice


class User(models.Model):
	email = models.EmailField(max_length=254)
	email_validated = models.BooleanField(default=False)
	avatar_img = models.ImageField(upload_to='avatars')
	avatar_name = models.CharField(max_length=48)
	fname = models.CharField(max_length=48)
	lname = models.CharField(max_length=48)
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
	
	def __unicode__(self):
		return self.title

	class Meta:
		get_latest_by = 'creation_date'


VALENCE_CHOICES = [
	(-1, 'oppose'),
	(0, 'ammend'),
	(1, 'support'),
]


class Letter(models.Model):
	proposal = models.ForeignKey(Proposal)
	valence = models.SmallIntegerField(default=1, choices=VALENCE_CHOICES)
	sender = models.ForeignKey(User)
	resenders = models.ManyToManyField(User, related_name='resent_letters')
	body = models.TextField()
	score = models.SmallIntegerField(default=0)

	def __unicode__(self):
		return "%s-%s" %(
			self.sender.avatar_name,
			get_choice(VALENCE_CHOICES, self.valence))


class Comment(models.Model):
	author = models.ForeignKey(User)
	letter = models.ForeignKey(Letter)
	body = models.CharField(max_length=512)
	score = models.SmallIntegerField(default=0)

	def __unicode__(self):
		return self.author.avatar_name


