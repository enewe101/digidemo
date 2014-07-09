from django.utils.translation import ugettext as _
from django.db import models
from django.forms import ModelForm 
from django import forms
from digidemo.choices import *
from digidemo.models import *


def ajax_form(endpoint):
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

				self.endpoint = kwargs.pop('endpoint', endpoint)

				if self.endpoint is None:
					raise ValueError("You must provide a function name "
						"(string) to the keyword argument `endpoint` since "
						"this form has no default endpoint")

				if not isinstance(self.endpoint, basestring):
					raise ValueError("`endpoint` must be a string "
						"representing the name of an ajax endpoint.")

				self.form_class = kwargs.pop('form_class', cls.__name__)
				super(NewClass, self).__init__(*args, **kwargs)

		return NewClass
	return class_decorator



@ajax_form('reply')
class ReplyForm(ModelForm):
	class Meta:
		model = Reply
		fields = ['body', 'user', 'discussion']
		widgets = {
			'body': forms.Textarea(attrs={'class':'reply_input'}),
			'user': forms.HiddenInput(), 
			'discussion': forms.HiddenInput(),
		}
	


@ajax_form('comment')
class LetterCommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['body', 'user', 'letter']
		widgets = {
			'body': forms.Textarea(attrs={'class':'letter_comment_input'}),
			'user': forms.HiddenInput(), 
			'letter': forms.HiddenInput(),
		}
	


@ajax_form('send_letter')
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


@ajax_form('vote_proposal')
class ProposalVoteForm(VoteForm):
	class Meta(VoteForm.Meta):
		model = ProposalVote


@ajax_form('vote_letter')
class LetterVoteForm(VoteForm):
	class Meta(VoteForm.Meta):
		model = LetterVote


@ajax_form('vote_discussion')
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

