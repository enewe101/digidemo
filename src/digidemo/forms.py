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
		class NewClass(cls):
			def __init__(self, *args, **kwargs):

				# allow specifying the endpoint for the form.  This is the
				# form action ( <form action=... ), or ajax endpoint (ajax.py)
				self.endpoint = kwargs.pop('endpoint', endpoint)

				# The form gets a class name ( <form class=... )
				default_class_name = class_name or cls.__name__
				self.form_class = kwargs.pop('form_class', default_class_name)

				# Customize the forms auto_id 
				auto_id = kwargs.pop('auto_id', self.form_class + '_%s')

				# The form's fields automatically get classes too, based on
				# the forms class and the fields name
				auto_add_input_class(self.form_class, self)

				# now call the usual form constructor
				super(NewClass, self).__init__(
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
				all_fields = dict([(field.id_for_label, []) for field in self])

				# Now we get the fields that actually have some errors
				error_dict = {}
				for field, error_list in self.errors.items():
					field_id = self[field].id_for_label
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


		return NewClass
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
		fields = ['body', 'user', 'discussion']
		widgets = {
			'body': forms.Textarea(attrs={'class':'reply_input'}),
			'user': forms.HiddenInput(), 
			'discussion': forms.HiddenInput(),
		}
	


@bound_form('comment')
class LetterCommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['body', 'user', 'letter']
		widgets = {
			'body': forms.Textarea(attrs={'class':'letter_comment_input'}),
			'user': forms.HiddenInput(), 
			'letter': forms.HiddenInput(),
		}
	


@bound_form('send_letter')
class LetterForm(ModelForm):
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


@bound_form()
class ProposalVersionForm(ModelForm):
	class Meta:
		model = ProposalVersion
		fields = [
			'proposal', 'title', 'summary', 'text', 'user'
		]
		widgets = {
			'proposal': forms.HiddenInput(),
			'user': forms.HiddenInput(),
			'title': forms.TextInput(),
			'summary': forms.Textarea(),
			'text': forms.Textarea(),
		}


@bound_form()
class FactorForm(ModelForm):
	class Meta:
		model = Factor
		fields = ['proposal']
		widgets = {
			'proposal': forms.HiddenInput()
		}

class FactorVersionForm(ModelForm):

	class Meta:
		model = FactorVersion
		fields = [
			'factor', 'proposal_version', 'valence', 'deleted', 'sector', 'description'
		]
		widgets = {
			'factor': forms.HiddenInput(),
			'proposal_version': forms.HiddenInput(),
			'valence': forms.HiddenInput(),
			'deleted': forms.CheckboxInput(),
			'sector': forms.Select(),
			'description': forms.Textarea()
		}


class EditProposalForm(object):

	'''
	this is an aggregator for a set of forms that together enable editing
	of a proposal: its versions, its factors, and factor versions.  Note that
	it only aggregates Forms, it does not itself subclass Form
	'''

	def __init__(self, proposal=None, data=None, *args, **kwargs):

		if proposal is not None:
			self._init_with_proposal(proposal, *args, **kwargs)

		elif data is not None:
			self._init_with_data(data, *args, **kwargs)

		else:
			self._init_blank(*args, **kwargs)


	def _init_blank(self, endpoint, initial=None, num_factors=3):

		# get ahold of the proposal and its latest version
		#self.proposal = proposal
		#self.proposal_version = proposal.get_latest()

		# set some form-wide attributes
		self.form_class = self.__class__.__name__
		self.endpoint = endpoint

		# get a form to edit the proposal, i.e. create a proposal version
		self.proposal_version_form = ProposalVersionForm(initial=initial)

		#   ** we'll be making formsets for adding factors **

		# make initial data arguments to prepopulate the factor forms 
		# based on the existing factors
		factor_version_inits = self._get_blank_factor_inits(num_factors)

		# get the formsets for factors
		self.factor_formsets = {
			'pos': self._get_formsets_from_init(
				'pos', 
				factor_version_inits['pos']
			),
			'neg': self._get_formsets_from_init(
				'neg', 
				factor_version_inits['neg']
			)
		}

		# get the formset managers
		self.factor_form_managers = {
			'pos' : self.factor_formsets['pos'].management_form,
			'neg' : self.factor_formsets['neg'].management_form
		}

		# This is an unbound (but prepopulated) form
		self.is_bound = False


	def _init_with_proposal(self, proposal, endpoint, num_factors=1):

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


		#   ** we'll be making formsets factor adding/editing/deleting **

		# Get the factors associated to the proposal as two lists
		(pos_factor_versions, neg_factor_versions,
			pos_factors, neg_factors) = self._get_and_split_factors()

		# make initial data arguments to prepopulate the factor forms 
		# based on the existing factors
		factor_version_inits = {
			'pos': self._get_init_from_objects(
				pos_factor_versions, 1, num_factors),
			'neg': self._get_init_from_objects(
				neg_factor_versions, -1, num_factors)
		}

		# get the formsets for factors
		self.factor_formsets = {
			'pos': self._get_formsets_from_init(
				'pos', 
				factor_version_inits['pos']
			),
			'neg': self._get_formsets_from_init(
				'neg', 
				factor_version_inits['neg']
			)
		}

		# get the formset managers
		self.factor_form_managers = {
			'pos' : self.factor_formsets['pos'].management_form,
			'neg' : self.factor_formsets['neg'].management_form
		}

		# This is an unbound (but prepopulated) form
		self.is_bound = False


	def _init_with_data(self, data, endpoint):

		# Set some form-wide attributes
		self.endpoint = endpoint
		self.form_class = self.__class__.__name__


		# make the formset for the proposal version based on POSTed data
		self.proposal_version_form = ProposalVersionForm(data)

		# get the formsets for factors
		self.factor_formsets = {
			'pos': self._get_formsets_from_data('pos', data),
			'neg': self._get_formsets_from_data('neg', data)
		}

		# get the formset managers
		self.factor_form_managers = {
			'pos' : self.factor_formsets['pos'].management_form,
			'neg' : self.factor_formsets['neg'].management_form
		}

		# this is a bound form!
		self.is_bound = True


	def _get_and_split_factors(self):

		pos_factors = (
			Factor.objects
			.filter(
				version__proposal_version=self.proposal_version,
				version__valence__gt=0,
				version__deleted=False)
			.order_by('version__pk')
		)
		neg_factors = (
			Factor.objects
			.filter(
				version__proposal_version=self.proposal_version,
				version__valence__lt=0,
				version__deleted=False)
			.order_by('version__pk')
		)

		pos_factor_versions = (
			FactorVersion.objects
			.filter(
				proposal_version=self.proposal_version,
				valence__gt=0,
				deleted=False)
			.order_by('pk')
		)
		neg_factor_versions = (
			FactorVersion.objects
			.filter(proposal_version=self.proposal_version,
				valence__lt=0,
				deleted=False)
			.order_by('pk')
		)


		return (pos_factor_versions, neg_factor_versions, 
			pos_factors, neg_factors)


	def is_valid(self):

		if not self.is_bound:
			return True 

		# validate the proposal version
		is_valid = self.proposal_version_form.is_valid()

		# validate the positive factors formset
		is_valid = self._validate_factors(
			self.factor_formsets['pos']) and is_valid

		# validate the negative factors formset
		is_valid = self._validate_factors(
			self.factor_formsets['neg']) and is_valid

		return is_valid


	def _validate_factors(self, formset):

		# valid till proven invalid
		is_valid = True

		for form in formset:

			# Don't validate forms marked as deleted.  Dealing with forms
			# marked for delete is NOT delegated to the FactorVersionForm
			if form['deleted'].value():
				continue

			# Also don't validate "add-forms" that are blank
			# "add-forms" are factor forms for adding a new factor rather than
			# editing an existing one.  They are recognizable because they
			# have no value for `factor`
			is_add_form = not bool(form['factor'].value())
			is_blank = not (form['description'].value()
					and form['description'].value().strip())
			if is_add_form and is_blank:
				continue
					
			# otherwise, we need to validate
			is_valid = form.is_valid() and is_valid

		return is_valid


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
			new_proposal_version = self.proposal_version_form.save(
				commit=False)
			new_proposal_version.proposal = self.proposal
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

			# and of course, save the ProposalVersion
			new_proposal_version = self.proposal_version_form.save()

		# Now save the factors
		self._save_factors(self.factor_formsets['pos'], new_proposal_version)
		self._save_factors(self.factor_formsets['neg'], new_proposal_version)

		# Finally, return a reference to the proposal
		return self.proposal

	
	def _save_factors(self, factor_formsets, proposal_version):
		for form in factor_formsets:

			# if the form is an add-factor form
			if form['factor'].value() == '':

				# and if the description isn't blank, and its not marked delete
				not_blank = (form['description'].value()
						and form['description'].value().strip())
				is_deleted = form['deleted'].value()
				if not_blank and not is_deleted:

					# make a new factor entry (points to proposal) 
					new_factor_data = utils.extract_dict(form.cleaned_data,
						['description', 'valence', 'sector', 'deleted'])
					new_factor = Factor(**new_factor_data)
					new_factor.proposal = self.proposal
					new_factor.save()

					# and a new factorVersion entry (points to 
					# factor and proposal_version
					new_factor_version = form.save(commit=False)
					new_factor_version.factor=new_factor
					new_factor_version.proposal_version = proposal_version
					new_factor_version.save()
					
			# otherwise its an edit-factor form
			else:

				factor = Factor.objects.get(pk=form['factor'].value())

				# if the factor is deleted, don't take values from the form.  
				# Just duplicate the previous factor version and mark deleted
				if form['deleted'].value():

					# Make sure that the factor mirrors the latest 
					# FactorVersion content
					factor.deleted=True
					factor.save()

					factor_version = factor.get_latest()
					factor_version.pk=None	# lets us save the same data as new
											# entry
					factor_version.deleted=True
					factor_version.save()

				# make a new factor version point it to the 
				# same factor, but to the proposal version
				else:

					# make the new factor version
					new_factor_version = form.save(commit=False)
					new_factor_version.proposal_version = proposal_version
					new_factor_version.save()

					# update the factor to mirror factor_version content
					fields = ['description', 'valence', 'sector', 'deleted']
					for field in fields:
						setattr(factor, field, 
							getattr(new_factor_version, field))

					factor.save()



	def _get_formsets_from_data(self, prefix, data):

		# make the formset classes
		FactorVersionFormSet = formset_factory(FactorVersionForm)

		# Make the formsets
		factor_version_formset = FactorVersionFormSet(
			prefix=prefix, data=data)

		return factor_version_formset


	def _get_factor_form_pairs(self, delete, version):

		pairs = zip(version, delete)

		formset_pairs = [{'version':f[0], 'delete':f[1]} for f in pairs]
		return formset_pairs


	def _get_management_forms(self, factor_formsets):

		factor_form_managers = {
			'pos' : {
				'version': factor_formsets['pos']['version'].management_form,
				'delete': factor_formsets['pos']['delete'].management_form
			},
			'neg' : {
				'version': factor_formsets['neg']['version'].management_form,
				'delete': factor_formsets['neg']['delete'].management_form
			}
		}
	
		return factor_form_managers


	def _get_formsets_from_init(self, prefix, factor_version_inits):

		# Here is the formset for editing factor versions
		FactorVersionFormSet = formset_factory(FactorVersionForm, extra=0)
		factor_version_formset = FactorVersionFormSet(
			initial=factor_version_inits, prefix=prefix
		)

		return factor_version_formset


	def _get_blank_factor_inits(self, num_factors):
		return {
			'pos': [{'valence':1} for i in range(num_factors)],
			'neg': [{'valence':-1} for i in range(num_factors)],
		}


	def _get_init_from_objects(self, factor_versions, valence, num_extra=1):

		factor_version_inits = []

		for fv in factor_versions:
			factor = fv.factor

			factor_version_inits.append({
				'factor':factor.pk, 
				'description':fv.description,
				'valence': fv.valence,
				'sector': fv.sector
			})

		# add `num_extra` number of extra forms
		factor_version_inits.extend(
			[{'valence': valence} for i in range(num_extra)]
		)
		
		return factor_version_inits



class ResendLetterForm(LetterForm):

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
			'sender': forms.HiddenInput(),
			'body': forms.Textarea(attrs={'class':'letter_body_textarea'})
		}
	


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
