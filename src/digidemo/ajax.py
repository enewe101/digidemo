import json
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as __
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from digidemo.models import *
from digidemo.abstract_models import *
from digidemo.forms import *
from digidemo.settings import DEBUG
from digidemo.utils import get_or_none, force_logout
from digidemo.views import get_vote_form, AnswerSection, ReplySection
from digidemo.shortcuts import get_profile, login_user

# json responders should return a python dict
_json_responders = {}


class AjaxError(Exception):
	pass


# decorator to register ajax responder endpoints
def ajax_endpoint(f):
	_json_responders[f.__name__] = f
	return f


def ajax_endpoint_login_required(error_msg=None, form_class=None):
	'''
	Use this decorator for ajax functions that should only honour requests
	from a logged in user.  When a request is made without an authenticated
	user, a sytem-level error message as well as a user-facing error message
	are returned to the client.

	If the ajax request came from a widget based on `_w_ajax_form.html`,
	then the system error message will appear in an alert box (if the 
	site is in DEBUG mode), and the user-facing message will get inserted
	into the widget's form_errors div.

	You can change the default user-facing error message by passing a string
	to the decorator as the `error_msg` argument.

	Any form that has a user field in it needs an extra step of validation.
	Although the user has been authenticated, we need to make sure that the
	user in the form is the same as the authenticated user.  Otherwise a 
	user could impersonate another by altering the user field.  we cannot 
	rely on the field (alone) therefore, but it is implicitly used when 
	form.save() is called.

	To validate that the user in the user field is the same as the logged in
	user, simply pass the class of the form to the decorator, as the second
	argument.  E.g. if you are processing a QuestionCommentForm, then pass
	`QuestionCommentForm` to the decorator, and it will perform this extra 
	check.  

	You *MUST* do this if the form has a user field!

	Note: This decorator must be called with parens following its name:
		like this --> @ajax_endpoint_login_required()
	'''

	# if no error_msg was given, use this default
	if error_msg is None:
		error_msg = 'You must login first!'

	# This function performs the act of decorating
	def decorate(original_func):

		# this function wraps the original endpoint function.  
		# It fires instead when the original function is called
		def wrapped(request):

			# check that the user is logged in
			if not request.user.is_authenticated():
				return {
					'success':False,
					'msg': 'user did not authenticate',
					'errors': {'__all__': 
						[error_msg]}
				}

			elif not get_profile(request.user).email_validated:
				return {
					'success':False,
					'msg': 'user email not validated',
					'errors': {'__all__': 
						['You must validate your email first!']}
				}

			# if the decoration was passed a form, then verify that the 
			# logged in user, and the user who requested the form are the same
			if form_class is not None:
				form = form_class(request.POST)
				form.is_valid()
				form_user = form.cleaned_data['user']
				if form_user != request.user:
					force_logout(request) # this is not implemented yet!
					return {
						'success':False,
						'msg': 'authenticated user did not match the '
							'user that requested the form',
						'errors':{'__all__':
							['Sorry, your session has expired...']}
					}

			# Finally, do whatever the original function does
			return original_func(request)

		# register the wrapped version as an ajax endpoint
		_json_responders[original_func.__name__] = wrapped

		# return the wrapped version to this module's namepsace
		return wrapped

	# The error message and form class (if any) were bound the custom decorator
	return decorate


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
			reason= 'Internal Server Error')

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

		# make sure that the vote is not being cast by a user on her own
		# content!
		content_author = vote_form.cleaned_data['target'].user
		if(request.user == content_author):
			return {
				'success':False, 
				'msg': 'user cannot vote on own content',
				'errors': ["You can't vote on your own post!"]
			}

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

UNAUTHORIZED_VOTE_MESSAGE = 'You must login to vote!'

@ajax_endpoint_login_required(UNAUTHORIZED_VOTE_MESSAGE, AnswerVoteForm)
def vote_answer(request):
	
	vote_spec = {
		'model' : AnswerVote,
		'form': AnswerVoteForm,
		'up_event': 'up_answer',
		'dn_event': 'dn_answer',
	}

	return vote(vote_spec, request)

@ajax_endpoint_login_required(UNAUTHORIZED_VOTE_MESSAGE, QuestionVoteForm)
def vote_question(request):
	
	vote_spec = {
		'model' : QuestionVote,
		'form': QuestionVoteForm,
		'up_event': 'up_question',
		'dn_event': 'dn_question',
	}

	return vote(vote_spec, request)

@ajax_endpoint_login_required(UNAUTHORIZED_VOTE_MESSAGE, DiscussionVoteForm)
def vote_discussion(request):
	
	vote_spec = {
		'model' : DiscussionVote,
		'form': DiscussionVoteForm,
		'up_event': 'up_discussion',
		'dn_event': 'dn_discussion',
	}

	return vote(vote_spec, request)


