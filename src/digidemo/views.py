import difflib
from django.core.urlresolvers import reverse
from django.core import serializers
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from digidemo.models import *
from forms import ProposalSearchForm
from django.forms.formsets import formset_factory
from digidemo.forms import *
from digidemo import utils
from settings import DEBUG
import json
import sys
from django import http
from django.views.debug import ExceptionReporter


def get_proposal_tabs(proposal, active_tab):

	# This is the basic tabs definition for the proposal views
	proposal_tabs = [
		{'name': 'overview','url': proposal.get_overview_url()},
		{'name': 'proposal','url': proposal.get_proposal_url()},
		{'name': 'questions','url': proposal.get_question_list_url()},
		{'name': 'discuss','url': proposal.get_discussion_url()},
		{'name': 'edit','url': proposal.get_edit_url()}
	]

	# mark the active tab as active
	active_index = [t['name'] for t in proposal_tabs].index(active_tab)
	proposal_tabs[active_index]['active'] = True

	return proposal_tabs
	


def get_django_vars(additional_vars={}):
	django_vars = {
		'DEBUG': DEBUG
	}

	django_vars.update(additional_vars)

	return django_vars


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


def get_django_vars_JSON(additional_vars):
	return json.dumps(get_django_vars(additional_vars))


def overview(request, proposal_id):

	proposal = Proposal.objects.get(pk=proposal_id)
	context = make_proposal_context(proposal)
	context['tabs'] = get_proposal_tabs(proposal, 'overview')

	return render(
		request,
		'digidemo/overview.html', 
		context
	)


def proposal(request, proposal_id):
	proposal = Proposal.objects.get(pk=proposal_id)
	context = make_proposal_context(proposal)
	context['tabs'] = get_proposal_tabs(proposal, 'proposal')

	return render(
		request,
		'digidemo/proposal.html',
		context
	)


def add_proposal(request):

	# ** Hardcoded the logged in user to be enewe101 **
	logged_in_user = User.objects.get(pk=1)


	if request.POST:

		edit_proposal_form = EditProposalForm(
			data=request.POST,
			endpoint=reverse('add_proposal')
		)

		if edit_proposal_form.is_valid():
			proposal = edit_proposal_form.save()
			return redirect(proposal.get_url('proposal'))

	else:
		edit_proposal_form = EditProposalForm(
			endpoint=reverse('add_proposal'),
			initial={'user': logged_in_user}
		)

	return render(
		request,
		'digidemo/edit.html', 
		{
			'django_vars_js': get_django_vars_JSON(
				{'user': utils.obj_to_dict(
				logged_in_user, exclude=['password'])}),
			'proposal': None,
			'proposal_vote_form': None,
			'edit_proposal_form': edit_proposal_form,
			'logged_in_user': logged_in_user,
			'tabs': None,
			'active_navitem': 'create'
		}
	)


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
	print 's:', s
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
				print last_end, prev_match.end()
				substrings.append(s[last_end:prev_match.end()])
				last_end = prev_match.end()
				prev_match = match

			# But if there is no previous match, forcefully split at max_len
			else:
				print last_end, last_end+max_len
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
			'django_vars_js': get_django_vars_JSON(
				{'user': utils.obj_to_dict(
				logged_in_user, exclude=['password'])}),
			'proposal': proposal,
			'proposal_vote_form': proposal_vote_form,
			'logged_in_user': logged_in_user,
			'diff_table': diff_table,
			'active_navitem': 'issues',
			'tabs': get_proposal_tabs(proposal, 'edit')
		}
	)


