# -*- coding: utf-8 -*-
import difflib
import collections as c

from uuid import uuid4
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as __
from django.core import serializers
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files import File
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.forms.formsets import formset_factory
from django import http
from django.views.debug import ExceptionReporter
from django.conf import settings

from digidemo.models import *
from digidemo.abstract_models import *
from digidemo.forms import *
from digidemo import utils
from digidemo.utils import force_logout
from digidemo.shortcuts import get_profile, login_user, send_email_confirmation


from forms import ProposalSearchForm
from settings import DEBUG, IN_PRODUCTION
from settings import TEMP_DIR
import pydenticon

import json
import sys
from choices import *;


# Names we use for the tabs in proposal sections
OVERVIEW_TAB_NAME = _('issue')
QUESTIONS_TAB_NAME = _('questions')
OPINION_TAB_NAME = _('letters')
EDIT_TAB_NAME = _('edit / discuss')

# Names we use for the top level "button" navigation
ISSUE_NAV_NAME = 'issues'
TOPICS_NAV_NAME = 'topics'
CREATE_NAV_VAME = 'create'
QUESTIONS_NAV_NAME = 'questions'
OPINION_NAV_NAME = 'letters'
USERS_NAV_NAME = 'users'


def get_user_notifications(user):
	SHOW_AT_LEAST = 8

	# get unchecked notifications
	unchecked_notifications = Notification.objects\
		.filter(target_user=user, was_checked=False)\
		.exclude(source_user=user)\
		.order_by('-creation_date')\

	# Force queryset evaluation
	unchecked_notifications = list(unchecked_notifications)
	num_left_to_show = SHOW_AT_LEAST - len(unchecked_notifications)

	# get seen notifications in order to show at least SHOW_AT_LEAST
	checked_notifications = []
	if num_left_to_show > 0:
		checked_notifications = Notification.objects\
			.filter(target_user=user, was_checked=True)\
			.exclude(source_user=user).order_by('-creation_date')[:num_left_to_show]

	# Force queryset evaluation
	checked_notifications = list(checked_notifications)
	notifications = unchecked_notifications + checked_notifications

	return notifications


def get_pretty_user_notifications(user):
	notifications = get_user_notifications(user)
	pretty_notifications = []
	for n in notifications:
		message = get_notification_message(n)
		n.message = message
		pretty_notifications.append(n)

	return pretty_notifications


def get_proposal_tabs(proposal, active_tab):

	# This is the basic tabs definition for the proposal views
	proposal_tabs = [
		{'name': OVERVIEW_TAB_NAME,'url': proposal.get_proposal_url()},
		{'name': EDIT_TAB_NAME,'url': proposal.get_open_discussions_url()},
		{'name': QUESTIONS_TAB_NAME,'url': proposal.get_question_list_url()},
		{'name': OPINION_TAB_NAME,'url': proposal.get_petitions_url()},
	]

	# mark the active tab as active
	active_index = [t['name'] for t in proposal_tabs].index(active_tab)
	proposal_tabs[active_index]['active'] = True

	return proposal_tabs


def get_edit_tabs(active_tab, issue):

	# This is the basic tabs definition for the proposal views
	tabs = [
		{
			'name': 'discuss',
			'url': issue.get_open_discussions_url()
		},
		{
			'name': 'edit',
			'url': reverse('edit', kwargs={'issue_id':issue.pk})
		},
		{
			'name': 'preview',
			'url': reverse('edit', kwargs={'issue_id':issue.pk})
		},
	]

	# mark the active tab as active
	active_index = [t['name'] for t in tabs].index(active_tab)
	tabs[active_index]['active'] = True

	return tabs

def get_issue_list_tabs(active_tab):

	# This is the basic tabs definition for the proposal views
	tabs = [
		{
			'name': 'interesting',
			'url': reverse('issue_list', kwargs={'order_by':'interesting'})
		},
		{
			'name': 'activity',
			'url': reverse('issue_list', kwargs={'order_by':'activity'})
		},
		{
			'name': 'newest',
			'url': reverse('issue_list', kwargs={'order_by':'newest'})
		},
		#{
		#	'name': 'location',
		#	'url': reverse('issue_list', kwargs={'order_by':'location'})
		#},
	]

	# mark the active tab as active
	active_index = [t['name'] for t in tabs].index(active_tab)
	tabs[active_index]['active'] = True

	return tabs


def get_petition_list_tabs(active_tab):

	# This is the basic tabs definition for the proposal views
	tabs = [
		{
			'name': 'interesting',
			'url': reverse('all_petitions_list',
				kwargs={'order_by':'interesting'})
		},
		{
			'name': 'activity',
			'url': reverse('all_petitions_list',
				kwargs={'order_by':'activity'})
		},
		{
			'name': 'newest',
			'url': reverse('all_petitions_list', kwargs={'order_by':'newest'})
		},
		#{
		#	'name': 'location',
		#	'url': reverse('all_petitions_list',
		#		kwargs={'order_by':'location'})
		#},
	]

	# mark the active tab as active
	active_index = [t['name'] for t in tabs].index(active_tab)
	tabs[active_index]['active'] = True

	return tabs


def get_question_list_tabs(active_tab):

	# This is the basic tabs definition for the proposal views
	question_list_tabs = [
		{
			'name': 'interesting',
			'url': reverse('all_questions_list',
				kwargs={'order_by':'interesting'})
		},
		{
			'name': 'activity',
			'url': reverse('all_questions_list',
				kwargs={'order_by':'activity'})
		},
		{
			'name': 'newest',
			'url': reverse('all_questions_list', kwargs={'order_by':'newest'})
		},
		#{
		#	'name': 'location',
		#	'url': reverse('all_questions_list',
		#		kwargs={'order_by':'location'})
		#},
	]

	# mark the active tab as active
	active_index = [t['name'] for t in question_list_tabs].index(active_tab)
	question_list_tabs[active_index]['active'] = True

	return question_list_tabs

def feedback(request):
	thank_you = False
	if request.POST:

		form = FeedbackForm(request.POST)

		if form.is_valid():
			form.save()
			thank_you = True

	else:
		form = FeedbackForm()

	return render(request, 'digidemo/feedback.html', {
		'GLOBALS': get_globals(request),
		'django_vars_js': get_django_vars_JSON(request=request),
		'thank_you': thank_you,
		'form': form
	})



	
