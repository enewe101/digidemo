from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from digidemo.models import *
from digidemo.forms import LetterCommentForm



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


	return render(
		request,
		'digidemo/proposal.html', 
		{
			'proposal': this_proposal,
			'comment_form': comment_form,
			'logged_in_user': logged_in_user,
		}
	)


def test(request):
	return render(request, 'digidemo/test.html', {})

