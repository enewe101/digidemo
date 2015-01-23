import logging
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from django.db import models
from django.forms import Form, ModelForm 
from django import forms
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from digidemo.choices import *
from digidemo.models import *
from digidemo.settings import PROJECT_DIR
from digidemo import utils
import os


USERNAME_MAX_LENGTH = 32
PASSWORD_MAX_LENGTH = USERNAME_MAX_LENGTH
PASSWORD_MIN_LENGTH = 8

class AugmentedFormMixin(object):

	endpoint = None
	class_name = None

	def __init__(self, *args, **kwargs):

		# allow specifying the endpoint for the form.  This is the
		# form action ( <form action=... ), or ajax endpoint (ajax.py)
		self.endpoint = kwargs.pop('endpoint', self.endpoint)

		# The form gets a class name ( <form class=... )
		default_class_name = self.class_name or self.__class__.__name__
		self.form_class = kwargs.pop('form_class', default_class_name)

		# An id-prefix can optionally be specified.  This changes the
		# html id attribute form elements, but not the name attribute
		self.id_prefix = kwargs.pop('id_prefix', '')

		default_auto_id = self.form_class + '_' + str(self.id_prefix)

		# Customize the forms auto_id 
		auto_id = kwargs.pop('auto_id', default_auto_id + '_%s')

		# The form's fields automatically get classes too, based on
		# the forms class and the fields name
		auto_add_input_class(self.form_class, self)

		# now call the usual form constructor
		super(AugmentedFormMixin, self).__init__(
			*args, auto_id=auto_id, **kwargs)


	def get_endpoint(self):
		# if none is supplied, theres no default, so an endpoint
		# *must be provided
		if self.endpoint is None:
			raise ValueError("No endpoint is bound to this form")

		return self.endpoint


	def json_errors(self):

		# We're going to make a dict of all fields and their errors
		# it will be exaustive (empty lists appear for fields without
		# errors.  First, get an empty error dict with all fields:
		all_fields = dict([(field.name, []) for field in self])

		# Now we get the fields that actually have some errors
		error_dict = {}
		for field, error_list in self.errors.items():
			field_id = field
			# field_id = self[field].id_for_label
			error_dict[field_id] = list(error_list)

		# mix them together before returning
		all_fields.update(error_dict)
		return all_fields



def bound_form(endpoint=None, class_name=None):
	'''
	A class decorator for turning SomeFormClass into an ajax-ready form.  

	`endpoint` should be a string corresponding to an ajax handler in the 
	namespace of the ajax.py module.

	An ajax_form can be rendered in a page by including the 
	_w_ajax_form.html template.  This template needs the template variables
	`form` to be set to an ajax_form instance.  It also needs a variable
	`include_id` to provide a unique string or number.  The include_id only
	has to be unique among instances of that kind of form on the page.  If
	there is only one form, it can be ommitted.

	E.g.:
		{% include "digidemo/_w_ajax_form with form=some_form include_id=4 %}

	This template will create a submit button for the form, and will bind a
	click event on the submit button to an ajax POST of the form to endpoint.

	The ajax form gets registered as a widget with the widgets manager.
	It's widget_class is the name of the form class (e.g. SomeFormClass), and 
	the widget_id is the class plus an underscore and the include_id
	(e.g. SomeFormClass_4).  

	Note: if the include_id was ommitted, the widget id would be 
		`SomeFormClass_`.

	The endpoint and the form_class can be overridden for instances, assigning 
	to the keywords `endpoint` or `form_class` when constructing the form.
	'''

	def class_decorator(cls):
		class AugmentedForm(cls):
			error_css_class = 'error'

			def __init__(self, *args, **kwargs):

				# allow specifying the endpoint for the form.  This is the
				# form action ( <form action=... ), or ajax endpoint (ajax.py)
				self.endpoint = kwargs.pop('endpoint', endpoint)

				# The form gets a class name ( <form class=... )
				default_class_name = class_name or cls.__name__
				self.form_class = kwargs.pop('form_class', default_class_name)

				# An id-prefix can optionally be specified.  This changes the
				# html id attribute form elements, but not the name attribute
				self.id_prefix = kwargs.pop('id_prefix', '')

				default_auto_id = self.form_class + '_' + str(self.id_prefix)

				# Customize the forms auto_id 
				auto_id = kwargs.pop('auto_id', default_auto_id + '_%s')

				# The form's fields automatically get classes too, based on
				# the forms class and the fields name
				auto_add_input_class(self.form_class, self)

				# now call the usual form constructor
				super(AugmentedForm, self).__init__(
					*args, auto_id=auto_id, **kwargs)


			def get_endpoint(self):
				# if none is supplied, theres no default, so an endpoint
				# *must be provided
				if self.endpoint is None:
					raise ValueError("No endpoint is bound to this form")

				return self.endpoint


			def json_errors(self):

				# We're going to make a dict of all fields and their errors
				# it will be exaustive (empty lists appear for fields without
				# errors.  First, get an empty error dict with all fields:
				all_fields = dict([(field.name, []) for field in self])

				# Now we get the fields that actually have some errors
				error_dict = {}
				for field, error_list in self.errors.items():
					field_id = field
					# field_id = self[field].id_for_label
					error_dict[field_id] = list(error_list)

				# mix them together before returning
				all_fields.update(error_dict)
				return all_fields



		return AugmentedForm
	return class_decorator


