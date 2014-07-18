from django.core.urlresolvers import reverse
from django.core import serializers
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from digidemo.models import *
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


def update_proposal(request, proposal_id):
	proposal_version_form = ProposalVersionForm(request.POST)
	if proposal_version_form.is_valid():
		proposal_version_form.save()

	return proposal(request, proposal_id)


def proposal(request, proposal_id):
	proposal = Proposal.objects.get(pk=proposal_id)
	context = make_proposal_context(proposal)
	context['tabs'] = get_proposal_tabs(proposal, 'proposal')

	return render(
		request,
		'digidemo/proposal.html',
		context
	)


def edit(request, proposal_id):

	proposal = Proposal.objects.get(pk=proposal_id)

	# ** Hardcoded the logged in user to be enewe101 **
	logged_in_user = User.objects.get(pk=1)

	if request.POST:

		edit_proposal_form = EditProposalForm.from_data(request.POST)

		if edit_proposal_form.is_valid():
			edit_proposal_form.save()
			return redirect(proposal.get_url('proposal'))

	else:
		edit_proposal_form = EditProposalForm(proposal)

	return render(
		request,
		'digidemo/edit.html', 
		{
			'django_vars_js': get_django_vars_JSON(
				{'user': utils.obj_to_dict(
				logged_in_user, exclude=['password'])}),
			'proposal': proposal,
			'edit_proposal_form': edit_proposal_form,
			'logged_in_user': logged_in_user,
			'tabs': get_proposal_tabs(proposal, 'edit')
		}
	)


def discuss(request, proposal_id):

	proposal = Proposal.objects.get(pk=proposal_id)

	# ** Hardcoded the logged in user to be enewe101 **
	logged_in_user = User.objects.get(pk=1)
	
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
			'logged_in_user': logged_in_user,
			'tabs': get_proposal_tabs(proposal, 'discuss'),
			'discussion_sections': discussion_sections
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
	
	proposal_vote = utils.get_or_none(
		ProposalVote, user=logged_in_user, target=proposal)

	if proposal_vote:
		proposal_vote_form = ProposalVoteForm(
			instance=proposal_vote,
			cur_score=proposal.score)

	else:
		proposal_vote_form = ProposalVoteForm(
			initial={'user':logged_in_user.pk, 'target':proposal.pk},
			cur_score=proposal.score)

	# Get all of the letters which are associated with this proposal
	# and which are 'original letters'
	letter_sections = []
	letters = Letter.objects.filter(parent_letter=None, proposal=proposal)
	for letter_num, letter in enumerate(letters):

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
				initial={'user':logged_in_user.pk, 'letter':letter.pk}),
			'vote_form': letter_vote_form,
			'resenders': resenders,
			'resend_form': resend_form
		}) 
	
	media = ProposalVoteForm().media
	media += LetterVoteForm().media

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
			'media': media,
			'tabs': get_proposal_tabs(proposal, 'overview')
		}

	return context






def test(request):
	return render(request, 'digidemo/test.html', {})


def login(request, provider_name):
    authomatic = Authomatic(CONFIG, 'a super secret random string')
    response = HttpResponse();
    result = authomatic.login(DjangoAdapter(request, response), provider_name)
    if result:
        # If there is result, the login procedure is over and we can write to response.
        response.write('<a href="..">Home</a>')
        if not (result.user.name and result.user.id):
           result.user.update()
            
           # Welcome the user.
        response.write(u'<h1>Hi {0}</h1>'.format(result.user.name))
        response.write(u'<h2>Your id is: {0}</h2>'.format(result.user.id))
        response.write(u'<h2>Your email is: {0}</h2>'.format(result.user.email))
        url = 'https://graph.facebook.com/{0}/picture?type=large'
        url = url.format(result.user.id)
        response.write(url)
        access_response = result.provider.access(url)
      #  response.write(access_response.data.keys())
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
        response.write('Login with <a href="../proposals/keystone_xl">check</a>.<br />')
    return response;


def mainPage(request,sort_type='most_recent'):

        if(sort_type=='most_recent'):
                proposals = Proposal.objects.order_by('-creation_date')[:5]
        elif(sort_type=='top_score'):
                proposals = Proposal.objects.order_by('-score')[:5]

        popular_posts =  Proposal.objects.order_by('-score')[:6]

        featured_post = Proposal.objects.get(title='Quebec');
        
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
                        print "absbsbbadsaasdasd"
                        passwordPass = user.cleaned_data['password']
                        userNamePass = user.cleaned_data['userName']
                        emailPass = user.cleaned_data['email']
                        firstNamePass = user.cleaned_data['firstName']
                        lastNamePass = user.cleaned_data['lastName']
                        userCreate = User.objects.create_user(username=userNamePass,
                                                        email= emailPass,
                                                        password = passwordPass,
                                                        first_name = firstNamePass,
                                                        last_name = lastNamePass)
                        print "absbsbbadsaasdasd"
                        userCreate.save();
                        streetPass = user.cleaned_data['street']
                        zipCodePass = user.cleaned_data['zipCode']
                        countryPass =  user.cleaned_data['country']
                        provincePass =  user.cleaned_data['province']
                        userProfile = UserProfile (user=userCreate,
                                                   email_validated = 0,
                                                   rep=0,
                                                   street = streetPass,
                                                   country = countryPass,
                                                   zip_code = zipCodePass,
                                                   province = provincePass)
                        userProfile.save();
                return redirect('../mainPage')

        registrationForm = NameForm();
               
        return render(
                request,
                'digidemo/User_registration.html',
                { 'form' : registrationForm,}
                )


