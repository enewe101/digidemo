from django.core.urlresolvers import reverse
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from digidemo.models import *
from digidemo.forms import *
from digidemo import utils
from settings import DEBUG
import json

def get_django_vars(additional_vars={}):
	django_vars = {
		'DEBUG': DEBUG
	}

	django_vars.update(additional_vars)

	return django_vars


def get_django_vars_JSON(additional_vars):
	return json.dumps(get_django_vars(additional_vars))


def proposal(request, proposal_name):

	this_proposal = Proposal.objects.get(name=proposal_name)

	# ** Hardcoded the logged in user to be enewe101 **
	logged_in_user = User.objects.get(pk=1)
	

	# if this is a form submission, handle it
	if request.method == 'POST':
		comment_form = LetterCommentForm(request.POST)
		if comment_form.is_valid():
			comment_form.save()
			return HttpResponseRedirect(
				reverse('proposal', kwargs={'proposal_name':proposal_name})
			)

	# otherwise make a comment form
	else:
		comment_form = LetterCommentForm()


	proposal_vote = utils.get_or_none(
		ProposalVote, user=logged_in_user, proposal=this_proposal)

	if proposal_vote:
		proposal_vote_form = ProposalVoteForm(
			instance=proposal_vote,
			cur_score=this_proposal.score)

	else:
		proposal_vote_form = ProposalVoteForm(
			initial={'user':logged_in_user.pk, 'proposal':this_proposal.pk},
			cur_score=this_proposal.score)

	# Get all of the letters which are associated with this proposal
	# and which are 'original letters'
	letter_sections = []
	letters = Letter.objects.filter(parent_letter=None, proposal=this_proposal)
	for letter_num, letter in enumerate(letters):

		# make a voting form for each letter
		letter_vote = utils.get_or_none(
			LetterVote, user=logged_in_user, letter=letter)

		if letter_vote:
			letter_vote_form = LetterVoteForm(
				instance=letter_vote,
				form_id=letter_num, cur_score=letter.score)
		else:
			letter_vote_form = LetterVoteForm(
				initial={'user':logged_in_user.pk, 'letter':letter.pk},
				form_id=letter_num,
				cur_score=letter.score
			)

		# make a re-sending form for each letter
		resend_form = ResendLetterForm(
			initial={
				'parent_letter': letter,
				'proposal': this_proposal,
				'body': letter.body,
				'recipients': letter.body,
				'sender': logged_in_user,
				'valence': letter.valence
			}, 
			form_id='resend_letter_%d' %letter_num,
		   	endpoint='resend_letter',
			form_class='resend_letter_form'
		)

		letter_sections.append({
			'letter': letter,
			'comment_form': LetterCommentForm(
				initial={'user':logged_in_user.pk, 'letter':letter.pk}),
			'vote_form': letter_vote_form,
			'resend_form': resend_form
		}) 
	
	media = ProposalVoteForm().media
	media += LetterVoteForm().media

	add_letter_form = LetterForm(initial={
		'proposal': this_proposal,
		'sender': logged_in_user,
	}, form_id='add_letter', form_class='add_letter')

	return render(
		request,
		'digidemo/proposal.html', 
		{
			'django_vars_js': get_django_vars_JSON(
				{'user': utils.obj_to_dict(
				logged_in_user, exclude=['password'])}),
			'proposal': this_proposal,
			'comment_form': comment_form,
			'letter_form': add_letter_form,
			'letter_sections': letter_sections,
			'logged_in_user': logged_in_user,
			'proposal_vote_form': proposal_vote_form,
			'media': media,
		}
	)


def send_letter(request):

	if request.method == 'POST':
		letter_form = LetterForm(request.POST)

		if letter_form.is_valid():
			valid = "True"
			letter_form.save()

		else:
			valid = "False"

	return render(
		request,
		'digidemo/send_letter.html', 
		{'valid':letter_form.errors}
	)


def test(request):
	return render(request, 'digidemo/test.html', {})

