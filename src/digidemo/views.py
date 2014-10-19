import difflib
import collections as c

from django.core import serializers
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.forms.formsets import formset_factory
from django import http
from django.views.debug import ExceptionReporter
from django.conf import settings

from digidemo.models import *
from digidemo.forms import *
from digidemo import utils
from digidemo.utils import force_logout
from forms import ProposalSearchForm
from settings import DEBUG 

import json
import sys
from choices import *;


# Names we use for the tabs in proposal sections
OVERVIEW_TAB_NAME = 'issue'
QUESTIONS_TAB_NAME = 'questions'
OPINION_TAB_NAME = 'petitions'
EDIT_TAB_NAME = 'editing room'

# Names we use for the top level "button" navigation
ISSUE_NAV_NAME = 'issues'
TOPICS_NAV_NAME = 'topics'
CREATE_NAV_VAME = 'create'
QUESTIONS_NAV_NAME = 'questions'
OPINION_NAV_NAME = 'petitions'
USERS_NAV_NAME = 'users'


def get_proposal_tabs(proposal, active_tab):

	# This is the basic tabs definition for the proposal views
	proposal_tabs = [
		{'name': OVERVIEW_TAB_NAME,'url': proposal.get_proposal_url()},
		{'name': QUESTIONS_TAB_NAME,'url': proposal.get_question_list_url()},
		{'name': OPINION_TAB_NAME,'url': proposal.get_petitions_url()},
		{'name': EDIT_TAB_NAME,'url': proposal.get_open_discussions_url()},
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
		{
			'name': 'location',
			'url': reverse('issue_list', kwargs={'order_by':'location'})
		},
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
		{
			'name': 'location',
			'url': reverse('all_petitions_list', 
				kwargs={'order_by':'location'})
		},
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
		{
			'name': 'location',
			'url': reverse('all_questions_list', 
				kwargs={'order_by':'location'})
		},
	]

	# mark the active tab as active
	active_index = [t['name'] for t in question_list_tabs].index(active_tab)
	question_list_tabs[active_index]['active'] = True

	return question_list_tabs

	
def get_globals():
	return {
		'DEBUG': DEBUG
	}


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
	django_vars = {
		'DEBUG': DEBUG,
		'IS_USER_AUTHENTICATED': request.user.is_authenticated()
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



def history(request, proposal_id):

	# ** Hardcoded the logged in user to be enewe101 **
	logged_in_user = User.objects.get(pk=1)

	proposal = Proposal.objects.get(pk=proposal_id)

	# make a proposal vote form
	proposal_vote_form = get_vote_form(
		ProposalVote, ProposalVoteForm, logged_in_user, proposal)

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
			'django_vars_js': get_django_vars_JSON(request=request),
			'proposal': proposal,
			'proposal_vote_form': proposal_vote_form,
			'logged_in_user': logged_in_user,
			'diff_table': diff_table,
			'active_navitem': 'issues',
			'tabs': get_proposal_tabs(proposal, 'edit')
		}
	)




def get_vote_form(VoteModel, VoteForm, user, target, id_prefix=''):

	existing_vote = utils.get_or_none(VoteModel, user=user.pk, target=target)
	
	# Only enable the form if the user is authenticated
	is_enabled = False
	tooltip = "You must login to vote!"
	if user.is_authenticated():
		is_enabled = True

		# Also, don't enable the form if the user is the author of the post!
		if (target.user == user):
			is_enabled = False
			tooltip = r"You can\'t vote on your own post!"


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

		logged_in_user = User.objects.get(pk=1)

		return {
			'globals': get_globals(),
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
	error = ''


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
			'login_form': login_form,
			'error': self.error
		}

	# This handles the users login attempt
	def handle_post(self):

		# try to authenticate the user
		user = authenticate(
			username=self.request.POST['username'],
			password=self.request.POST['password']
		)

		# If successful, get the original login-required url, which was
		# concatenated onto the login-required url, as the 'next' kwarg.
		if user:
			login(self.request, user)
			return redirect(self.kwargs['next_url'])

		# Otherwise, show login form, but with an error message
		else:
			self.error = 'Oops, try again...'
			return self.handle_get()


