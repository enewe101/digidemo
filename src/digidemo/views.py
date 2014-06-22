from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from digidemo.models import *
from digidemo.forms import *



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


	letter_form = LetterForm()

	return render(
		request,
		'digidemo/proposal.html', 
		{
			'proposal': this_proposal,
			'comment_form': comment_form,
			'letter_form': letter_form,
			'logged_in_user': logged_in_user,
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
		{'valid':valid}
	)


def test(request):
	return render(request, 'digidemo/test.html', {})

