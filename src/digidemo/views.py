from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from digidemo.models import *
from digidemo.forms import *
from digidemo.utils import get_or_none


def proposal(request, proposal_name):

	this_proposal = Proposal.objects.get(name=proposal_name)

	# ** Hardcoded the logged in user to be enewe101 **
	logged_in_user = User.objects.get(pk=2)

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


	proposal_vote = get_or_none(
		ProposalVote, user=logged_in_user, proposal=this_proposal)

	if proposal_vote:
		proposal_vote_form = ProposalVoteForm(
			instance=proposal_vote,
			cur_score=this_proposal.score)

	else:
		proposal_vote_form = ProposalVoteForm(
			initial={'user':logged_in_user.pk, 'proposal':this_proposal.pk},
			cur_score=this_proposal.score)

	letter_sections = []
	letters = Letter.objects.filter(proposal=this_proposal)
	for letter_num, letter in enumerate(letters):

		letter_vote = get_or_none(
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


		letter_sections.append({
			'letter': letter,
			'comment_form': LetterCommentForm(
				initial={'user':logged_in_user.pk, 'letter':letter.pk}),
			'vote_form': letter_vote_form
		}) 
	
	media = ProposalVoteForm().media
	media += LetterVoteForm().media

	letter_form = LetterForm(initial={
		'proposal': this_proposal.pk,
		'sender': logged_in_user,
	})

	return render(
		request,
		'digidemo/proposal.html', 
		{
			'proposal': this_proposal,
			'comment_form': comment_form,
			'letter_form': letter_form,
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