# TODO: the cancel button won't work after an invalid form post
class EditProposalView(AbstractLoginRequiredView):

	template = 'digidemo/edit.html'
	form_class = ProposalVersionForm

	def get_context_data(self):

		proposal = Proposal.objects.get(pk=self.kwargs['issue_id'])

		# Work out where the cancel button should point
		cancel_url = proposal.get_open_discussions_url()

		initial = {
			'proposal': proposal,
			'title': proposal.title,
			'summary': proposal.summary,
			'text': proposal.text,
			'user': self.request.user,
			'tags': ','.join([t.name for t in proposal.tags.all()]),
			'sectors': proposal.sectors.all()
		}

		proposal_form = TaggedProposalForm(
			initial=initial,
			endpoint=proposal.get_edit_url()
		)
		

		return {
			'headline': proposal.title,
			'proposal': proposal,
			'proposal_form': proposal_form,
			'tabs': get_proposal_tabs(proposal, EDIT_TAB_NAME),
			'active_navitem': 'create',
			'cancel_url': cancel_url
		}


	def handle_post(self):

		proposal = Proposal.objects.get(pk=self.kwargs['issue_id'])

		proposal_form = TaggedProposalForm(
			data=self.request.POST,
			endpoint=proposal.get_edit_url()
		)

		if proposal_form.is_valid():
			proposal_version = proposal_form.save()
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
			return redirect(proposal.get_url('proposal'))

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
			initial={'user': self.request.user}
		)

		cancel_url = reverse('mainPage')
		if 'HTTP_REFERER' in self.request.META:
			cancel_url = self.request.META['HTTP_REFERER']

		return {
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
			'sector_sets': sector_sets,
			'active_navitem': TOPICS_NAV_NAME
		}


class IssueListView(AbstractView):
	template = 'digidemo/issue_list.html'

	def get_context_data(self):
		
		# get the list of issues, sorted in the desired way
		order_by = self.kwargs['order_by'] or 'interesting'
		if order_by == 'interesting':
			issues = Proposal.objects.all().order_by('?')

		elif order_by == 'newest':
			issues = Proposal.objects.all().order_by('-creation_date')

		elif order_by == 'activity':
			issues = Proposal.objects.all().order_by('-creation_date')

		elif order_by == 'location':
			issues = Proposal.objects.all().order_by('-creation_date')

		# build the tabs, and show the right tab as active
		tabs = get_issue_list_tabs(order_by)

		return {
			'issues': issues,
			'tabs': tabs,
			'active_navitem': ISSUE_NAV_NAME
		}



class AllPetitionsListView(AbstractView):
	template = 'digidemo/all_petitions_list.html'

	def get_context_data(self):

		logged_in_user = User.objects.get(pk=1)

		# get the list of petitions, sorted in the desired way
		order_by = self.kwargs['order_by'] or 'interesting'
		if order_by == 'interesting':
			petitions = Letter.objects.filter(parent_letter=None).order_by('?')

		elif order_by == 'newest':
			petitions = Letter.objects.filter(parent_letter=None).order_by('-creation_date')

		elif order_by == 'activity':
			petitions = Letter.objects.filter(parent_letter=None).order_by('-creation_date')

		elif order_by == 'location':
			petitions = Letter.objects.filter(parent_letter=None).order_by('-creation_date')

		# build the tabs, and show the right tab as active
		tabs = get_petition_list_tabs(order_by)

		return {
			'letters': petitions,
			'tabs': tabs,
			'logged_in_user': logged_in_user,
			'active_navitem': OPINION_NAV_NAME
		}


class AllQuestionsListView(AbstractView):
	template = 'digidemo/all_questions_list.html'

	def get_context_data(self):

		logged_in_user = User.objects.get(pk=1)

		# get the list of questions, sorted in the desired way
		order_by = self.kwargs['order_by'] or 'interesting'
		if order_by == 'interesting':
			questions = Question.objects.all().order_by('?')

		elif order_by == 'newest':
			questions = Question.objects.all().order_by('-creation_date')

		elif order_by == 'activity':
			questions = Question.objects.all().order_by('-creation_date')

		elif order_by == 'location':
			questions = Question.objects.all().order_by('-creation_date')

		# build the tabs, and show the right tab as active
		tabs = get_question_list_tabs(order_by)

		return {
			'questions': questions,
			'tabs': tabs,
			'logged_in_user': logged_in_user,
			'active_navitem': QUESTIONS_NAV_NAME
		}



class MakePost(AbstractLoginRequiredView):

	template = 'digidemo/make_post.html'
	form_class = None
	target_class = None
	active_navitem = None

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
			'headline': self.target.title,
			'target': self.target,
			'tabs': self.get_tabs(),
			'form': form,
			'active_navitem': self.active_navitem,
			'headline_icon_url': self.get_headline_icon_url()
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
			'globals': get_globals(),
			'django_vars_js': get_django_vars_JSON(request=self.request),
			'headline': self.target.title,
			'target': self.target,
			'tabs': self.get_tabs(),
			'form': form,
			'active_navitem': self.active_navitem,
			'headline_icon_url': self.get_headline_icon_url()
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

	def get_headline_icon_url(self):
		return static('digidemo/images/petition_icon.png')

	def get_tabs(self):
		return get_proposal_tabs(self.target, OPINION_TAB_NAME)

	def get_form_endpoint(self):
		return self.target.get_start_petition_url()



