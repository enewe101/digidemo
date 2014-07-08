import json
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.template.loader import get_template
from digidemo.models import *
from digidemo.forms import *
from digidemo.settings import DEBUG
from digidemo.utils import get_or_none

# json responders should return a python dict
_json_responders = {}


class AjaxError(Exception):
	pass


# decorator to register ajax responder endpoints
def ajax_endpoint(f):
	_json_responders[f.__name__] = f
	return f


# entry point handling all incomming ajax requests, 
# the request will be dispatched to the endpoint identified as `view` 
def handle_ajax_json(request, view='test', *args, **kwargs):

	# Get the handler, or return an error to the client
	try:
		handler = _json_responders[view]

	except KeyError, e:
		msg = screen_ajax_error(AjaxError('no endpoint named %s.'%view))
		return HttpResponse(content=msg, status=404, reason='Not Found')

	# process the request with the handler.	
	try:
		data = handler(request, *args, **kwargs)

	except Exception, e:
		return HttpResponse(content=screen_ajax_error(e), status=500, 
			reason='Internal Server Error')

	# render and return the HttpResponse
	data = json.dumps(data)
	return render(request, 'digidemo/ajax.html', {'json_data':data})



def screen_ajax_error(e):
	if DEBUG:
		err_msg = "%s: %s" %(type(e).__name__, e)

	else:
		err_msg = "error"

	return err_msg





def vote(vote_spec, request):

	existing_vote = get_or_none(vote_spec['model'],
		user=request.POST['user'], target=request.POST['target']) 

	if existing_vote is not None:
		existing_valence = existing_vote.valence
	else:
		existing_valence = 0

	vote_form = vote_spec['form'](request.POST, instance=existing_vote)

	if vote_form.is_valid():

		# record that the user has voted on this target
		vote_form.save()

		# increment or decrement the target score and author's rep
		target = vote_form.cleaned_data['target']
		author = target.user.profile.get()

		if existing_valence == 1:
			target.score -= 1
			author.undo_rep(vote_spec['up_event'])

		elif existing_valence == -1:
			target.score += 1
			author.undo_rep(vote_spec['dn_event'])

		if vote_form.cleaned_data['valence'] == 1:
			target.score += 1
			author.apply_rep(vote_spec['up_event'])

		elif vote_form.cleaned_data['valence'] == -1:
			target.score -= 1
			author.apply_rep(vote_spec['dn_event'])

		target.save()
		author.save()

		return {'success':True}

	return {
		'success': False,
		'msg': 'ajax.py: vote_discussion(): VoteForm was not valid'
	}



#####################
#					#
#  ajax endpoints	#
#					#
#####################

@ajax_endpoint
def vote_discussion(request):
	
	vote_spec = {
		'model' : DiscussionVote,
		'form': DiscussionVoteForm,
		'up_event': 'up_discussion',
		'dn_event': 'dn_discussion',
	}

	return vote(vote_spec, request)


#@ajax_endpoint
#def vote_proposal(request):
#
#	vote_spec = {
#		'model' : ProposalVote,
#		'form': ProposalVoteForm,
#		'up_event': 'up_proposal',
#		'dn_event': 'dn_proposal',
#	}
#
#	return vote(vote_spec, request)
#

	




@ajax_endpoint
def vote_proposal(request):

	existing_vote = get_or_none(ProposalVote,
		user=request.POST['user'], target=request.POST['target']) 

	if existing_vote is not None:
		existing_valence = existing_vote.valence
	else:
		existing_valence = 0


	vote_form = ProposalVoteForm(request.POST, instance=existing_vote)

	if vote_form.is_valid():

		# record that the user has voted on this proposal
		vote_form.save()

		# increment or decrement the proposal score
		proposal = vote_form.cleaned_data['target']

		proposal.score += vote_form.cleaned_data['valence'] - existing_valence

		proposal.save()
		
		return {'success':True}

	return {
		'success': False,
		'msg': 'ajax.py: vote_proposal(): VoteForm was not valid'
	}



@ajax_endpoint
def vote_letter(request):

	existing_vote = get_or_none(LetterVote,
		user=request.POST['user'], target=request.POST['target']) 

	if existing_vote is not None:
		existing_valence = existing_vote.valence
	else:
		existing_valence = 0

	vote_form = LetterVoteForm(request.POST, instance=existing_vote)

	if vote_form.is_valid():

		# record that the user has voted on this proposal
		vote_form.save()

		# increment or decrement the proposal score
		letter = vote_form.cleaned_data['target']

		letter.score += vote_form.cleaned_data['valence'] - existing_valence

		letter.save()
		
		return {'success':True}

	return {
		'success': False,
		'msg':'ajax.py: vote_letter(): VoteForm was not valid'  
	}



@ajax_endpoint
def send_letter(request):
	letter_form = LetterForm(request.POST)

	if letter_form.is_valid():

		# add the new (re)sent letter to the database
		letter_form.save()

		return {'success':True}

	return {
		'success':False,
		'msg':'ajax.py: send_letter(): LetterForm was not valid'
	}


@ajax_endpoint
def resend_letter(request):
	letter_form = ResendLetterForm(request.POST)

	if letter_form.is_valid():

		# add the new (re)sent letter to the database
		letter_form.save()
		return {'success':True}

	return {
		'success':False,
		'msg': 'ajax.py: send_letter(): LetterForm was not valid'
	}



@ajax_endpoint
def get_resender_avatar(request):

	# ** Hardcoded the logged in user to be enewe101 **
	logged_in_user = User.objects.get(pk=1)

	# render an html snippet, containing the avatar
	template = get_template('digidemo/_i_resender_avatar.html')
	context = Context({'resender': logged_in_user})
	reply_html = template.render(context)

	# package it up as for a JSON response and return
	return {'success': True, 'html': reply_html}



@ajax_endpoint
def reply(request):
	reply_form = ReplyForm(request.POST)
	
	if reply_form.is_valid():
		reply = reply_form.save()
		
		template = get_template('digidemo/_i_discussion_reply.html')
		context = Context({'reply': reply})
		reply_html = template.render(context)
		return {'success': True, 'html': reply_html}

	return {
		'success': False,
		'msg':'ajax.py: reply(): ReplyForm was not valid'
	}


@ajax_endpoint
def comment(request):
	comment_form = LetterCommentForm(request.POST)
	
	if comment_form.is_valid():
		comment = comment_form.save()
		
		template = get_template('digidemo/_i_letter_comment.html')
		context = Context({'comment': comment})
		reply_html = template.render(context)
		return {'success': True, 'html': reply_html}

	return {
		'success': False,
		'msg':'ajax.py: comment(): comment form was not valid'
	}


@ajax_endpoint
def test(request):
	return {'test':'success!'}



