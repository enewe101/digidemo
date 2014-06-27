import json
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from digidemo.models import *
from digidemo.forms import *
from digidemo.settings import DEBUG
from digidemo.utils import get_or_none

# json responders should return a python dict
json_responders = {}

# html responders should return an HttpResponse
html_responders = {}

class AjaxError(Exception):
	pass


def handle_ajax_json(request, view='test', *args, **kwargs):

	# Get the handler, or return an error to the client
	try:
		handler = json_responders[view]

	except KeyError, e:
		data = screen_ajax_error(AjaxError('no endpoint named %s.'%view))
		data = json.dumps(data)
		return render(request, 'digidemo/ajax.html', {'json_data':data})

	# process the request with the handler.	
	try:
		data = handler(request, *args, **kwargs)

	except Exception, e:
		data = {'error': screen_ajax_error(e)}

	# render and return the HttpResponse
	data = json.dumps(data)
	return render(request, 'digidemo/ajax.html', {'json_data':data})


def handle_ajax_html(request, view='test', *args, **kwargs):

	# Get the handler, or return an error to the client
	try:
		handler = html_responders[view]

	except KeyError, e:
		return HttpResponse('<p>' + screen_ajax_error(e) + '</p>')

	try:
		http_response = handler(request, *args, **kwargs)
		assert(isinstance(http_response, HttpResponse))

	except Exception, e:
		return HttpResponse('<p>' + screen_ajax_error(e) + '</p>')

	return http_response

	


def screen_ajax_error(e):
	if DEBUG:
		err_msg = "%s: %s" %(type(e).__name__, e)

	else:
		err_msg = "error"

	return err_msg

	

def vote_proposal(request):
	existing_vote = get_or_none(ProposalVote,
		user=request.POST['user'], proposal=request.POST['proposal']) 

	if existing_vote is not None:
		existing_valence = existing_vote.valence
	else:
		existing_valence = 0


	vote_form = ProposalVoteForm(request.POST, instance=existing_vote)

	if vote_form.is_valid():

		# record that the user has voted on this proposal
		vote_form.save()

		# increment or decrement the proposal score
		proposal = vote_form.cleaned_data['proposal']

		proposal.score += vote_form.cleaned_data['valence'] - existing_valence

		proposal.save()
		
		return {'success':True}

	return {'errors': vote_form.errors}

json_responders['vote_proposal'] = vote_proposal


def vote_letter(request):

	existing_vote = get_or_none(LetterVote,
		user=request.POST['user'], letter=request.POST['letter']) 

	if existing_vote is not None:
		existing_valence = existing_vote.valence
	else:
		existing_valence = 0

	vote_form = LetterVoteForm(request.POST, instance=existing_vote)

	if vote_form.is_valid():

		# record that the user has voted on this proposal
		vote_form.save()

		# increment or decrement the proposal score
		letter = vote_form.cleaned_data['letter']

		letter.score += vote_form.cleaned_data['valence'] - existing_valence

		letter.save()
		
		return {'success':True}

	return {'errors': vote_form.errors}


json_responders['vote_letter'] = vote_letter


def resend_letter(request):
	letter_form = ResendLetterForm(request.POST)

	if letter_form.is_valid():

		# add the new (re)sent letter to the database
		letter_form.save()

		# add the resender to the list of resenders of the original letter
		parent_letter = letter_form.cleaned_data['parent_letter']
		parent_letter.resenders.add(letter_form.cleaned_data['sender'])
		parent_letter.save()

		return {'success':True}

	return {'success':False}

json_responders['resend_letter'] = resend_letter


def get_resender_avatar(request):

	# ** Hardcoded the logged in user to be enewe101 **
	logged_in_user = User.objects.get(pk=1)

	return render(
		request, 'digidemo/resender_avatar.html', {'resender': logged_in_user})


html_responders['get_resender_avatar'] = get_resender_avatar
	

def test(request):
	return {'test':'success!'}

json_responders['test'] = test