@ajax_endpoint_login_required(UNAUTHORIZED_VOTE_MESSAGE, ProposalVoteForm)
def vote_proposal(request):

	vote_spec = {
		'model' : ProposalVote,
		'form': ProposalVoteForm,
		'up_event': 'up_proposal',
		'dn_event': 'dn_proposal',
	}

	return vote(vote_spec, request)


@ajax_endpoint_login_required(UNAUTHORIZED_VOTE_MESSAGE, LetterVoteForm)
def vote_letter(request):

	vote_spec = {
		'model' : LetterVote,
		'form': LetterVoteForm,
		'up_event': 'up_letter',
		'dn_event': 'dn_letter',
	}

	return vote(vote_spec, request)


@ajax_endpoint_login_required(UNAUTHORIZED_VOTE_MESSAGE, ReplyVoteForm)
def vote_reply(request):

	vote_spec = {
		'model' : ReplyVote,
		'form': ReplyVoteForm,
		'up_event': 'up_reply',
		'dn_event': 'dn_reply',
	}

	return vote(vote_spec, request)



@ajax_endpoint_login_required()
def register_notifications_seen(request):

	notifications_seen = request.POST['notification_pks'].strip()
	if notifications_seen == '':
		return {
			'success':True,
			'num_marked':0,
			'errors': []
		}

	notifications_seen = [int(i) for i in notifications_seen.split(',')]
	num_marked = len(notifications_seen)
	notifications_seen = Notification.objects.filter(pk__in=notifications_seen)
	notifications_seen.update(was_seen=True)
	
	return {
		'success':True,
		'num_marked': num_marked,
		'errors': []
	}

@ajax_endpoint_login_required()
def register_notification_checked(request):

	notification_checked = int(request.POST['notification_pk'])
	notification_checked = Notification.objects.filter(pk=notification_checked)
	notification_checked.update(was_checked=True)
	
	return {
		'success':True,
		'errors': []
	}


@ajax_endpoint_login_required('You must login to comment!')
def add_inline_discussion(request):

	discussion_form = InlineDiscussionForm(request.POST)
	if discussion_form.is_valid():

		# if the comment id is not empty, this is an edit request
		if(request.POST['comment_id'] != ''):
			comment_id = int(request.POST['comment_id'])
			discussion = Discussion.objects.get(pk=comment_id)

			# the user can only edit her own comments
			if discussion.user != request.user:
				raise PermissionDenied

			discussion.text = request.POST['text']
			discussion.save()

		# otherwise, this is a create request
		else:
			discussion = discussion_form.save(commit=False)
			discussion.user = request.user
			discussion.save()

		print 'comment id:', discussion.pk

		return {
			'success':True,
			'comment_id': discussion.pk,
			'errors': discussion_form.json_errors()
		}

	print 'form not valid'
	print discussion_form._errors

	return {
		'success':False,
		'msg':'ajax.py: InlineDiscussionForm was not valid', 
		'errors': discussion_form.json_errors()
	}

@ajax_endpoint_login_required('You must login to delete a comment!')
def delete_inline_comment(request):

	# get the comment identified in the request
	comment_id = request.POST['comment_id']
	inline_comment = get_object_or_404(Discussion, pk=comment_id)

	# ensure that the requesting user is trying to delete a comment that
	# belongs to her
	if inline_comment.user != request.user:
		raise PermissionDenied

	inline_comment.delete()
	print 'Deleted'
	return {'success':True}



@ajax_endpoint_login_required('You must login to post a reply!', ReplyForm)
def reply(request):

	reply_form = ReplyForm(request.POST)

	if reply_form.is_valid():

		# add the new (re)sent letter to the database
		reply = reply_form.save()

		# make a reply section
		reply_section = ReplySection(reply, request.user)

		# render the reply section, send it back to be put on the page
		template = get_template('digidemo/_i_post_with_comments.html')
		context = RequestContext(request, {
			'post_section': reply_section,
			'user': request.user})
		reply_html = template.render(context)

		return {
			'success':True,
			'html':reply_html, 
			'errors': reply_form.json_errors()	# this should be empty
		}

	return {
		'success':False,
		'msg': 'ajax.py: answer(): ReplyForm was not valid',
		'errors': reply_form.json_errors()
	}





@ajax_endpoint_login_required('Please login to post your answer!', AnswerForm)
def answer(request):

	answer_form = AnswerForm(request.POST)

	if answer_form.is_valid():

		# add the new (re)sent letter to the database
		answer = answer_form.save()

		# make an answer section
		answer_section = AnswerSection(answer, answer_form.cleaned_data['user'])

		# render the answer section, and send it back for inclusion on page
		template = get_template('digidemo/_i_post_with_comments.html')
		context = RequestContext(request, {
			'post_section': answer_section,
		})
		reply_html = template.render(context)


		return {
			'success':True,
			'html':reply_html, 
			'errors': answer_form.json_errors()	# this will be empty
		}

	return {
		'success':False,
		'msg': 'ajax.py: answer(): AnswerForm was not valid',
		'errors': answer_form.json_errors()
	}



