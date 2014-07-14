import logging
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from django.db import models
from django.forms import Form, ModelForm 
from django import forms
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

