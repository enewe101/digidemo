import json
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from digidemo.models import *
from digidemo.forms import *
from digidemo.settings import DEBUG

handlers = {}

def handle_ajax(request, view='test', *args, **kwargs):
	try:
		data = handlers[view](request, *args, **kwargs)

	except Exception, e:

		if DEBUG:
			data = {'error': "%s: %s" %(type(e).__name__, e)}

		else:
			data = {'error': True}

	json_data = json.dumps(data);
	return render(request, 'digidemo/ajax.html', {'json_data':json_data})


def vote_proposal(request):
	vote_form = ProposalVoteForm(request.POST)

	if vote_form.is_valid(): 	# checks 1-vote-per-user constraint ?

		# record that the user has voted on this proposal
		vote_form.save()

		# increment or decrement the proposal score
		proposal = vote_form.cleaned_data['proposal']

		if vote_form.cleaned_data['valence']==1:
			proposal.score += 1
		elif vote_form.cleaned_data['valence']==-1:
			proposal.score -= 1

		proposal.save()
		
		return {'success':True}

	return {'success':False}

handlers['vote_proposal'] = vote_proposal


def vote_letter(request):
	vote_form = LetterVoteForm(request.POST)

	if vote_form.is_valid(): 	# checks 1-vote-per-user constraint ?

		# record that the user has voted on this proposal
		vote_form.save()

		# increment or decrement the proposal score
		letter = vote_form.cleaned_data['letter']

		if vote_form.cleaned_data['valence']==1:
			letter.score += 1
		elif vote_form.cleaned_data['valence']==-1:
			letter.score -= 1

		letter.save()
		
		return {'success':True}

	return {'success':False}

handlers['vote_letter'] = vote_letter


def test(request):
	return {'test':'success!'}

handlers['test'] = test


