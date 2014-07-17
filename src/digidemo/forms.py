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
import os

log_fname = os.path.join(PROJECT_DIR, 'media/~log.txt')
logging.basicConfig(filename=log_fname, level=logging.DEBUG)


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
				auto_id = kwargs.pop('auto_id', default_class_name + '_%s')

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

@bound_form()
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

	def __init__(self, proposal):

		if proposal is None:
			return

		# get a form to edit the proposal, i.e. create a proposal version
		self.proposal_version = ProposalVersionForm.init_from_object(
			proposal.get_latest(),
			endpoint=proposal.get_url('edit')
		)

		#   ** we'll be making formsets factor adding/editing/deleting **

		# Get the factors associated to the proposal as two lists
		(pos_factor_versions, neg_factor_versions,
			pos_factors, neg_factors) = self._get_and_split_factors(proposal)

		# make initial data arguments to prepopulate the factor forms 
		# based on the existing factors
		factor_version_inits = {
			'pos': self._get_init_from_objects(pos_factor_versions),
			'neg': self._get_init_from_objects(neg_factor_versions)
		}

		# get the formsets for factors
		self.factor_formsets = {
			'pos': self._get_formsets_from_init(
				'pos', 
				factor_version_inits['pos'],
				pos_factors
			),
			'neg': self._get_formsets_from_init(
				'neg', 
				factor_version_inits['neg'],
				neg_factors
			)
		}

		# get the formset managers
		self.factor_form_managers = {
			'pos' : self.factor_formsets['pos'].management_form,
			'neg' : self.factor_formsets['neg'].management_form
		}

		# This is an unbound (but prepopulated) form
		self.is_bound = False


	@classmethod
	def from_data(cls, data):
		'''
		this is an alternative constructor for making a bound EditProposalForm
		from submitted data
		'''

		instance = cls(None)
		instance._init_from_data(data)
		return instance


	def _init_from_data(self, data):

		# make the formset for the proposal version based on POSTed data
		self.proposal_version = ProposalVersionForm(data)

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


	def _get_and_split_factors(self, proposal):

		proposal_version = proposal.get_latest()

		pos_factors = (
			Factor.objects
			.filter(version__proposal_version=proposal_version)
			.filter(version__valence__gt=0)
			.order_by('version__pk')
		)
		neg_factors = (
			Factor.objects
			.filter(version__proposal_version=proposal_version)
			.filter(version__valence__lt=0)
			.order_by('version__pk')
		)

		pos_factor_versions = (
			FactorVersion.objects
			.filter(proposal_version=proposal_version)
			.filter(valence__gt=0)
			.order_by('pk')
		)
		neg_factor_versions = (
			FactorVersion.objects
			.filter(proposal_version=proposal_version)
			.filter(valence__lt=0)
			.order_by('pk')
		)


		return (pos_factor_versions, neg_factor_versions, 
			pos_factors, neg_factors)


	def is_valid(self):

		return True

		if not self.is_bound:
			return True 

		# validate the proposal version
		is_valid = self.proposal_version.is_valid()

		# validate the positive factors formset
		pos_formset_pairs = self.edit_factor['pos']['formset']
		is_valid = is_valid and self.validate_farmset_pair(pos_formset_pairs)

		# validate the negative factors formset
		neg_formset_pairs = self.edit_factor['neg']['formset']
		is_valid = is_valid and self.validate_farmset_pair(neg_formset_pairs)

		return is_valid


	def validate_formset_pair(formset_pair):

		# valid till proven invalid
		is_valid = True

		for f_pair in formset_pair:
			is_valid = (
				is_valid 
				and f_pair['delete'].is_valid() 
				and f_pair['version'].is_valid()
			)

		return is_valid


	def save(self):
		# self.proposal_version.save()
		print 'save positive factors'
		self._save_factors(self.factor_formsets['pos'])
		print 'save negative factors'
		self._save_factors(self.factor_formsets['neg'])

	
	def _save_factors(self, factor_formsets):

		pass
#		for f_pair in factor_pairs:
#
#			# if the delete checkbox is ticked, delete this
#			if f_pair['delete'].cleaned_data['DELETE']:
#				f_pair['delete'].save()
#				continue
#
#			print 'delete: ' + str(f_pair['delete'].is_valid())
#			try:
#				print f_pair['delete'].cleaned_data
#			except AttributeError:
#				pass
#
#			print 'version: ' + str(f_pair['version'].is_valid())
#			try:
#				print f_pair['version'].cleaned_data
#			except AttributeError:
#				pass


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


	def _get_formsets_from_init(
		self, prefix, factor_version_inits, factors):

		# Here is the formset for editing factor versions
		FactorVersionFormSet = formset_factory(FactorVersionForm, extra=1)
		factor_version_formset = FactorVersionFormSet(
			initial=factor_version_inits, prefix=prefix
		)

		return factor_version_formset


	def _get_init_from_objects(self, factor_versions):

		factor_version_inits = []

		for fv in factor_versions:
			factor = fv.factor

			factor_version_inits.append({
				'factor':factor.pk, 
				'proposal_version': None,
				'description':fv.description,
				'valence': fv.valence,
				'sector': fv.sector
			})

		
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
        street = forms.CharField(max_length = 32)
        zipCode = forms.CharField(max_length = 8)
        country = forms.CharField(max_length = 20)
        province = forms.CharField(max_length = 30)