class IssueOverview(AbstractView):
	template = 'digidemo/overview.html'

	def get_context_data(self):
		proposal = Proposal.objects.get(pk=self.kwargs['proposal_id'])
		questions = Question.objects.filter(target=proposal)

		# Get all of the letters which are associated with this proposal
		# and which are 'original letters'
		letter_sections = []
		letters = Letter.objects.filter(parent_letter=None, target=proposal)
		for letter in letters:
			letter_section = LetterSection(letter, self.request.user)
			letter_sections.append(letter_section)

		return {
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
		proposal = Proposal.objects.get(pk=self.kwargs['proposal_id'])

		# Get all of the letters which are associated with this proposal
		# and which are 'original letters'
		letter_sections = []
		letters = Letter.objects.filter(parent_letter=None, target=proposal)
		for letter in letters:
			letter_section = LetterSection(letter, self.request.user)
			letter_sections.append(letter_section)

		return {
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

		proposal = Proposal.objects.get(pk=self.kwargs['issue_id'])

		self.open_discussions = Discussion.objects.filter(
			target=proposal,
			is_open=True)

		self.closed_discussions = Discussion.objects.filter(
			target=proposal,
			is_open=False)

		return {
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
		proposal = Proposal.objects.get(pk=self.kwargs['proposal_id'])
		questions = Question.objects.filter(target=proposal)
		logged_in_user = User.objects.get(pk=1)

		return {
			'section_title': '%d Questions' % questions.count(),
			'proposal': proposal,
			'target': proposal,
			'headline': proposal.title,
			'items': questions,
			'logged_in_user': logged_in_user,
			'tabs': get_proposal_tabs(proposal, QUESTIONS_TAB_NAME),
			'active_navitem': QUESTIONS_NAV_NAME
		}


class PetitionView(AbstractView):
	template = 'digidemo/view_petition.html'

	def get_context_data(self):
		letter = Letter.objects.get(pk=self.kwargs['petition_id'])
		proposal = letter.target
		letter_section = LetterSection(letter, self.request.user)

		return {
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


def mainPage(request,sort_type='most_recent'):

	if(sort_type=='most_recent'):
		proposals = Proposal.objects.order_by('-creation_date')[:5]
	elif(sort_type=='top_score'):
		proposals = Proposal.objects.order_by('-score')[:5]

	active_issues =  Proposal.objects.order_by('-score')[:6]
	featured_post = Proposal.objects.get(pk=1);
	users = UserProfile.objects.all();
	new_petitions = Letter.objects.all()

        
	return render(
		request,
		'digidemo/proposal_index.html',
		{
			'django_vars_js': get_django_vars_JSON(request=request),
			'users': users,
			'active_issues': active_issues,
			'featured_post': featured_post,
			'new_petitions': new_petitions
		}
	)


def userRegistration(request):
	if(request.method == 'POST'):
		user = NameForm(request.POST)
		
		if user.is_valid():

			passwordPass = user.cleaned_data['password']
			userNamePass = user.cleaned_data['userName']
			emailPass = user.cleaned_data['email']
			firstNamePass = user.cleaned_data['firstName']
			lastNamePass = user.cleaned_data['lastName']

			userCreate = User.objects.create_user(
				username=userNamePass,
				email= emailPass,
				password = passwordPass,
				first_name = firstNamePass,
				last_name = lastNamePass
			)

			userCreate.save();
			streetPass = "";
			zipCodePass = "";
			countryPass =   "";
			provincePass =  "";

			userProfile = UserProfile(
				user=userCreate,
				email_validated = 0,
				rep=0,
				street = streetPass,
				country = countryPass,
				zip_code = zipCodePass,
				province = provincePass
			)

			userProfile.save();

		return redirect('../mainPage')
	
	registrationForm = NameForm();
 
	return render(
		request,
		'digidemo/User_registration.html',
		{ 
			'form' : registrationForm,
			'django_vars_js': get_django_vars_JSON(request=request)
		}
	)


def get_default_context(request):

	logged_in_user = User.objects.get(pk=1)

	return {
		'globals': get_globals(),
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
			'django_vars_js': get_django_vars_JSON(request=request),
			'user' : userProfile,
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
			'django_vars_js': get_django_vars_JSON(request=request),
			'error' : error,
		}
	)


#        ,------,
#   o O <` WAT? | 
#    ^   \______,
#    
def lev(a, b):
	if not a: return len(b)
	if not b: return len(a)
	return min(
		lev(a[1:], b[1:]) + (a[0] != b[0]), 
		lev(a[1:], b) + 1,
		lev(a, b[1:])+1
	)

