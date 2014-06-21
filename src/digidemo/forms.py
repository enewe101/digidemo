from django.forms import ModelForm 
from django import forms
from digidemo.models import *

class LetterCommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['body', 'author', 'letter']
		widgets = {
			'author': forms.HiddenInput(), 
			'letter': forms.HiddenInput(),
		}
	
