import logging
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

#log_fname = os.path.join(PROJECT_DIR, 'media/~log.txt')
#logging.basicConfig(filename=log_fname, level=logging.DEBUG)


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

				# We're going to make a dict of all fields and there errors
				# it will be exaustive (empty lists appear for fields without
				# erorrs.  First, get an empty error dict with all fields:
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


			@classmethod
			def init_from_object(cls, obj, *args, **kwargs):
				if obj is None:
					return cls(*args, **kwargs)

				initial = {}
				for field in cls.Meta.fields:
					try:
						field_val = getattr(obj, field)
						initial[field] = field_val
					except AttributeError:
						pass

				return cls(initial=initial, *args, **kwargs)


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
	logging.debug(form_class_name)
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


@bound_form()
class QuestionForm(ModelForm):
	class Meta:
		model = Question
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

@bound_form('send_letter')
class LetterForm(ModelForm):

	recipients = forms.ModelMultipleChoiceField(
		queryset=Position.objects.all())
		

	class Meta:
		model = Letter
		fields = [
			'parent_letter', 'proposal', 'user', 'valence', 'recipients', 
			'body'
		]
		widgets = {
			'parent_letter': forms.HiddenInput(),
			'proposal': forms.HiddenInput(),
			'user': forms.HiddenInput(),
			'body': forms.Textarea(attrs={'class':'letter_body_textarea'})
		}


# Note: don't decorate -- inherits from LetterForm which was already decorated
class ResendLetterForm(LetterForm):

	recipients = forms.ModelMultipleChoiceField(
		queryset=Position.objects.all())

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
			'proposal': forms.HiddenInput(),
			'user': forms.HiddenInput(),
			'sender': forms.HiddenInput(),
			'body': forms.Textarea(attrs={'class':'letter_body_textarea'})
		}
	


@bound_form()
class ProposalVersionForm(ModelForm):
	class Meta:
		model = ProposalVersion
		fields = [
			'proposal', 'title', 'summary', 'text', 'user','tags'
		]
		widgets = {
			'proposal': forms.HiddenInput(),
			'user': forms.HiddenInput(),
			'title': forms.TextInput(),
			'summary': forms.Textarea(),
			'text': forms.Textarea(),
                        'tags':forms.Textarea(),
		}
		


class EditProposalForm(object):

	'''
	this is an aggregator for a set of forms that together enable editing
	of a proposal (i.e. create a new proposal, or a new *version* of an
	existing proposal).  Note that it only aggregates Forms, it does not 
	itself subclass Form
	'''

	def __init__(self, proposal=None, data=None, *args, **kwargs):

		if proposal is not None:
			self._init_with_proposal(proposal, *args, **kwargs)

		elif data is not None:
			self._init_with_data(data, *args, **kwargs)

		else:
			self._init_blank(*args, **kwargs)


	def _init_blank(self, endpoint, initial=None, num_factors=3):

		# set some form-wide attributes
		self.form_class = self.__class__.__name__
		self.endpoint = endpoint

		# get a form to edit the proposal, i.e. create a proposal version
		self.proposal_version_form = ProposalVersionForm(initial=initial)

		# This is an unbound (but prepopulated) form
		self.is_bound = False


	def _init_with_proposal(self, proposal, endpoint):

		# get ahold of the proposal and its latest version
		self.proposal = proposal
		self.proposal_version = proposal.get_latest()

		# Set some form-wide attributes
		self.endpoint = endpoint
		self.form_class = self.__class__.__name__

		# get a form to edit the proposal, i.e. create a proposal version
		self.proposal_version_form = ProposalVersionForm.init_from_object(
			self.proposal_version,
		)

		# This is an unbound (but prepopulated) form
		self.is_bound = False


	def _init_with_data(self, data, endpoint):

		# Set some form-wide attributes
		self.endpoint = endpoint
		self.form_class = self.__class__.__name__


		# make the formset for the proposal version based on POSTed data
		self.proposal_version_form = ProposalVersionForm(data)

		# this is a bound form!
		self.is_bound = True


	def is_valid(self):

		if not self.is_bound:
			return True 

                if len(self.proposal_version_form.errors) == 1 :
                        if self.proposal_version_form.errors.keys()[0] == 'tags':
                                return True
                else: 
                        return self.proposal_version_form.is_valid()


	def save(self):

		# If the proposal version isn't bound to a proposal, we are making
		# a brand new proposal
		if self.proposal_version_form.cleaned_data['proposal'] is None:

			# Make the new proposal
			proposal_init = utils.extract_dict(
				self.proposal_version_form.cleaned_data,
				['title', 'summary', 'text', 'user']
			)
			proposal_init['original_user'] = proposal_init['user']
			self.proposal = Proposal(**proposal_init)
                        self.proposal.save()
			
			# Bind it to the proposal version and save the proposal version
			proposal_init.pop("original_user", None)
                        new_proposal_version = ProposalVersion(**proposal_init);
		#	new_proposal_version = self.proposal_version_form.save(
                #			commit=False)
			new_proposal_version.proposal = self.proposal
			new_proposal_version.save()

                        #Used for spliiting and saving the tags
			allTags = self.proposal_version_form.data['tags'].split(',');

                        print self.proposal_version_form.data['tags']
                        
                        for eachTag in allTags:
                                try :
                                        tag = Tag.objects.get(name=eachTag);
                                except:
                                        tag = Tag(name=eachTag)
                                        tag.save();
                                self.proposal.tags.add(tag);
                                new_proposal_version.tags.add(tag);
			
			self.proposal.save()
			new_proposal_version.save()

		# Otherwise, we are not making a new proposal, only saving a new
		# proposal version
		else:

			# Update the values in the Proposal which mirror the 
			# ProposalVersion
			self.proposal = self.proposal_version_form.cleaned_data['proposal']
			for field in ['title', 'summary', 'text', 'user']:
				setattr(self.proposal, field,
					self.proposal_version_form.cleaned_data[field])
				
			self.proposal.save()

			
                        proposal_init = utils.extract_dict(
				self.proposal_version_form.cleaned_data,
				['title', 'summary', 'text', 'user']
			)
			# and of course, save the ProposalVersion
			new_proposal_version = ProposalVersion(**proposal_init);
                        new_proposal_version.proposal = self.proposal
			new_proposal_version.save()

                        #Used for splitting and saving all the tags
        		allTags = self.proposal_version_form.data['tags'].split(',');
                        for eachTag in allTags:
                                try :
                                        tag = Tag.objects.get(name=eachTag);
                                except:
                                        tag = Tag(name=eachTag)
                                        tag.save();
                                self.proposal.tags.add(tag);
                                new_proposal_version.tags.add(tag);
			
			self.proposal.save()
			new_proposal_version.save()

		# Finally, return a reference to the proposal
		return self.proposal

	






class VoteForm(ModelForm):
	def __init__(self, *args, **kwargs):
		self.cur_score = kwargs.pop('cur_score', 0)
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


class NameForm(forms.Form):
        userName = forms.CharField(label='UserName', max_length=16)
        password = forms.CharField(label='Password',widget=forms.PasswordInput())
        email = forms.EmailField(label='Email')
        firstName =  forms.CharField(max_length = 16)
        lastName = forms.CharField(max_length = 32)
#        street = forms.CharField(max_length = 32)
#        zipCode = forms.CharField(max_length = 8)
#        country = forms.CharField(max_length = 20)
#        province = forms.CharField(max_length = 30)


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