def get_globals(request):

	email_validated = True if (
			request.user.is_authenticated() 
			and get_profile(request.user).email_validated
		) else False

	language_is_english = request.LANGUAGE_CODE.startswith('en')
	GLOBALS = {
		'IS_ENGLISH': language_is_english,
		'OTHER_LANG': 'fr' if language_is_english else 'en',
		'DEBUG': DEBUG,
		'IN_PRODUCTION': IN_PRODUCTION,
		'SECTORS': Sector.objects.all(),
		'IS_USER_AUTHENTICATED': request.user.is_authenticated(),
		'IS_EMAIL_VALIDATED': email_validated,
		'USER': request.user,
		'FEEDBACK_FORM': FeedbackForm()
	}

	if request.user.is_authenticated():
		# count how many were never seen before
		notifications = get_pretty_user_notifications(request.user) 
		unseen_notification_pks = [
			str(n.pk) for n in notifications if not n.was_seen]
		num_unseen = len(unseen_notification_pks)
		GLOBALS['NOTIFICATIONS'] = notifications
		GLOBALS['NUM_UNSEEN_NOTIFICATIONS'] = num_unseen
		GLOBALS['UNSEEN_NOTIFICATION_PKS'] = ','.join(
			unseen_notification_pks)

	else:
		GLOBALS['NOTIFICATIONS'] = []
		GLOBALS['NUM_UNSEEN_NOTIFICATIONS'] = 0
		GLOBALS['UNSEEN_NOTIFICATION_PKS'] = ''

	return GLOBALS


def show_server_error(request):
    """
    500 error handler to show Django default 500 template
    with nice error information and traceback.
    Useful in testing, if you can't set DEBUG=True.

    Templates: `500.html`
    Context: sys.exc_info() results
     """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    error = ExceptionReporter(request, exc_type, exc_value, exc_traceback)
    return http.HttpResponseServerError(error.get_traceback_html())


def get_django_vars_JSON(additional_vars={}, request=None):
	return json.dumps(get_django_vars(
		request, additional_vars=additional_vars))


def get_django_vars(request, additional_vars={}):

	email_validated = True if (
			request.user.is_authenticated() 
			and get_profile(request.user).email_validated
		) else False

	django_vars = {
		'DEBUG': DEBUG,
		'IS_USER_AUTHENTICATED': request.user.is_authenticated(),
		'IS_EMAIL_VALIDATED': email_validated
	}

	django_vars.update(additional_vars)

	return django_vars



def flatten(list_2d):
	return [item for sublist in list_2d for item in sublist]


def split_keep(s, r):

	'''
	split the s (a string) wherever *after* matches to r (a regular
	expression representing a delimiter) keeping the delimiter attached to the
	substring to the "left" of the split.
	'''

	substrings = []
	last_end = 0
	for match in r.finditer(s):
		substrings.append(s[last_end:match.end()])
		last_end = match.end()

	if s[last_end:] != '':
		substrings.append(s[last_end:])

	return substrings


def split_at(s, r, max_len):
	substrings = []
	last_end = 0
	prev_match = None
	for match in r.finditer(s):

		# If the current match is beyond max_len, split at the previous match
		if match.end() - last_end > max_len:

			if prev_match is not None:
				substrings.append(s[last_end:prev_match.end()])
				last_end = prev_match.end()
				prev_match = match

			# But if there is no previous match, forcefully split at max_len
			else:
				substrings.append(s[last_end:last_end+max_len])
				last_end += max_len

		else:
			prev_match = match
	
	# If there is left-over stringage after the last cut, keep it
	if s[last_end:] != 0:
		substrings.append(s[last_end:])

	return substrings


def chop_string(s, max_len=40):

	# split on new sentences and new lines
	d = re.compile(r'\.+\s+(\s*\n)*|\n(\s*\n)*')
	lines = split_keep(s, d)

	# keep lines shorter than max_len.  Prefer to split on word-boundaries.
	d = re.compile('\W')
	lines = flatten([split_at(line, d, max_len) for line in lines])

	return lines


def land(request):

	thank_you = False
	email_form = EmailSignupForm()
	email_form.id_prefix=0
	email_form.endpoint='/'

	if request.POST:
		sent_email_form = EmailSignupForm(request.POST)

		if sent_email_form.is_valid():
			sent_email_form.save()
			thank_you = True

		else:
			email_form = sent_email_form
			email_form.id_prefix = 0
			email_form.endpoint = '/'

	return render(request, 'digidemo/land.html', {
		'GLOBALS': get_globals(request),
		'thank_you': thank_you,
		'email_form': email_form
	})


def history(request, proposal_id):

	proposal = Proposal.objects.get(pk=proposal_id)

	# make diff between the latest version of the proposal and the one
	# before it
	proposal_versions = ProposalVersion.objects\
		.filter(proposal=proposal)\
		.order_by('-creation_date')\
		[:2]

	# TODO: handle this case
	if proposal_versions.count() == 0:
		pass

	elif proposal_versions.count() < 2:
		to_text, from_text = proposal_versions[0].text, ''
	
	else:
		to_text, from_text = [pv.text for pv in proposal_versions]

	# chop the text into 80-character lines
	to_text, from_text = [chop_string(t, 60) for t in [to_text, from_text]]

	differ = difflib.HtmlDiff(tabsize=4)

	diff_table = differ.make_table(from_text, to_text)


	return render(
		request,
		'digidemo/history.html',
		{
			'GLOBALS': get_globals(self.request),
			'django_vars_js': get_django_vars_JSON(request=request),
			'proposal': proposal,
			'diff_table': diff_table,
			'active_navitem': 'issues',
			'tabs': get_proposal_tabs(proposal, 'edit')
		}
	)




def get_vote_form(VoteModel, VoteForm, user, target, id_prefix=''):

	existing_vote = utils.get_or_none(VoteModel, user=user.pk, target=target)
	
	# Only enable the form if the user is authenticated
	is_enabled = False
	tooltip = _("You must login to vote!")
	if user.is_authenticated():
		is_enabled = True

		# Also, don't enable the form if the user is the author of the post!
		if (target.user == user):
			is_enabled = False
			tooltip = _(r"You can\'t vote on your own post!")

		if not get_profile(user).email_validated:
			is_enabled = False
			tooltip = _(r"You need to validate your email!")


	if existing_vote:
		vote_form = VoteForm(
			instance=existing_vote,
			cur_score=target.score,
			is_enabled=is_enabled,
			tooltip=tooltip,
			id_prefix=id_prefix
		)

	else:
		vote_form = VoteForm(
			initial={'user':user.pk, 'target':target.pk},
			cur_score=target.score,
			is_enabled=is_enabled,
			tooltip=tooltip,
			id_prefix=id_prefix
		)

	return vote_form


class CommentSection(object):
	'''
	this encapsulates a series of comments as well as an add comment
	form. It removes the burden of creating links between these aspects
	from the view
	'''
	def __init__(self, comment_set, comment_form):
		self.comments = comment_set
		self.comment_form = comment_form

		# Below is the important line, which ensures that the
		# include id used to set the html id's in the comments area
		# matches the comment_form's prefix id.  This is necessary for
		# allowing new comments submitted by the comment form to get displayed
		# dynamically in the comments area by javascript
		self.id_prefix = comment_form.id_prefix