def auto_add_input_class(form_class_name, form_instance):
	'''
	Add an html class to the widget html for all the widgets listed in a 
	form's Meta.widgets dictionary.

	The html class is made from the form's class and the widget's field name
	e.g. If a CommentForm has a widget for the field `body`, the widget
	html would look like:
		<textarea class="CommentForm_body" ...

	'''
	for field in form_instance.Meta.fields:

		# for each field, get the widget
		try:
			attrs = form_instance.Meta.widgets[field].attrs
		except KeyError:
			continue

		# for each widget, get the html class attributed to it (if any)
		if 'class' in attrs:
			css_classes = attrs['class'] + ' '
		else:
			css_classes = ''

		# add an auto-generated class to the widget html's class
		if form_class_name not in css_classes:
			css_classes += form_class_name + '_' + field
			attrs['class'] = css_classes


class EmailSignupForm(ModelForm):
	form_class = 'signup_form'
	class Meta:
		model = EmailRecipient
		fields = ['email']
		widgets = {
			'email': forms.EmailInput()
		}


@bound_form('answer')
class AnswerForm(ModelForm):
	class Meta:
		model = Answer
		fields = ['target', 'user', 'text']
		widgets = {
			'target': forms.HiddenInput(),
			'user': forms.HiddenInput(),
			'text': forms.Textarea()
		}


class QuestionForm(AugmentedFormMixin, ModelForm):
	class Meta:
		model = Question
		fields = ['target', 'user', 'title', 'text']
		widgets = {
			'target': forms.HiddenInput(),
			'user': forms.HiddenInput(),
			'title': forms.TextInput(),
			'text': forms.Textarea()
		}


@bound_form()
class DiscussionForm(ModelForm):
	class Meta:
		model = Discussion
		fields = ['target', 'user', 'title', 'text']
		widgets = {
			'target': forms.HiddenInput(),
			'user': forms.HiddenInput(),
			'title': forms.TextInput(),
			'text': forms.Textarea()
		}


@bound_form('reply')
class ReplyForm(ModelForm):
	class Meta:
		model = Reply
		fields = ['text', 'user', 'target']
		widgets = {
			'text': forms.Textarea(attrs={'class':'reply_input'}),
			'user': forms.HiddenInput(), 
			'target': forms.HiddenInput(),
		}
	

class CommentForm(ModelForm):
	class Meta:
		fields = ['text', 'user', 'target']
		widgets = {
			'text': forms.Textarea(attrs={'class':'letter_comment_input'}),
			'user': forms.HiddenInput(), 
			'target': forms.HiddenInput(),
		}


@bound_form('answer_comment')
class AnswerCommentForm(CommentForm):
	class Meta(CommentForm.Meta):
		model = AnswerComment
	
@bound_form('question_comment')
class QuestionCommentForm(CommentForm):
	class Meta(CommentForm.Meta):
		model = QuestionComment

	
@bound_form('comment')
class LetterCommentForm(CommentForm):
	class Meta(CommentForm.Meta):
		model = Comment

@bound_form('discussion_comment')
class DiscussionCommentForm(CommentForm):
	class Meta(CommentForm.Meta):
		model= DiscussionComment

@bound_form('reply_comment')
class ReplyCommentForm(CommentForm):
	class Meta(CommentForm.Meta):
		model= ReplyComment

class LetterForm(AugmentedFormMixin, ModelForm):

	endpoint = 'send_letter'

	recipients = forms.ModelMultipleChoiceField(
		widget=forms.CheckboxSelectMultiple(), 
		queryset=Position.objects.all())
		
	class Meta:
		model = Letter
		fields = [
			'parent_letter', 'target', 'user', 'valence', 'title', 
			'recipients', 'text'
		]
		widgets = {
			'parent_letter': forms.HiddenInput(),
			'target': forms.HiddenInput(),
			'user': forms.HiddenInput(),
			'title': forms.TextInput(),
			'recipients': forms.CheckboxSelectMultiple(),
			'text': forms.Textarea(attrs={'class':'letter_body_textarea'})
		}