@ajax_endpoint_login_required(
'You must log in to create a petition!', LetterForm)
def send_letter(request):
	letter_form = LetterForm(request.POST)

	if letter_form.is_valid():

		# add the new (re)sent letter to the database
		letter_form.save()

		return {'success':True}

	return {
		'success':False,
		'msg': 'ajax.py: send_letter(): LetterForm was not valid'
	}


@ajax_endpoint_login_required(
'You must log in to sign a petition!', ResendLetterForm)
def resend_letter(request):
	letter_form = ResendLetterForm(request.POST)

	if letter_form.is_valid():

		# add the new (re)sent letter to the database
		letter = letter_form.save()

		# increment the score of the parent letter
		letter.parent_letter.increment_score()
		return {'success':True}

	return {
		'success':False,
		'msg': 'ajax.py: send_letter(): ResendLetterForm was not valid'
	}



# TODO: is this still being used?  User is hardcoded...
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
def ajax_login(request):

	# attempt to authenticate the user
	username = request.POST['username']
	password = request.POST['password']
	login_success = login_user(username, password, request)


	# successful login
	if login_success == 'LOGIN_VALID_EMAIL':
		return {'success':True, 'email_valid': True, 'username':username}

	# successful login but invalid email
	elif login_success == 'LOGIN_INVALID_EMAIL':
		return {'success':True, 'email_valid': False}

	# failed login
	else: # login_success == 'LOGIN_FAILED':
		return {'success':False, 'email_valid': False}



# TODO: replace this with a post login
@ajax_endpoint
def ajax_logout(request):
	logout(request)
	return {'success':True}


#
# all of the comment forms are processed very similarly, but we actually
# use different models for different comments, because they are tied to 
# different targets (e.g. comment on an Answer vs comment on a Letter).
# all comments are ultimately processed by `process_comment`, which abstracts
# the differences.  Here we bind separate endpoints for each kind of comment
#
@ajax_endpoint_login_required(form_class=AnswerCommentForm)
def answer_comment(request):
	return process_comment(request, AnswerCommentForm)

@ajax_endpoint_login_required(form_class=QuestionCommentForm)
def question_comment(request):
	return process_comment(request, QuestionCommentForm)

@ajax_endpoint_login_required(form_class=LetterCommentForm)
def comment(request):
	return process_comment(request, LetterCommentForm)

@ajax_endpoint_login_required(form_class=ReplyCommentForm)
def reply_comment(request):
	return process_comment(request, ReplyCommentForm)

@ajax_endpoint_login_required(form_class=DiscussionCommentForm)
def discussion_comment(request):
	return process_comment(request, DiscussionCommentForm)


#
# All comments end up getting processed here.  
# At this point user has been authenticated.
#
def process_comment(request, comment_form_class):
	comment_form = comment_form_class(request.POST)
	
	if comment_form.is_valid():
		comment = comment_form.save()
		
		template = get_template('digidemo/_i_comment.html')
		context = Context({'comment': comment})
		reply_html = template.render(context)
		return {
			'success': True,
			'html': reply_html,
			'errors': comment_form.json_errors()	# this will be empty
		}

	return {
		'success': False,
		'msg': 'ajax.py: comment(): comment form was not valid',
		'errors': comment_form.json_errors()
	}




@ajax_endpoint
def follow_post(request):
        print "yes"
        if(request.session.has_key('user')):
                proposalID = request.POST['id'];
                proposal = Proposal.objects.get(pk=proposalID);
                userName = request.session['user'];
                userLoggedIn = User.objects.get(username = userName);
                userProfile = UserProfile.objects.get(user = userLoggedIn);
                if proposal in userProfile.followedProposals.all() :
                        userProfile.followedProposals.remove(proposal);
                        print "exits already";   
                else:
                        print "Doesnt exists"
                        userProfile.followedProposals.add(proposal);
                        userProfile.save();
                print "returning"
                return "logged"
        else :
                return "unlogged"

        

@ajax_endpoint
def checkValidUserName(request):
		username_pass = request.POST['username'];
		try :
			available = User.objects.get(username=username_pass);
			available = False;

		except:
			available = True;

		return {'success':True, 'available': available}




def handle_ajax_login(request):
	username_pass = request.GET['username']
	password_pass = request.GET['password']
	user = authenticate(username=username_pass, password=password_pass)
	data = 0;
	if user is not None:
		login(request, user)
		data = "accepted";
		request.session['user']=username_pass;
	else:
		data = "denied";

	return render(request, 'digidemo/ajax.html', {'json_data':data})


def handle_ajax_logout(request):
	request.session.pop("user",None)
	data = test(request)
	logout(request)
	return render(request, 'digidemo/ajax.html', {'json_data':data})


@ajax_endpoint
def test(request):
	return {'test':'success!'}