class PostSection(object):
	'''
	This encapsulates a "post" along with its comments, comment_form,
	and voting widget.  A "post" is an abstract object, and Question, Answer,
	Discussion, Reply, and Letter, are, conceptually, non-abstract
	implementations of it.
	
	This class let's one build all of the widgetery that goes along with
	a post, which is fairly repetitive buisiness.  In doing so, it makes
	sure that all of the id's, which ultimately become html ids, are
	syncronized so that assumptions that exist in the templates, which
	bind behaviors between elements in the post based on getting these elements
	by id, are satisfied, and everything works nicely, and DRYly.
	'''

	# These are not implemented in this class, because it is abstract
	CommentForm = None
	Vote = None
	VoteForm = None

	def __init__(
			self,
			post,
			user,
			id_prefix=None
		):

		# ascertain the kind of post we're dealing with
		self.post = post

		# derive the include id from the post's pk, guaranteed to be unique
		# on the page unless for some reason the post is included multiple
		# times
		if id_prefix is None:
			self.id_prefix = self.post.pk
		else:
			self.id_prefix = id_prefix

		# get the associated object models for the post's widgetery
		self.comments = self.post.comment_set.all()
		self.comment_form = self.CommentForm(
			initial={'user':user, 'target': self.post},
			id_prefix=self.id_prefix
		)

		# make a vote form
		self.vote_form = get_vote_form(
			self.Vote,
			self.VoteForm,
			user,
			post,
			id_prefix=self.id_prefix
		)

		# make a comments section
		self.comments_section = CommentSection(
			self.comments,
			self.comment_form
		)


class QuestionSection(PostSection):
	CommentForm = QuestionCommentForm
	Vote = QuestionVote
	VoteForm = QuestionVoteForm

class DiscussionSection(PostSection):
	CommentForm = DiscussionCommentForm
	Vote = DiscussionVote
	VoteForm = DiscussionVoteForm

class ReplySection(PostSection):
	CommentForm = ReplyCommentForm
	Vote = ReplyVote
	VoteForm = ReplyVoteForm

class AnswerSection(PostSection):
	CommentForm = AnswerCommentForm
	Vote = AnswerVote
	VoteForm = AnswerVoteForm

class LetterSection(PostSection):
	CommentForm = LetterCommentForm
	Vote = LetterVote
	VoteForm = LetterVoteForm
	ResendForm = ResendLetterForm

	def __init__(self,
			post,
			user,
			id_prefix=None,
			*args,
			**kwargs
		):

		# In addition to all of the equipment for a standard post...
		super(LetterSection, self).__init__(
			post,
			user,
			*args,
			id_prefix=id_prefix,
			**kwargs
		)

		# We need a list of all the senders of the letter...
		self.resenders = set([
			l.user
			for l in Letter.objects
				.exclude(user=self.post.user)
				.filter(parent_letter=self.post)
		])

		# And we also need a resend-letter form.
		self.resend_form = ResendLetterForm(
			initial={
				'parent_letter': self.post,
				'target': self.post.target,
				'user': user,
				'valence': self.post.valence,
				'title': self.post.title,
				'recipients': self.post.recipients.all(),
				'text': self.post.text
			},
			id_prefix=self.id_prefix
		)



class AbstractView(object):

	# override this with desired template
	template = 'digidemo/__base.html'


	# Top-level request handler.
	# Give this function to the url resolver in urls.py.
	def view(self, request, *args, **kwargs):

		# Register the views arguments for easy access
		self.request = request
		self.args = args
		self.kwargs = kwargs

		# Delegate to a response handler
		if self.request.POST:
			return self.handle_post()

		else:
			return self.handle_get()


	# handles get requests.  Usually you don't need to override this.
	# Instead override to which it delegates
	def handle_get(self):
		# Create the response
		template = self.get_template()
		context = self.get_context()
		reply = HttpResponse(template.render(context))

		# Return the response
		return reply


	# This is hook makes it possible to do fancy template relolution.
	# But usually, a view should just override the `template` attribute.
	def get_template(self):
		return get_template(self.template)


	# Preloads the context with stuff that pretty much every view should have
	def get_default_context(self):

		return {
			'GLOBALS': get_globals(self.request),
			'django_vars_js': get_django_vars_JSON(request=self.request),
			'user': self.request.user
		}


	# Usually you should override get_context_data instead of this,
	# Which let's you keep the default context in tact.
	def get_context(self):
		context_data = self.get_default_context()
		context_data.update(self.get_context_data())
		return RequestContext(self.request, context_data)


	# Usually this is the only function to override.
	def get_context_data(self):
		raise NotImplementedError('Subclasses of AbstractView must override'
				+ ' get_context_data')

	
	# handles post requests.  Usually you'll want to override the functions
	# to which it delegates, rather than this itself.
	def handle_post(self):
		# Create the response
		template = self.get_template()
		context = self.get_post_context()
		reply = HttpResponse(template.render(context))

		# Return the response
		return reply


	# Usually you should override get_post_context_data instead of this,
	# which let's you keep the default context in tact.
	def get_post_context(self):
		context_data = self.get_default_context()
		context_data.update(self.get_post_context_data())
		return RequestContext(self.request, context_data)


	# This default makes POST requests handled like GET, unless overriden.
	def get_post_context_data(self):
		return self.get_context_data()



# This provides a base for creating views which only logged in users
# should be able to access.
#
# As an additional, optional protection, if this is a view which handles
# post data from a form that contains a `user` field, a check can be
# performed to ensure that the user indicated in the form is the same as the
# logged in user.  To perform this check, provide the class of the form
# in which a field called `user` occurs as the value for form_class.
# To opt out of this verification, set check_form_user = False.
#
class AbstractLoginRequiredView(AbstractView):

	form_class = None
	check_form_user = True

	def get_login_url(self, request):
		return reverse('login_required', kwargs={'next_url':request.path})

	def view(self, request, *args, **kwargs):

		if not request.user.is_authenticated():
			return redirect(self.get_login_url(request))

		elif not get_profile(request.user).email_validated:
			return redirect(reverse('invalid_email'))

		# if the form_class is set, we'll do an extra check when form data
		# has been posted, to make sure that the logged in user is the same
		# as the user in the form's user field.  If not, force a logout
		if request.POST and self.check_form_user is not None:

			# Make sure that we haven't just forgotten to set up the user
			# form validation.  This requires that check_user_form is
			# explicitly set to False in order to opt out of the check.
			if self.form_class is None:
				raise NotImplementedError(
					'AbstractLoginRequiredView could '\
					'not verify the form user field, because form_class was '\
					'None. Either provide a proper form_class, or set '\
					'check_form_user = False.'
				)

			form = self.form_class(request.POST)
			form.is_valid()
			if form.cleaned_data['user'] != request.user:
				force_logout(request)
				return redirect(self.get_login_url(request))

		return super(AbstractLoginRequiredView, self).view(
			request, *args, **kwargs)


