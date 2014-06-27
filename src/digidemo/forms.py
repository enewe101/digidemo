from django.utils.translation import ugettext as _
from django.db import models
from django.forms import ModelForm 
from django import forms
from digidemo.models import *


def ajax_form(endpoint=None, form_id=None, form_class='ajax_form'):
	'''
	A class decorator factory for turning a MyFormClass into an ajax-ready
	form.  This is a 'decorator facory' so it needs to be actually *called*
	when decorating your class:

	@ajax_form()
	class MyFormClass(ModelForm):
		...

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

				self.form_id = kwargs.pop('form_id', form_id)
				self.form_class = kwargs.pop('form_class', form_class)
				super(NewClass, self).__init__(*args, **kwargs)

		return NewClass
	return class_decorator


class LetterCommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['body', 'author', 'letter']
		widgets = {
			'body': forms.Textarea(attrs={'class':'letter_comment_input'}),
			'author': forms.HiddenInput(), 
			'letter': forms.HiddenInput(),
		}
	
VALENCE_CHOICES = [
	(1, 'support'),
	(-1, 'oppose'),
	(0, 'ammend'),
]


@ajax_form('send_letter', 'send_letter_form')
class LetterForm(ModelForm):
	class Meta:
		model = Letter
		fields = [
			'parent_letter', 'proposal', 'sender', 'valence', 'recipients', 
			'body'
		]
		widgets = {
			'parent_letter': forms.HiddenInput(),
			'proposal': forms.HiddenInput(),
			'sender': forms.HiddenInput(),
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
	



class ProposalVoteForm(ModelForm):
	def __init__(self, *args, **kwargs):

		self.form_id = 'proposal_vote_%d' % kwargs.pop('form_id', 0)
		self.cur_score = kwargs.pop('cur_score', 0)
		self.endpoint = kwargs.pop('endpoint', 'vote_proposal')

		super(ProposalVoteForm, self).__init__(*args, **kwargs)


	class Meta:
		model = ProposalVote
		fields = ['user', 'proposal', 'valence']

		widgets = {
			'user': forms.HiddenInput(),
			'proposal': forms.HiddenInput(),
			'valence': forms.HiddenInput(),
		}

	class Media:
		js = ('digidemo/js/vote_form.js',)


class LetterVoteForm(ModelForm):

	def __init__(self, *args, **kwargs):

		self.form_id = 'letter_vote_%d' % kwargs.pop('form_id', 0)
		self.cur_score = kwargs.pop('cur_score', 0)
		self.endpoint = kwargs.pop('endpoint', 'vote_letter')
		super(LetterVoteForm, self).__init__(*args, **kwargs)


	class Meta:
		model = LetterVote
		fields = ['user', 'letter', 'valence']

		widgets = {
			'user': forms.HiddenInput(),
			'letter': forms.HiddenInput(),
			'valence': forms.HiddenInput(),
		}

	class Media:
		js = ('digidemo/js/vote_form.js',)




