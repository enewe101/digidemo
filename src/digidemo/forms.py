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
		}