class Login(AbstractView):
	template = 'digidemo/login_page.html'
	error = False


	# By default (if `next_url` is not set), send the user to the front page.
	#
	def view(self, *args, **kwargs):
		next_url = kwargs.pop('next_url', reverse('mainPage'))
		return super(Login, self).view(*args, next_url=next_url, **kwargs)


	# Unauthenticated users get this page when accessing a login-required view
	def get_context_data(self):

		# Note, the request.path contains this login page url concatenated
		# with the original url they were trying to access
		login_form = LoginForm(endpoint=self.request.path)

		return {
			'GLOBALS': get_globals(self.request),
			'login_form': login_form,
			'error': self.error
		}


	# Handles displaying the empty form, ensures no error is printed
	def handle_get(self):
		self.error = False
		return super(Login,self).handle_get()


	# This handles the users login attempt
	def handle_post(self):

		login_success = login_user(
			self.request.POST['username'],
			self.request.POST['password'],
			self.request
		)

		if login_success == 'LOGIN_VALID_EMAIL':
			return redirect(self.kwargs['next_url'])

		elif login_success == 'LOGIN_INVALID_EMAIL':
			return redirect(reverse('invalid_email'))

		# Otherwise, show login form, but with an error message
		elif login_success == 'LOGIN_FAILED':
			self.error = True
			return super(Login, self).handle_get()



class InvalidEmail(AbstractView):
	template = 'digidemo/invalid_email.html'

	def get_context_data(self):
		return {}

		



# TODO: the cancel button won't work after an invalid form post
class EditProposalView(AbstractLoginRequiredView):

	template = 'digidemo/edit.html'
	form_class = ProposalVersionForm

	def get_context_data(self):

		proposal = get_object_or_404(Proposal, pk=self.kwargs['issue_id'])

		# Work out where the cancel button should point
		cancel_url = proposal.get_open_discussions_url()

		initial = {
			'proposal': proposal,
			'title': proposal.title,
			'summary': proposal.summary,
			'text': proposal.text,
			'user': self.request.user,
			'tags': ','.join([t.name for t in proposal.tags.all()]),
			'sectors': proposal.sectors.all(),
			'language': proposal.language
		}

		proposal_form = TaggedProposalForm(
			initial=initial,
			endpoint=proposal.get_edit_url()
		)
		

		return {
			'GLOBALS': get_globals(self.request),
			'headline': proposal.title,
			'proposal': proposal,
			'proposal_form': proposal_form,
			'tabs': get_proposal_tabs(proposal, EDIT_TAB_NAME),
			'active_navitem': 'create',
			'cancel_url': cancel_url
		}


	def handle_post(self):

		proposal = get_object_or_404(Proposal, pk=self.kwargs['issue_id'])

		proposal_form = TaggedProposalForm(
			data=self.request.POST,
			endpoint=proposal.get_edit_url()
		)

		if proposal_form.is_valid():

			proposal_version = proposal_form.save()

			# while saving the form above, publication is suppressed.
			# publish now.
			proposal = proposal_version.proposal
			proposal.subscribe(reason='EDITOR')
			proposal.publish(event_type='EDIT_ISSUE')

			return redirect(proposal.get_proposal_url())

		# Otherwise, make the context to dislpay the form

		# Work out where the cancel button should point
		cancel_url = proposal.get_open_discussions_url()

		# Assemble the context data on top of default context
		context_data = self.get_default_context()
		context_data.update({
			'proposal': proposal,
			'headline': proposal.title,
			'proposal_form': proposal_form,
			'tabs': get_edit_tabs('edit', proposal),
			'active_navitem': 'create',
			'cancel_url': cancel_url
		})

		# Build a request context
		context = RequestContext(self.request, context_data)

		# Render the response
		return HttpResponse(self.get_template().render(context))



class AddProposalView(AbstractLoginRequiredView):

	template = 'digidemo/add_proposal.html'
	form_class = ProposalVersionForm

	# We need to override handle_post, because a successful form post should
	# cause a rediret
	def handle_post(self):

		proposal_form = TaggedProposalForm(
			data=self.request.POST,
			endpoint=reverse('add_proposal')
		)

		# If the form is correctly filled out, save it and redirect
		# to the issue page
		if proposal_form.is_valid():
			proposal_version = proposal_form.save()
			proposal = proposal_version.proposal
			proposal.subscribe(reason='AUTHOR')
			proposal.publish(event_type='ISSUE')
			return redirect(proposal.get_url_by_view_name('proposal'))

		# Otherwise, make the context to dislpay the form

		# Work out where the cancel button should point
		cancel_url = reverse('mainPage')
		if 'HTTP_REFERER' in self.request.META:
			cancel_url = self.request.META['HTTP_REFERER']

		# Assemble the context data on top of default context
		context_data = self.get_default_context()
		context_data.update({
			'headline': 'new issue',
			'proposal_form': proposal_form,
			'tabs': None,
			'active_navitem': 'create',
			'cancel_url': cancel_url
		})

		# Build a request context
		context = RequestContext(self.request, context_data)

		# Render the response
		return HttpResponse(self.get_template().render(context))


	def get_context_data(self):

		proposal_form = TaggedProposalForm(
			endpoint=reverse('add_proposal'),
			initial={
				'user': self.request.user,
				'language': self.request.LANGUAGE_CODE
			}
		)

		cancel_url = reverse('mainPage')
		if 'HTTP_REFERER' in self.request.META:
			cancel_url = self.request.META['HTTP_REFERER']

		return {
			'GLOBALS': get_globals(self.request),
			'headline': 'new issue',
			'proposal_form': proposal_form,
			'tabs': None,
			'active_navitem': 'create',
			'cancel_url': cancel_url
		}



class TagListView(AbstractView):
	template = 'digidemo/tags.html'

	def get_context_data(self):
		sectors = []
		sector_set_names = [
			['education', 'health', 'democracy'],
			['economy', 'environment', 'culture'],
			['readiness', 'relations']
		]

		sector_sets = []
		for sector_names in sector_set_names:
			sector_set = []
			for name in sector_names:
				s = Sector.objects.get(name=name)
				sector_set.append({
					'sector': s,
					'tags': Tag.objects.filter(sector=s)
				})

			sector_sets.append(sector_set)
				

		return {
			'GLOBALS': get_globals(self.request),
			'sector_sets': sector_sets,
			'active_navitem': TOPICS_NAV_NAME
		}


