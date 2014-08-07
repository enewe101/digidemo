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
from digidemo.views import get_vote_form
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

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
		author = target.user.profile

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
		'msg': 'ajax.py: vote(): VoteForm was not valid'
	}



#####################
#					#
#  ajax endpoints	#
#					#
#####################

@ajax_endpoint
def vote_answer(request):
	
	vote_spec = {
		'model' : AnswerVote,
		'form': AnswerVoteForm,
		'up_event': 'up_answer',
		'dn_event': 'dn_answer',
	}

	return vote(vote_spec, request)

@ajax_endpoint
def vote_question(request):
	
	vote_spec = {
		'model' : QuestionVote,
		'form': QuestionVoteForm,
		'up_event': 'up_question',
		'dn_event': 'dn_question',
	}

	return vote(vote_spec, request)

@ajax_endpoint
def vote_discussion(request):
	
	vote_spec = {
		'model' : DiscussionVote,
		'form': DiscussionVoteForm,
		'up_event': 'up_discussion',
		'dn_event': 'dn_discussion',
	}

	return vote(vote_spec, request)


@ajax_endpoint
def vote_proposal(request):

	vote_spec = {
		'model' : ProposalVote,
		'form': ProposalVoteForm,
		'up_event': 'up_proposal',
		'dn_event': 'dn_proposal',
	}

	return vote(vote_spec, request)


@ajax_endpoint
def vote_letter(request):

	vote_spec = {
		'model' : LetterVote,
		'form': LetterVoteForm,
		'up_event': 'up_letter',
		'dn_event': 'dn_letter',
	}

	return vote(vote_spec, request)



@ajax_endpoint
def answer(request):

	# ** Hardcoded the logged in user to be enewe101 **
	logged_in_user = User.objects.get(pk=1)
	 
	answer_form = AnswerForm(request.POST)

	if answer_form.is_valid():

		# add the new (re)sent letter to the database
		answer = answer_form.save()

		vote_form = get_vote_form(
			AnswerVote, AnswerVoteForm, logged_in_user, answer)

		# make a unique id for the vote form based on the userstats
		num_prior_answers = Answer.objects.filter(
			user=logged_in_user, target=answer.target).count()


		# render an html snippet, containing the avatar
		template = get_template('digidemo/_i_reply.html')
		context = Context({
			'include_id': logged_in_user.username + str(num_prior_answers),
			'reply': {
				'content': answer,
				'vote_form': vote_form,
			},
		})
		reply_html = template.render(context)


		return {
			'success':True,
			'html':reply_html, 
			'errors': answer_form.json_errors()	# these will be empty
		}

	return {
		'success':False,
		'msg':'ajax.py: answer(): AnswerForm was not valid',
		'errors': answer_form.json_errors()
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
def get_factor_form(request):

	# unpack expected data
	valence = request.POST['valence']
	include_id = request.POST['include_id']

	# make the factor form
	prefix = valence + '-' + include_id 
	valence_val = 1 if valence=='pos' else -1
	factor_form = FactorVersionForm(
		initial={'valence':valence_val},
		prefix=prefix
	)

	# get the template and assemble the context, and render the html
	template = get_template('digidemo/_w_factor_form.html')
	context = Context({
		'valence':valence,
		'include_id':include_id,
		'form':factor_form
	})
	reply_html = template.render(context)

	# send back a json reply
	return {'success':True, 'html': reply_html}



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
def answer_comment(request):
	return process_comment(request, AnswerCommentForm)

@ajax_endpoint
def question_comment(request):
	return process_comment(request, QuestionCommentForm)

@ajax_endpoint
def comment(request):
	return process_comment(request, LetterCommentForm)



def process_comment(request, comment_form_class):
	comment_form = comment_form_class(request.POST)
	
	if comment_form.is_valid():
		comment = comment_form.save()
		
		template = get_template('digidemo/_i_comment.html')
		context = Context({'comment': comment})
		reply_html = template.render(context)
		return {'success': True, 'html': reply_html}

	return {
		'success': False,
		'msg':'ajax.py: comment(): comment form was not valid'
	}


@ajax_endpoint
def editProposal(request):
        pName = request.GET['name']
        title = request.GET['title']
        text = request.GET['text']
        goodFactors = request.GET['goodFactors']
        badFactors = request.GET['badFactors']
        proposal = Proposal.objects.get(name=pName)
        proposal.title = title
        proposal.text= text
        proposal.last_modified = timezone.now()
        
        proposal.save()
        print "Here222"
	return {'test':'success!'}


@ajax_endpoint
def follow_post(request):
        print "yes"
        if(request.session.has_key('user')):
                proposalID = request.POST['id'];
                proposal = Proposal.objects.get(pk=proposalID);
                print proposal;
                userName = request.session['user'];
                print "yes yes"
                userLoggedIn = User.objects.get(username = userName);
                userProfile = UserProfile.objects.get(user = userLoggedIn);
                userProfile.followedProposals.add(proposal);
                print "yo"
                userProfile.save();
                print "yo"
                return "logged"
        else :
                return "unlogged"

        
@ajax_endpoint
def checkValidUserName(request):
        username_pass = request.GET['username'];
        print username_pass;
        try :
               name =  User.objects.get(username=username_pass);
        except:
                name = None
        print name
        if name:
                return 'unavailable';
        else:
                return 'available';

def handle_ajax_login(request):
        username_pass = request.GET['username']
        password_pass = request.GET['password']
        user = authenticate(username=username_pass, password=password_pass)
        data = 0;
        if user is not None:
                data = "accepted";
                request.session['user']=username_pass;
        else :
                data = "denied";
        #data = test(request)
        return render(request, 'digidemo/ajax.html', {'json_data':data})


def handle_ajax_logout(request):
        request.session.pop("user",None)
        data = test(request)
        return render(request, 'digidemo/ajax.html', {'json_data':data})



@ajax_endpoint
def test(request):
	return {'test':'success!'}



