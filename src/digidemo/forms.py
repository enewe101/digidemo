from django.forms import ModelForm 
from django import forms
from digidemo.models import *

class LetterCommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['body', 'author', 'letter']
		widgets = {
			'body': forms.Textarea(attrs={'class':'letter_comment_input'}),
			'author': forms.HiddenInput(), 
			'letter': forms.HiddenInput(),
		}
	
class LetterForm(ModelForm):
	class Meta:
		model = Letter
		fields = [
			'proposal', 'valence', 'sender', 'body', 'recipients',
		]
		widgets = {
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
			'user': forms.TextInput(),
			'letter': forms.TextInput(),
			'valence': forms.TextInput(),
		}

	class Media:
		js = ('digidemo/js/vote_form.js',)