class IssueListView(AbstractView):
	template = 'digidemo/issue_list.html'

	def get_context_data(self):
		
		# get the list of issues, sorted in the desired way
		order_by = self.kwargs.pop('order_by', 'interesting')

		print self.request.LANGUAGE_CODE

		issue_list = Proposal.objects.filter(
			language=self.request.LANGUAGE_CODE)

		sector = self.kwargs.pop('sector', None)
		sector_title = ''
		if sector is not None:
			sector = Sector.objects.get(name=sector)
			sector_title = ' : ' + __(sector.name) if sector is not None else ''
			issue_list = issue_list.filter(sectors=sector)

		tag = self.kwargs.pop('tag', None)
		tag_title = ''
		if tag is not None:
			tag = Tag.objects.get(name=tag)
			tag_title = ' : ' + tag.name if tag is not None else ''
			issue_list = issue_list.filter(tags=tag)

		if order_by == 'interesting':
			issues = issue_list.order_by('-last_modified')

		elif order_by == 'newest':
			issues = issue_list.order_by('-creation_date')

		elif order_by == 'activity':
			issues = issue_list.order_by('-creation_date')

		elif order_by == 'location':
			issues = issue_list.order_by('-creation_date')

		# build the tabs, and show the right tab as active
		tabs = get_issue_list_tabs(order_by)

		return {
			'GLOBALS': get_globals(self.request),
			'tag_title': tag_title,
			'sector_title': sector_title,
			'issues': issues,
			'tabs': tabs,
			'active_navitem': ISSUE_NAV_NAME
		}



class AllPetitionsListView(AbstractView):
	template = 'digidemo/all_petitions_list.html'

	def get_context_data(self):

		# get the list of petitions, sorted in the desired way
		order_by = self.kwargs['order_by'] or 'interesting'
		petitions = Letter.objects.filter(parent_letter=None,
			target__language=self.request.LANGUAGE_CODE)

		if order_by == 'interesting':
			petitions = petitions.order_by('-last_modified')

		elif order_by == 'newest':
			petitions = petitions.order_by('-creation_date')

		elif order_by == 'activity':
			petitions = petitions.order_by('-score')

		elif order_by == 'location':
			petitions = petitions.order_by('-creation_date')

		# build the tabs, and show the right tab as active
		tabs = get_petition_list_tabs(order_by)

		return {
			'GLOBALS': get_globals(self.request),
			'link_find_issue': reverse('issue_list', 
				kwargs={'order_by':'interesting'}),
			'link_add_issue':reverse('add_proposal'),
			'letters': petitions,
			'tabs': tabs,
			'active_navitem': OPINION_NAV_NAME
		}


class AllQuestionsListView(AbstractView):
	template = 'digidemo/all_questions_list.html'

	def get_context_data(self):

		# get the list of questions, sorted in the desired way
		order_by = self.kwargs['order_by'] or 'interesting'
		questions = Question.objects.filter(
			target__language=self.request.LANGUAGE_CODE)

		if order_by == 'interesting':
			questions = questions.order_by('-last_modified')

		elif order_by == 'newest':
			questions = questions.order_by('-creation_date')

		elif order_by == 'activity':
			questions = questions.order_by('-creation_date')

		elif order_by == 'location':
			questions = questions.order_by('-creation_date')

		# build the tabs, and show the right tab as active
		tabs = get_question_list_tabs(order_by)

		return {
			'GLOBALS': get_globals(self.request),
			'questions': questions,
			'tabs': tabs,
			'active_navitem': QUESTIONS_NAV_NAME
		}



class MakePost(AbstractLoginRequiredView):

	template = 'digidemo/make_post.html'
	form_class = None
	target_class = None
	active_navitem = None
	subtitle = None

	def get_headline_icon_url(self):
		raise NotImplementedError

	def get_form_endpoint(self):
		raise NotImplementedError

	def get_tabs(self):
		raise NotImplementedError


	def get_context_data(self):

		self.target = self.target_class.objects.get(
			pk=self.kwargs['target_id'])

		form = self.form_class(
			initial={'user':self.request.user, 'target':self.target},
			endpoint=self.get_form_endpoint()
		)

		return 	{
			'GLOBALS': get_globals(self.request),
			'headline': self.target.title,
			'target': self.target,
			'tabs': self.get_tabs(),
			'form': form,
			'active_navitem': self.active_navitem,
			'headline_icon_url': self.get_headline_icon_url(),
			'subtitle': self.subtitle
		}


	def handle_post(self):

		self.target = self.target_class.objects.get(
			pk=self.kwargs['target_id'])

		form = self.form_class(
			self.request.POST,
			endpoint=self.get_form_endpoint()
		)

		# If the form is valid, save question and redirect to the
		# question view page
		if form.is_valid():
			post = form.save()
			return redirect(post.get_url())

		# If the form wasn't valid, we don't redirect.
		# build the context
		context_data = {
			'GLOBALS': get_globals(self.request),
			'django_vars_js': get_django_vars_JSON(request=self.request),
			'headline': self.target.title,
			'target': self.target,
			'tabs': self.get_tabs(),
			'form': form,
			'active_navitem': self.active_navitem,
			'headline_icon_url': self.get_headline_icon_url(),
			'subtitle': self.subtitle
		}

		context = RequestContext(self.request, context_data)

		# get the template
		template = self.get_template()

		# return the reply
		return HttpResponse(template.render(context))


class AskQuestionView(MakePost):
	form_class = QuestionForm
	target_class = Proposal
	active_navitem = QUESTIONS_NAV_NAME
	subtitle = _('Ask a question')

	def get_headline_icon_url(self):
		return static('digidemo/images/question_icon.png')

	def get_tabs(self):
		return get_proposal_tabs(self.target, 'questions')

	def get_form_endpoint(self):
		return self.target.get_question_url()


class StartDiscussionView(MakePost):
	form_class = DiscussionForm
	target_class = Proposal
	active_navitem = ISSUE_NAV_NAME
	subtitle = _('Start a discussion')

	def get_headline_icon_url(self):
		return static('digidemo/images/comment_icon_med.png')

	def get_tabs(self):
		return get_proposal_tabs(self.target, EDIT_TAB_NAME)

	def get_form_endpoint(self):
		return self.target.get_start_discussion_url()


class StartPetitionView(MakePost):
	form_class = LetterForm
	target_class = Proposal
	active_navitem = OPINION_NAV_NAME
	subtitle = _('Write an open letter')

	def get_headline_icon_url(self):
		return static('digidemo/images/petition_icon.png')

	def get_tabs(self):
		return get_proposal_tabs(self.target, OPINION_TAB_NAME)

	def get_form_endpoint(self):
		return self.target.get_start_petition_url()