def edit(request, proposal_id):

	# ** Hardcoded the logged in user to be enewe101 **
	logged_in_user = User.objects.get(pk=1)

	proposal = Proposal.objects.get(pk=proposal_id)

	# make a proposal vote form
	proposal_vote_form = get_vote_form(
		ProposalVote, ProposalVoteForm, logged_in_user, proposal)

	if request.POST:

		edit_proposal_form = EditProposalForm(
			data=request.POST,
			endpoint=proposal.get_url('edit')
		)

		if edit_proposal_form.is_valid():
			proposal = edit_proposal_form.save()
			return redirect(proposal.get_url('proposal'))

	else:
		edit_proposal_form = EditProposalForm(
			proposal=proposal,
			endpoint=proposal.get_url('edit')
		)

	return render(
		request,
		'digidemo/edit.html', 
		{
			'django_vars_js': get_django_vars_JSON(
				{'user': utils.obj_to_dict(
				logged_in_user, exclude=['password'])}),
			'proposal': proposal,
			'proposal_vote_form': proposal_vote_form,
			'edit_proposal_form': edit_proposal_form,
			'logged_in_user': logged_in_user,
			'tabs': get_proposal_tabs(proposal, 'edit'),
			'active_navitem': 'issues'
		}
	)


def discuss(request, proposal_id):

	proposal = Proposal.objects.get(pk=proposal_id)

	# ** Hardcoded the logged in user to be enewe101 **
	logged_in_user = User.objects.get(pk=1)

	# make a proposal vote form
	proposal_vote_form = get_vote_form(
		ProposalVote, ProposalVoteForm, logged_in_user, proposal)

	discussion_sections = []
	for discussion in proposal.discussion_set.all():

		# make a voting form for each discussion
		discussion_vote = utils.get_or_none(
			DiscussionVote, user=logged_in_user, target=discussion)

		if discussion_vote:
			discussion_vote_form = DiscussionVoteForm(
				instance=discussion_vote,
				cur_score=discussion.score)
		else:
			discussion_vote_form = DiscussionVoteForm(
				initial={'user':logged_in_user.pk, 'target':discussion.pk},
				cur_score=discussion.score
			)

		discussion_sections.append({
			'discussion': discussion,
			'discussion_vote_form': discussion_vote_form,
			'reply_form': ReplyForm(
				initial={'user':logged_in_user.pk, 'discussion':discussion.pk})
		})

	return render(
		request,
		'digidemo/discuss.html', 
		{
			'django_vars_js': get_django_vars_JSON(
				{'user': utils.obj_to_dict(
				logged_in_user, exclude=['password'])}),
			'proposal': proposal,
			'proposal_vote_form': proposal_vote_form,
			'logged_in_user': logged_in_user,
			'tabs': get_proposal_tabs(proposal, 'discuss'),
			'discussion_sections': discussion_sections,
			'active_navitem': 'issues'
		}
	)


def proposal_question_list(request, proposal_id):

	proposal = Proposal.objects.get(pk=proposal_id)

	# ** Hardcoded the logged in user to be enewe101 **
	logged_in_user = User.objects.get(pk=1)

	# make a proposal vote form
	proposal_vote_form = get_vote_form(
		ProposalVote, ProposalVoteForm, logged_in_user, proposal)

	questions = Question.objects.filter(target=proposal)

	return render(
		request,
		'digidemo/proposal_question_list.html',
		{
			'django_vars_js': get_django_vars_JSON(
				{'user': utils.obj_to_dict(
				logged_in_user, exclude=['password'])}),
			'proposal': proposal,
			'proposal_vote_form': proposal_vote_form,
			'logged_in_user': logged_in_user,
			'tabs': get_proposal_tabs(proposal, 'questions'),
			'questions': questions,
			'active_navitem': 'questions'
		}
	)


def ask_question(request, proposal_id):

	proposal = Proposal.objects.get(pk=proposal_id)

	# ** Hardcoded the logged in user to be enewe101 **
	logged_in_user = User.objects.get(pk=1)

	# make a proposal vote form
	proposal_vote_form = get_vote_form(
		ProposalVote, ProposalVoteForm, logged_in_user, proposal)


	if request.method == 'POST':
		form = QuestionForm(request.POST, endpoint=proposal.get_question_url())
		if form.is_valid():
			question = form.save()
			return redirect(question.get_url())
	
	else:
		form = QuestionForm(
			initial={'user':logged_in_user, 'target':proposal},
			endpoint=proposal.get_question_url()
		)

	return render(
		request,
		'digidemo/ask_question.html',
		{
			'django_vars_js': get_django_vars_JSON(
				{'user': utils.obj_to_dict(
				logged_in_user, exclude=['password'])}),
			'proposal': proposal,
			'proposal_vote_form': proposal_vote_form,
			'logged_in_user': logged_in_user,
			'tabs': get_proposal_tabs(proposal, 'questions'),
			'form': form,
			'active_navitem': 'questions'
		}
	)