# Note: don't decorate -- inherits from LetterForm which was already decorated
class ResendLetterForm(LetterForm):

	endpoint = 'resend_letter'

	def clean(self):

		# Check that the resent letter has the same valence as the original
		expected_valence = self.cleaned_data['parent_letter'].valence
		if self.cleaned_data['valence'] != expected_valence:
			raise forms.ValidationError(
				_('Resent letter must have same valence as original letter'),
				code='wrongValence'
			)

		return self.cleaned_data

	class Meta(LetterForm.Meta):
		widgets = {
			'valence': forms.HiddenInput(),
			'parent_letter': forms.HiddenInput(),
			'target': forms.HiddenInput(),
			'user': forms.HiddenInput(),
			'sender': forms.HiddenInput(),
			'title': forms.TextInput(),
			'recipients': forms.CheckboxSelectMultiple(),
			'text': forms.Textarea(attrs={'class':'letter_body_textarea'})
		}
	


# TODO: seem to be losing the original user during save
class ProposalVersionForm(AugmentedFormMixin, ModelForm):
	class Meta:
		model = ProposalVersion
		fields = [
			'proposal', 'title', 'summary', 'text', 'user', 'sectors'
		]
		widgets = {
			'proposal': forms.HiddenInput(),
			'user': forms.HiddenInput(),
			'title': forms.TextInput(),
			'summary': forms.Textarea(),
			'text': forms.Textarea(),
			'sectors': forms.CheckboxSelectMultiple()
		}


	def save(self, commit=True):

		# If the proposal version isn't bound to a proposal, we are making
		# a brand new proposal
		if self.cleaned_data['proposal'] is None:

			# Copy data from the proposal_version, 
			# which is used to make the proposal itself
			proposal_init = utils.extract_dict(
				self.cleaned_data,
				['title', 'summary', 'text', 'user']
			)

			# In proposal, we also have a field called original user
			proposal_init['original_user'] = proposal_init['user']

			# now make the proposal and save it
			self.proposal = Proposal(**proposal_init)
			self.proposal.save()

			# now save the proposal version, then bind the proposal and 
			# then save the bound proposal_version
			new_proposal_version = super(ProposalVersionForm, self).save(
				commit=False)
			new_proposal_version.proposal = self.proposal
			new_proposal_version.save()

			# Finally copy the sectors to the saved proposal and 
			# proposal_version
			for sector in self.cleaned_data['sectors']:
				new_proposal_version.sectors.add(sector)
				self.proposal.sectors.add(sector)

		# Otherwise, we editing an existing proposal proposal, by saving a new
		# proposal version
		else:

			# Update the values in the Proposal which mirror the 
			# ProposalVersion.  Since this is an edit, there is already
			# a proposal bound to the form, get it, then update values.
			self.proposal = self.cleaned_data['proposal']
			for field in ['title', 'summary', 'text', 'user']:
				setattr(self.proposal, field, self.cleaned_data[field])

			self.proposal.save()

			# Save a new proposal version based on the contents of this form
			new_proposal_version = super(ProposalVersionForm, self).save()

			# We also need to manually copy over the sectors.
			# First, clear any existing ones from the proposal (this makes
			# deletion of sectors possible)
			self.proposal.sectors.clear()
			for sector in self.cleaned_data['sectors']:
				new_proposal_version.sectors.add(sector)
				self.proposal.sectors.add(sector)

		# Finally, return a reference to the proposal
		return new_proposal_version


