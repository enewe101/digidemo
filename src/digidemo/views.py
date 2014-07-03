from django.core.urlresolvers import reverse
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from digidemo.models import *
from digidemo.forms import *
from digidemo import utils
from settings import DEBUG
import json

def get_django_vars(additional_vars={}):
	django_vars = {
		'DEBUG': DEBUG
	}

	django_vars.update(additional_vars)

	return django_vars


def get_django_vars_JSON(additional_vars):
	return json.dumps(get_django_vars(additional_vars))


def discuss(request, proposal_name):

	this_proposal = Proposal.objects.get(name=proposal_name)

	# ** Hardcoded the logged in user to be enewe101 **
	logged_in_user = User.objects.get(pk=1)
	
	# make the proposal vote form -- this gets rendered as a voting widget
	proposal_vote = utils.get_or_none(
		ProposalVote, user=logged_in_user, proposal=this_proposal)

	if proposal_vote:
		proposal_vote_form = ProposalVoteForm(
			instance=proposal_vote,
			cur_score=this_proposal.score)

	else:
		proposal_vote_form = ProposalVoteForm(
			initial={'user':logged_in_user.pk, 'proposal':this_proposal.pk},
			cur_score=this_proposal.score)

	
	media = ProposalVoteForm().media

	return render(
		request,
		'digidemo/discuss.html', 
		{
			'django_vars_js': get_django_vars_JSON(
				{'user': utils.obj_to_dict(
				logged_in_user, exclude=['password'])}),
			'proposal': this_proposal,
			'logged_in_user': logged_in_user,
			'proposal_vote_form': proposal_vote_form,
			'media': media,
			'tab': 'discuss',
		}
	)


def overview(request, proposal_name):

	this_proposal = Proposal.objects.get(name=proposal_name)

	# ** Hardcoded the logged in user to be enewe101 **
	logged_in_user = User.objects.get(pk=1)
	
	proposal_vote = utils.get_or_none(
		ProposalVote, user=logged_in_user, proposal=this_proposal)

	if proposal_vote:
		proposal_vote_form = ProposalVoteForm(
			instance=proposal_vote,
			cur_score=this_proposal.score)

	else:
		proposal_vote_form = ProposalVoteForm(
			initial={'user':logged_in_user.pk, 'proposal':this_proposal.pk},
			cur_score=this_proposal.score)

	# Get all of the letters which are associated with this proposal
	# and which are 'original letters'
	letter_sections = []
	letters = Letter.objects.filter(parent_letter=None, proposal=this_proposal)
	for letter_num, letter in enumerate(letters):

		# make a voting form for each letter
		letter_vote = utils.get_or_none(
			LetterVote, user=logged_in_user, letter=letter)

		if letter_vote:
			letter_vote_form = LetterVoteForm(
				instance=letter_vote,
				cur_score=letter.score)
		else:
			letter_vote_form = LetterVoteForm(
				initial={'user':logged_in_user.pk, 'letter':letter.pk},
				cur_score=letter.score
			)

		# make a re-sending form for each letter
		resend_form = ResendLetterForm(
			initial={
				'parent_letter': letter,
				'proposal': this_proposal,
				'body': letter.body,
				'recipients': letter.body,
				'sender': logged_in_user,
				'valence': letter.valence
			}, 
		   	endpoint='resend_letter',
		)

		# compile the list of resenders -- don't include the original sender
		resenders = letter.resenders.exclude(pk=letter.sender.pk)

		letter_sections.append({
			'letter': letter,
			'comment_form': LetterCommentForm(
				initial={'author':logged_in_user.pk, 'letter':letter.pk}),
			'vote_form': letter_vote_form,
			'resenders': resenders,
			'resend_form': resend_form
		}) 
	
	media = ProposalVoteForm().media
	media += LetterVoteForm().media

	add_letter_form = LetterForm(initial={
		'proposal': this_proposal,
		'sender': logged_in_user,
	})

	return render(
		request,
		'digidemo/overview.html', 
		{
			'django_vars_js': get_django_vars_JSON(
				{'user': utils.obj_to_dict(
				logged_in_user, exclude=['password'])}),
			'proposal': this_proposal,
			'letter_form': add_letter_form,
			'letter_sections': letter_sections,
			'logged_in_user': logged_in_user,
			'proposal_vote_form': proposal_vote_form,
			'media': media,
			'tab': 'overview',
		}
	)





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

        featured_post = Proposal.objects.get(name='Quebec');
        
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
                print "working till here"
                user = User(request.POST)
                print user
                print "now"
        return render(
                request,
                'digidemo/User_registration.html',
                )