def get_vote_form(VoteModel, VoteForm, user, target):
	existing_vote = utils.get_or_none(VoteModel, user=user, target=target)

	if existing_vote:
		vote_form = VoteForm(instance=existing_vote, cur_score=target.score)
	else:
		vote_form = VoteForm(
			initial={'user':user.pk, 'target':target.pk},
			cur_score=target.score
		)

	return vote_form


def view_question(request, question_id):
	question = Question.objects.get(pk=question_id)
	proposal = question.target


	# ** Hardcoded the logged in user to be enewe101 **
	logged_in_user = User.objects.get(pk=1)

	# make a question vote form 
	question_vote = get_vote_form(
		QuestionVote, QuestionVoteForm, logged_in_user, question)

	# make a comment form for the question
	question_comment_form = QuestionCommentForm(
		initial={'user':logged_in_user, 'target': question},
		id_prefix='qc'
	)

	# make a proposal vote form
	proposal_vote_form = get_vote_form(
		ProposalVote, ProposalVoteForm, logged_in_user, proposal)

	answers = []
	for answer_num, answer in enumerate(Answer.objects.all()):
		vote_form = get_vote_form(
			AnswerVote, AnswerVoteForm, logged_in_user, answer)
		comment_form = AnswerCommentForm(
			initial={'user':logged_in_user, 'target': answer},
			id_prefix=answer_num
		)
		answers.append({
			'content':answer,
			'vote_form':vote_form,
			'comment_form': comment_form
		})

	answer_form = AnswerForm(
		initial={'user':logged_in_user, 'target':question})

	return render(
		request,
		'digidemo/view_question.html',
		{
			'django_vars_js': get_django_vars_JSON(
				{'user': utils.obj_to_dict(
				logged_in_user, exclude=['password'])}),
			'question': {
				'content':question,
				'vote_form': question_vote,
				'comment_form': question_comment_form
			},
			'answers': answers,
			'answer_form': answer_form,
			'proposal': proposal,
			'proposal_vote_form': proposal_vote_form,
			'logged_in_user': logged_in_user,
			'tabs': get_proposal_tabs(proposal, 'questions'),
			'active_navitem': 'questions'
		}
	)


def make_proposal_context(proposal):

	proposal_version = proposal.get_latest()
	pos_factors = (
		FactorVersion.objects
		.filter(proposal_version=proposal_version,
			valence__gt=0,
			deleted=False)
		.order_by('pk')
	)
	neg_factors = (
		FactorVersion.objects
		.filter(proposal_version=proposal_version,
			valence__lt=0,
			deleted=False)
		.order_by('pk')
	)

	# ** Hardcoded the logged in user to be enewe101 **
	logged_in_user = User.objects.get(pk=1)

	proposal_vote_form = get_vote_form(
		ProposalVote, ProposalVoteForm, logged_in_user, proposal)

	# Get all of the letters which are associated with this proposal
	# and which are 'original letters'
	letter_sections = []
	letters = Letter.objects.filter(parent_letter=None, proposal=proposal)
	for letter_num, letter in enumerate(letters):

		# TODO: use the convenience method to make a voting widget
		# make a voting form for each letter
		letter_vote = utils.get_or_none(
			LetterVote, user=logged_in_user, target=letter)

		if letter_vote:
			letter_vote_form = LetterVoteForm(
				instance=letter_vote,
				cur_score=letter.score)
		else:
			letter_vote_form = LetterVoteForm(
				initial={'user':logged_in_user.pk, 'target':letter.pk},
				cur_score=letter.score
			)

		# make a re-sending form for each letter
		resend_form = ResendLetterForm(
			initial={
				'parent_letter': letter,
				'proposal': proposal,
				'body': letter.body,
				'recipients': letter.body,
				'user': logged_in_user,
				'valence': letter.valence
			}, 
		   	endpoint='resend_letter',
		)

		# compile the list of resenders -- don't include the original sender
		resenders = set([l.user 
			for l in Letter.objects.filter(parent_letter=letter)])

		letter_sections.append({
			'letter': letter,
			'comment_form': LetterCommentForm(
				initial={'user':logged_in_user.pk, 'target':letter.pk},
				id_prefix = letter_num
				),
			'vote_form': letter_vote_form,
			'resenders': resenders,
			'resend_form': resend_form
		}) 
	

	add_letter_form = LetterForm(initial={
		'proposal': proposal,
		'user': logged_in_user,
	})

	context = {
			'django_vars_js': get_django_vars_JSON(
				{'user': utils.obj_to_dict(
				logged_in_user, exclude=['password'])}),
			'proposal': proposal,
			'pos_factors': pos_factors,
			'neg_factors': neg_factors,
			'letter_form': add_letter_form,
			'letter_sections': letter_sections,
			'logged_in_user': logged_in_user,
			'proposal_vote_form': proposal_vote_form,
			'tabs': get_proposal_tabs(proposal, 'overview'),
			'active_navitem': 'issues'
		}

	return context