class TaggedProposalForm(object):

	# tags can consist of letters, numbers, and hyphens
	# a valid list of tags has at least one tag (containing at least one
	# of the above characters, followed by any number of tags separated by
	# commas
	valid_tags_re = re.compile(r'^[-a-zA-Z0-9]+(,[-a-zA-Z0-9]+)*$')

	def __init__(self, initial=None, data=None, endpoint=None):

		self.tag_errors = ''
		self.taggit = {
			'id': 'proposal_tags',
			'tags': '',
			'label': 'tags',
			'name': 'tags',
			'errors': []
		}

		if data is not None:

			self.taggit['tags'] = data['tags']
			self.proposal_version_form = ProposalVersionForm(
				data, endpoint=endpoint)

		elif initial is not None:

			self.taggit['tags'] = initial.pop('tags', '')
			self.proposal_version_form = ProposalVersionForm(
				initial=initial, endpoint=endpoint)

		else:
			self.proposal_version_form = ProposalVersionForm(
				endpoint=endpoint)


	def is_valid(self):

		valid = self.proposal_version_form.is_valid()

		if self.valid_tags_re.match(self.taggit['tags']) is None:

			if self.taggit['tags'].strip() == '':
				self.taggit['errors'].append(
					'Please include at least one tag.')

			else: 
				self.taggit['errors'].append('Tags should contain only '\
					'letters, numbers and hyphens.')
			
			valid = False

		else:
			self.tags = self.taggit['tags'].split(',')

		return valid


	def save(self):

		proposal_version = self.proposal_version_form.save()
		proposal = proposal_version.proposal

		# we will clear the current tags, then add the ones that were
		# actually sent in the form.  This means that if the user deleted
		# tags, they will actually be deleted on the proposal
		proposal.tags.clear()

		for tag_name in self.tags:

			tag, created = Tag.objects.get_or_create(name=tag_name)

			proposal_version.tags.add(tag)
			proposal.tags.add(tag)

		return proposal_version
	





class VoteForm(ModelForm):
	def __init__(self, *args, **kwargs):
		self.cur_score = kwargs.pop('cur_score', 0)
		self.is_enabled = kwargs.pop('is_enabled', False)
		self.tooltip = kwargs.pop('tooltip', 'You must login to vote!')

		super(VoteForm, self).__init__(*args, **kwargs)

	class Meta:
		fields = ['user', 'target', 'valence']
		widgets = {
			'user': forms.HiddenInput(),
			'target': forms.HiddenInput(),
			'valence': forms.HiddenInput(),
		}


@bound_form('vote_proposal')
class ProposalVoteForm(VoteForm):
	class Meta(VoteForm.Meta):
		model = ProposalVote


@bound_form('vote_letter')
class LetterVoteForm(VoteForm):
	class Meta(VoteForm.Meta):
		model = LetterVote


@bound_form('vote_answer')
class AnswerVoteForm(VoteForm):
	class Meta(VoteForm.Meta):
		model = AnswerVote


@bound_form('vote_question')
class QuestionVoteForm(VoteForm):
	class Meta(VoteForm.Meta):
		model = QuestionVote

@bound_form('vote_discussion')
class DiscussionVoteForm(VoteForm):
	class Meta(VoteForm.Meta):
		model = DiscussionVote

@bound_form('vote_reply')
class ReplyVoteForm(VoteForm):
	class Meta(VoteForm.Meta):
		model = ReplyVote


class LoginForm(AugmentedFormMixin, Form):
	endpoint = 'ajax_login'
	username = forms.CharField(max_length=USERNAME_MAX_LENGTH)
	password = forms.CharField(
		widget=forms.PasswordInput(), max_length=PASSWORD_MAX_LENGTH)

	class Meta:
		fields = ['username', 'password']
		widgets = {
			'password': forms.PasswordInput()
		}


class UserRegisterForm(AugmentedFormMixin, ModelForm):
	confirm_password = forms.CharField(
			widget=forms.PasswordInput(), max_length=PASSWORD_MAX_LENGTH)

	class Meta:
		model = User
		fields = [
				'first_name', 'last_name', 'username', 'email', 'password',
				'confirm_password'
			]
		widgets = {
			'first_name': forms.TextInput(),
			'last_name': forms.TextInput(),
			'username': forms.TextInput(),
			'email': forms.EmailInput(),
			'password': forms.PasswordInput(),
		}


	def clean(self):
		cleaned = super(UserRegisterForm, self).clean()
		pwd1 = cleaned['password']
		pwd2 = cleaned['confirm_password']

		pwd_too_short = len(pwd1) < PASSWORD_MIN_LENGTH
		pwd_no_match = pwd1 != pwd2

		if pwd_too_short:
			self._errors['password'] = self.error_class(
				["Password too short"])

		if pwd_no_match:
			if 'password' in self._errors:
				self._errors['password'].append("Passwords didn't match!")
			else:
				self._errors['password'] = self.error_class(
					["Passwords didn't match!"])

		if pwd_no_match or pwd_too_short:
			del cleaned['password']
			del cleaned['confirm_password']

		return cleaned


from haystack.forms import SearchForm

class ProposalSearchForm(SearchForm):

    def no_query_found(self):
        return self.searchqueryset.all()

    def search(self):
        # First, store the SearchQuerySet received from other processing. (the main work is run internally by Haystack here).
        sqs = super(ProposalSearchForm, self).search()

        # if something goes wrong
        if not self.is_valid():
            return self.no_query_found()

        # you can then adjust the search results and ask for instance to order the results by title
        

        return sqs