class IssueOverview(AbstractView):
	template = 'digidemo/overview.html'

	def get_context_data(self):
		proposal = get_object_or_404(Proposal,
			pk=self.kwargs['proposal_id'])
		questions = Question.objects.filter(target=proposal)

		# Get all of the letters which are associated with this proposal
		# and which are 'original letters'
		letter_sections = []
		letters = Letter.objects.filter(parent_letter=None, target=proposal)
		for letter in letters:
			letter_section = LetterSection(letter, self.request.user)
			letter_sections.append(letter_section)

		return {
			'GLOBALS': get_globals(self.request),
			'proposal': proposal,
			'num_questions': questions.count,
			'questions': questions[0:5],
			'letter_sections': letter_sections,
			'tabs': get_proposal_tabs(proposal, OVERVIEW_TAB_NAME),
			'active_navitem': ISSUE_NAV_NAME
		}


class PostAreaView(AbstractView):

	# Override these with the appropriate templates, models, and forms
	Post = None
	PostSection = None
	Subpost = None
	SubpostSection = None
	SubpostForm = None

	# Other inheritance-based options
	template = 'digidemo/post_area.html'
	active_navitem = None
	active_tab = None

	def get_context_data(self):

		# The following class attributes should be overriden
		concrete_attributes = [self.Post, self.PostSection, self.Subpost,
			self.SubpostSection, self.SubpostForm]

		# So none of them should be None if this method is being called...
		if any([attr is None for attr in concrete_attributes]):
			raise NotImplementedError('To use PostAreaView you must override'
				' each of %s.' % ', '.join(
					[str(attr) for attr in concrete_attributes]
				)
			)

		post = self.Post.objects.get(pk=self.kwargs['post_id'])
		target = post.target

		# make a section for the question
		post_section = self.PostSection(
			post, self.request.user, id_prefix='q')

		# make sections for subposts
		subpost_sections = []
		for subpost in self.Subpost.objects.filter(target=post):
			subsection = self.SubpostSection(subpost, self.request.user)
			subpost_sections.append(subsection)

		# make a form for submitting new answers
		subpost_form = self.SubpostForm(
			initial={'user':self.request.user, 'target':post})

		return {
			'GLOBALS': get_globals(self.request),
			'post_section': post_section,
			'subpost_sections': subpost_sections,
			'subpost_form': subpost_form,
			'headline': target.title,
			'proposal': target,
			'tabs': get_proposal_tabs(target, self.active_tab),
			'active_navitem': self.active_navitem
		}



class PetitionListView(AbstractView):
	template = 'digidemo/petition_list.html'

	def get_context_data(self):

		# get the current proposal
		proposal = get_object_or_404(Proposal,
			pk=self.kwargs['proposal_id']
		)

		# Get all of the letters which are associated with this proposal
		# and which are 'original letters'
		letter_sections = []
		letters = Letter.objects.filter(parent_letter=None, target=proposal)
		for letter in letters:
			letter_section = LetterSection(letter, self.request.user)
			signed=False

			if not self.request.user.is_authenticated():
				signed = False
			elif letter.user.pk == self.request.user.pk:
				signed=True
			elif letter.resent_letters.filter(
				user__pk=self.request.user.pk).count()>0:
				signed=True

			print letter.resent_letters.count()
			print '****' + self.request.user.username

			letter_section.signed = signed
			letter_sections.append(letter_section)

		return {
			'GLOBALS': get_globals(self.request),
			'section_title': '%d Petitions' % letters.count(),
			'proposal': proposal,
			'letter_sections': letter_sections,
			'headline': proposal.title,
			'tabs': get_proposal_tabs(proposal, OPINION_TAB_NAME),
			'active_navitem': OPINION_NAV_NAME
		}



class DiscussionListView(AbstractView):
	template = 'digidemo/discussion_list.html'

	def get_discussions_to_show(self):
		if self.kwargs['open_status'] == 'open':
			return self.open_discussions

		elif self.kwargs['open_status'] == 'closed':
			return self.closed_discussions

		else:
			raise Http404


	def get_context_data(self):

		# Decide which button will be highlighted, and catch the case
		# where a nonsense open_status was given in the url
		if self.kwargs['open_status'] == 'open':
			highlighted = 'open'
		elif self.kwargs['open_status'] == 'closed':
			highlighted = 'closed'
		else:
			raise Http404

		proposal = get_object_or_404(Proposal,
			pk=self.kwargs['issue_id'])

		self.open_discussions = Discussion.objects.filter(
			target=proposal,
			is_open=True
		)

		self.closed_discussions = Discussion.objects.filter(
			target=proposal,
			is_open=False
		)

		return {
			'GLOBALS': get_globals(self.request),
			'section_title': 'Welcome to the editor\'s area',
			'issue': proposal,
			'headline': proposal.title,
			'items': self.get_discussions_to_show(),
			'open_items': self.open_discussions,
			'closed_items': self.closed_discussions,
			'tabs': get_proposal_tabs(proposal, EDIT_TAB_NAME),
			'active_navitem': 'create',
			'highlighted': highlighted
		}


# The only differences with the closed discussion list is that we show
# the closed discussions, and we highlight the closed discussions button
class ClosedDiscussionListView(DiscussionListView):
	highlighted = 'closed'
	def get_discussions_to_show(self):
		return self.closed_discussions


class QuestionListView(AbstractView):
	template = 'digidemo/question_list.html'

	def get_context_data(self):
		proposal = get_object_or_404(Proposal,
			pk=self.kwargs['proposal_id'])
		questions = Question.objects.filter(target=proposal)

		return {
			'GLOBALS': get_globals(self.request),
			'section_title': '%d Questions' % questions.count(),
			'proposal': proposal,
			'target': proposal,
			'headline': proposal.title,
			'items': questions,
			'tabs': get_proposal_tabs(proposal, QUESTIONS_TAB_NAME),
			'active_navitem': QUESTIONS_NAV_NAME
		}


class PetitionView(AbstractView):
	template = 'digidemo/view_petition.html'

	def get_context_data(self):
		letter = Letter.objects.get(pk=self.kwargs['petition_id'])
		proposal = letter.target
		letter_section = LetterSection(letter, self.request.user)

		# figure out if the user has already signed this letter
		signed = False
		if not self.request.user.is_authenticated():
			signed = False
		elif letter.user == self.request.user:
			signed = True
		elif letter.resent_letters.filter(user=self.request.user).count()>0:
			signed = True

		return {
			'GLOBALS': get_globals(self.request),
			'signed': signed,
			'headline': proposal.title,
			'proposal': proposal,
			'letter_section': letter_section,
			'tabs': get_proposal_tabs(proposal, OPINION_TAB_NAME),
			'active_navitem': OPINION_TAB_NAME
		}


class QuestionAreaView(PostAreaView):
	template = 'digidemo/view_question.html'
	Post = Question
	PostSection = QuestionSection
	Subpost = Answer
	SubpostSection = AnswerSection
	SubpostForm = AnswerForm
	active_tab = QUESTIONS_TAB_NAME
	active_navitem = QUESTIONS_NAV_NAME