def test(request):
	return render(request, 'digidemo/test.html', {})


def login(request, provider_name):

	authomatic = Authomatic(CONFIG, 'a super secret random string')
	response = HttpResponse();
	result = authomatic.login(DjangoAdapter(request, response), provider_name)

	if result:
		# If there is result, the login procedure is over and we can write to 
		# response.
		response.write('<a href="..">Home</a>')
		if not (result.user.name and result.user.id):
		   result.user.update()
			
		# Welcome the user.
		response.write(u'<h1>Hi {0}</h1>'.format(result.user.name))
		response.write(u'<h2>Your id is: {0}</h2>'.format(result.user.id))
		response.write(
			u'<h2>Your email is: {0}</h2>'.format(result.user.email))
		url = 'https://graph.facebook.com/{0}/picture?type=large'
		url = url.format(result.user.id)
		response.write(url)
		access_response = result.provider.access(url)
		response.write(access_response.data.keys())
		urllib.urlretrieve(url, "../"+result.user.name+".jpg")

		logged_in_user = User.objects.filter(fname=result.user.name)
		count = len(logged_in_user);
		if count == 0:
			logged_in_user = None;
			logged_in_user = User(
				email='test@test.com',
				email_validated=1,
				avatar_img=result.user.name+'.jpg',
				avatar_name=result.user.name,
				fname=result.user.name,
				lname='test',
				rep=10,
				zip_code='h2x1x3',
				country='india',
				province='kar',
				street='1'
			)
			logged_in_user.save();

		request.session['member_id'] = result.user.name;
		response.write(
			'Login with <a href="../proposals/keystone_xl">check</a>.<br />')

	return response;


def mainPage(request,sort_type='most_recent'):

        if(sort_type=='most_recent'):
                proposals = Proposal.objects.order_by('-creation_date')[:5]
        elif(sort_type=='top_score'):
                proposals = Proposal.objects.order_by('-score')[:5]

        popular_posts =  Proposal.objects.order_by('-score')[:6]

        featured_post = Proposal.objects.get(pk=1);
        
        users = UserProfile.objects.all();

        # Hard coded Featured news
        
	return render(
                request,
                'digidemo/proposal_index.html',
                {'proposals': proposals,
                 'users': users,
                 'popular_posts':popular_posts,
                 'featured_post':featured_post,}
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
		{ 'form' : registrationForm,}
	)


def search(request):
    """
    Search > Root
    """

    # we retrieve the query to display it in the template
    form =ProposalSearchForm(request.GET)

    # we call the search method from the NotesSearchForm. Haystack do the work!
    results = form.search()

    return render(request, 'search/search.html', {
      #  'search_query' : search_query,
        'notes' : results,
    })