class DiscussionAreaView(PostAreaView):
	template = 'digidemo/view_discussion.html'
	Post = Discussion
	PostSection = DiscussionSection
	Subpost = Reply
	SubpostSection = ReplySection
	SubpostForm = ReplyForm
	active_tab = OVERVIEW_TAB_NAME
	active_navitem = ISSUE_NAV_NAME


def show_test_page(request):
	return render(request, 'digidemo/test.html', {})


# A simple way to force reload from the server.
# This allows one to trigger a reload without the risk of re-posting form data
def do_reload(request):
	return redirect(request.META['HTTP_REFERER'])
	

class AllPetitionListView(object):
	def view(self, request):
		return mainPage(request)


def what_about(request,sort_type='most_recent'):

	return render(
		request,
		'digidemo/what_about.html',
		{
			'GLOBALS': get_globals(request),
			'django_vars_js': get_django_vars_JSON(request=request)
		}
	)

#def find_issues(request,sort_type='most_recent'):
#
#	if(sort_type=='most_recent'):
#		proposals = Proposal.language_filtered.all(request
#			).order_by('-creation_date')[:5]
#	elif(sort_type=='top_score'):
#		proposals = Proposal.language_filtered.all(request
#			).order_by('-score')[:5]
#
#	active_issues =  Proposal.objects.order_by('-score')[:6]
#	featured_post = Proposal.objects.get(pk=1);
#	users = UserProfile.objects.all();
#	new_petitions = Letter.objects.all()
#
#        
#	return render(
#		request,
#		'digidemo/index.html',
#		{
#			'GLOBALS': get_globals(request),
#			'django_vars_js': get_django_vars_JSON(request=request),
#			'users': users,
#			'active_issues': active_issues,
#			'featured_post': featured_post,
#			'new_petitions': new_petitions
#		}
#	)


def mainPage(request,sort_type='most_recent'):

	# get lists of issues
	proposals = Proposal.objects.filter(language=request.LANGUAGE_CODE)

	if(sort_type=='most_recent'):
		proposals = proposals.order_by('-creation_date')[:5]
	elif(sort_type=='top_score'):
		proposals = proposals.order_by('-score')[:5]

	active_issues = Proposal.objects.filter(language=request.LANGUAGE_CODE
		).order_by('-score')[:6]

	# take the earliest issue as the featured post
	featured_post = None
	try:
		featured_post = Proposal.objects.filter(
			language=request.LANGUAGE_CODE)[0];
	except IndexError:
		pass

	# what are we doing with all of the users here?
	users = UserProfile.objects.all();

	# and with all of the petitions?
	new_petitions = Letter.objects.all()

        
	return render(
		request,
		'digidemo/index.html',
		{
			'GLOBALS': get_globals(request),
			'django_vars_js': get_django_vars_JSON(request=request),
			'users': users,
			'active_issues': active_issues,
			'featured_post': featured_post,
			'new_petitions': new_petitions
		}
	)


def userRegistration(request):
	if(request.method == 'POST'):
		reg_form = UserRegisterForm(
			request.POST,
			endpoint=reverse('userRegistration')
		)
		
		# before validating the form, check if the email already exists
		# if so, we show the user an option to recover their credentials.
		try:
			email = request.POST['email']

		# if blank, forget about this check
		except KeyError:
			pass

		else:
			email_exists = User.objects.filter(email=email).count() > 0
			if email_exists:

				return render(
					request,
					'digidemo/register.html',
					{
						'GLOBALS': get_globals(request),
						'form': None,
						'email_exists': True, # changes how template displays
						'django_vars_js': get_django_vars_JSON(
							request=request)
					}
				)

		if reg_form.is_valid():

			new_user = User.objects.create_user(
				password = reg_form.cleaned_data['password'],
				username = reg_form.cleaned_data['username'],
				email = reg_form.cleaned_data['email'],
				first_name = reg_form.cleaned_data['first_name'],
				last_name = reg_form.cleaned_data['last_name']
			)

			user_profile = UserProfile(user=new_user)
			user_profile.save()

			# make a default avatar
			foreground = [ 
				"rgb(45,79,255)",
				"rgb(254,180,44)",
				"rgb(226,121,234)",
				"rgb(30,179,253)",
				"rgb(232,77,65)",
				"rgb(49,203,115)",
				"rgb(141,69,170)" 
			] 
			background = "rgb(224,224,224)"
			avatar_generator = pydenticon.Generator(
				8,8, foreground=foreground, background=background)
			avatar = avatar_generator.generate(
				new_user.username,240,240,output_format='png')

			img_dir = os.path.join(TEMP_DIR, '%s.png' % new_user.username)
			f = open(img_dir, 'wb')
			f.write(avatar)
			f.close()
			f = open(img_dir, 'r')
			user_profile.avatar_img.save(
				'%s.png' % new_user.username,
				File(f)
			)
			send_email_confirmation(new_user, request)
			return redirect(reverse('mail_sent'))

	else:
		reg_form = UserRegisterForm(
		endpoint=reverse('userRegistration'))

 
	return render(
		request,
		'digidemo/register.html',
		{
			'GLOBALS': get_globals(request),
			'form' : reg_form,
			'email_exists': False,
			'django_vars_js': get_django_vars_JSON(request=request)
		}
	)


def resend_email_confirmation(request):

		# only logged in users should be able to resend the verification email
		user = request.user
		if not user.is_authenticated():
			return HttpResponseForbidden()

		# only send the verification email if their email isn't validated
		if not get_profile(user).email_validated:
			send_email_confirmation(user, request)

		# Show the mail sent page
		return mail_sent(request)


def mail_sent(request):
	return render(
		request,
		'digidemo/check_your_mail.html',
		{
			'GLOBALS': get_globals(request),
			'django_vars_js': get_django_vars_JSON(request=request)
		}
	)


def verify_email(request, code):
	user = get_object_or_404(EmailVerification, code=code).user
	user_profile = get_profile(user)
	user_profile.email_validated = True
	user_profile.save()

	return render(
		request,
		'digidemo/validated.html',
		{
			'GLOBALS': get_globals(request),
			'django_vars_js': get_django_vars_JSON(request=request)
		}
	)


def resetPassword(request):
	if(request.method == 'POST'):
		pass_reset_form = ResetPasswordForm(
			request.POST,
			endpoint=reverse('resetPassword')
		)
		
		if pass_reset_form.is_valid():
			user = User.objects.get(
				username = pass_reset_form.cleaned_data['username'],
				email = pass_reset_form.cleaned_data['email']
			)
			new_password = str(uuid4()).replace('-', '')[:8]
			user.set_password(new_password)
			user.save()
			user.email_user(
				subject=_('Luminocracy.org Password Reset'),
				message=_('Your new luminocracy.org password is: %s')
					% new_password,
				from_email=_('support@luminocracy.org')
			)

			return mainPage(request)

	else:
		pass_reset_form = ResetPasswordForm(endpoint=reverse('resetPassword'))
 
	return render(
		request,
		'digidemo/reset_password.html',
		{
			'GLOBALS': get_globals(request),
			'form' : pass_reset_form,
			'django_vars_js': get_django_vars_JSON(request=request)
		}
	)


def get_default_context(request):

	return {
		'GLOBALS': get_globals(request),
		'django_vars_js': get_django_vars_JSON(request=request),
		'user': request.user
	}


def search(request):
	"""
		Search > Root
	"""

	# we retrieve the query to display it in the template
	form =ProposalSearchForm(request.GET)

	# we call the search method from the NotesSearchForm. Haystack do the work!
	results = form.search()

	# get the default context
	context = get_default_context(request)
	context.update({'notes':results})
	return render(
		request,
		'search/search.html',
		context
	)

def users(request):

	listToReturn = []
	
	if request.POST:
		dictionary ={};

		for user in UserProfile.objects.all():
			dictionary[user] = lev(
				user.user.username,request.POST['userName'])

		# Use this for descending order
		# for w in sorted(dictionary,key=dictionary.get,reverse=True)

		for user in sorted(dictionary, key=dictionary.get):
			listToReturn.append(user);

	return render(
		request,'digidemo/users.html',
		{
			'GLOBALS': get_globals(request),
			'django_vars_js': get_django_vars_JSON(request=request),
			'usersList' : listToReturn,
		}
	)

# A dry view for displaying the userProfile
# Every profile is public
# Read the userName from the URL, get the obkect and send it to the view
# TO - DO : Establish the distinction of making the user profile public or private

def userProfile(request, userName) :
	userLoggedIn = User.objects.get(username = userName);
	userProfile = UserProfile.objects.get(user = userLoggedIn);
	return render (request, 'digidemo/userProfile.html',
		{
			'GLOBALS': get_globals(request),
			'django_vars_js': get_django_vars_JSON(request=request),
			'user' : userLoggedIn,
		}
	)


# View used for editing the userProfile
# If the request is a POST request, the user has made changes to the form. The changes are accepted and redirected to display the userProfile page
# If the user has uploaded an image, the image is uploaded and linked appropriately
# Else, the normal userProfileEdit page is shown with prefilled data.
#TO -DO : Write a python script to automatically which images are not linked to any userProfile and delete them
# Django has a good mechanism where same files are renamed and linked
# Alaternatively you could check if the user has uploaded an image previously and delete it and upload a different one

def userProfileEdit(request,userName) :

	userLoggedIn = User.objects.get(username = userName);
	userProfileLoggedIn = UserProfile.objects.get(user = userLoggedIn);

	if request.method == 'POST':

		userLoggedIn.first_name = request.POST['fname'];
		userLoggedIn.last_name = request.POST['lname'];
		userLoggedIn.email = request.POST['email'];

		userLoggedIn.save();

		userProfileLoggedIn.street = request.POST['street'];
		userProfileLoggedIn.zip_code = request.POST['zip_code']
		userProfileLoggedIn.country = request.POST['country']
		userProfileLoggedIn.province = request.POST['province']

		if 'image' in request.FILES:
			uploadedImage = request.FILES['image'];
			uploadedImage.name = userName;
			userProfileLoggedIn.avatar_img = uploadedImage;

		userProfileLoggedIn.save();
   	
		return (userProfile(request,userName))
        
	else :
        
		try :
			if (request.session['user'] != userName):
				return(errorPage(request,"No Necessary Permissions"));

		except :
			return(errorPage(
				request,"You have not been authorised to access the page"));
		
		return render(
			request,
			'digidemo/userProfileEdit.html',
			{
				'GLOBALS': get_globals(request),
				'django_vars_js': get_django_vars_JSON(request=request),
				'user' : userProfileLoggedIn,
				'country':COUNTRIES,
			}
		)


def errorPage(request, error):
	return render(
		request,
		'digidemo/errorPage.html',
		{
			'GLOBALS': get_globals(request),
			'django_vars_js': get_django_vars_JSON(request=request),
			'error' : error,
		}
	)


#        ,------,   ,----------------------,
#   o O <` WAT? |  | levinshtein distance!	>  * *
#    ^   \______,   \______________________/    _
#
def lev(a, b):
	if not a: return len(b)
	if not b: return len(a)
	return min(
		lev(a[1:], b[1:]) + (a[0] != b[0]),
		lev(a[1:], b) + 1,
		lev(a, b[1:])+1
	)


def get_notification_message(notification):

	source_user = notification.source_user.username
	event_type = notification.event_type
	event_data = notification.event_data
	reason = notification.reason

	# this case is easy
	if event_type=='VOTE':
		try:
			if int(event_data) == 1:
				return "your post was upvoted!"
			elif int(event_data) == -1:
				return "your post was downvoted"
			else:
				return "someone voted on your post"
		except ValueError:
			return "someone voted on your post"

	# so is this one
	if event_type=='SYSTEM':
		return notification.event_data

	# the rest of the cases we need to get a user and an action
	# user is always source_user.  But we need to figure out the action:
	if event_type=='ISSUE':
		action = "started an issue in a topic you're watching"

	elif event_type=='EDIT_ISSUE':
		action = "edited an issue you're watching"

	elif event_type=='QUESTION':
		action = "asked a question in an issue you're watching"

	elif event_type=='ANSWER':
		action = 'answered a question'
		if reason == 'AUTHOR':
			action += ' you asked'
		elif reason == 'COMMENTER':
			action += ' you commented on'
		else:
			action += " you're watching"

	elif event_type=='DISCUSSION':
		action = "posted in an issue you're watching"

	elif event_type =='REPLY':
		action = 'replied to a post'
		if reason == 'AUTHOR':
			action += ' you wrote'
		elif reason == 'COMMENTER':
			action += ' you commented on'
		else:
			action += " you're watching"


	elif event_type=='COMMENT':
		action = 'commented on a post'
		if reason == 'AUTHOR':
			action += ' you wrote'
		elif reason == 'COMMENTER':
			action += ' you also commented on'
		else:
			action += " you're watching"

	elif event_type=='LETTER':
		action = ("sent a letter in relation to an issue "
			"you're watching")

	elif event_type=='SIGN_LETTER':
		action = 'signed a letter'
		if reason == 'AUTHOR':
			action += ' you wrote'
		elif reason == 'COMMENTER':
			action += ' you commented on'
		else:
			action += " you're watching"

	message = '%s %s' % (source_user, action)
	return message
