from django.conf.urls import patterns, include, url
from django.conf.urls.static import static as static_url
from django.conf import settings

from django.contrib import admin
from views import *
from ajax import *

admin.autodiscover()



#if settings.TESTING_MODE:
    # enable this handler only for testing, 
    # so that if DEBUG=False and we're not testing,
    # the default handler is used
#    handler500 = 'digidemo.views.show_server_error'


urlpatterns = patterns('',

	# test url
	url(r'^test/$', show_test_page, name='test'),

	# front page urls
	url(r'^$', land, name='land'),
	url(r'^mainPage/$',mainPage, name='mainPage'),

	# login page
	url(r'^login_required/', Login().view, name='login_required'),
	url(r'^login_required/(?P<next_url>.+)', Login().view, name='login_required'),
	url(r'^do_reload/', do_reload, name='do_reload'),

	# main tabs
	url(r'^petition_list', AllPetitionListView().view, name="petition_list"),
	url(r'^issue_list/(?P<order_by>\w*)', IssueListView().view, 
		name="issue_list"),
	url(r'^topics/$', TagListView().view, name="topics"),
	url(r'^all_questions_list/(?P<order_by>\w*)', AllQuestionsListView().view, 
		name="all_questions_list"),
	url(r'^all_petitions_list/(?P<order_by>\w*)', AllPetitionsListView().view, 
		name="all_petitions_list"),

	#Search results
	url(r'^search/$',search,name='search'),

	#AllUserDisplay
	url(r'^users/$',users,name='users'),
        
	#userProfiles
	#Seeing the user Profile - Basic information and followed Posts
	
	url(r'^userProfile/(?P<userName>\w+)/$', userProfile,name='userProfile'),
	url(r'^userProfile/(?P<userName>\w+)/edit$',userProfileEdit,name='userProfileEdit'),

	# Registration
	url(r'^userRegistration/$', userRegistration,name='userRegistration'),


	# proposal-centric urls
	url(r'^add_proposal/$', AddProposalView().view, name='add_proposal'),
	url(r'^overview/(?P<proposal_id>\w+)/.*$', IssueOverview().view,
		name='proposal'),
	url(r'^questions/(?P<proposal_id>\w+)/.*$', QuestionListView().view, 
		name='questions'),
	url(r'^ask-question/(?P<target_id>\w+)/.*$', AskQuestionView().view, 
		name='ask_question'),
	url(r'^editors-area/(?P<issue_id>[0-9]+)/(?P<open_status>\w+)/.*$', 
		DiscussionListView().view, name='editors_area'),
	url(r'^start-discussion/(?P<target_id>[0-9]+)/.*$', 
		StartDiscussionView().view, name='start_discussion'),
	url(r'^petitions/(?P<proposal_id>\w+)/.*$', 
		PetitionListView().view, name='petitions'),
	url(r'^start-petition/(?P<target_id>[0-9]+)/.*$', 
		StartPetitionView().view, name='start_petition'),
	url(r'^view-discussion/(?P<post_id>\w+)/.*$', 
		DiscussionAreaView().view, name='view_discussion'),
	url(r'^edit/(?P<issue_id>\w+)/.*$', EditProposalView().view, name='edit'),
	url(r'^history/(?P<proposal_id>\w+)/.*$', history, name='history'),
	url(r'^view-question/(?P<post_id>\w+)/.*$', QuestionAreaView().view, 
		name='view_question'),

	# petition-centric views
	url(r'^view-petition/(?P<petition_id>\w+)/.*$', PetitionView().view, 
		name='view_petition'),


	# ajax urls
	url(r'^ajaxJson/(?P<view>\w+)/$', handle_ajax_json, 
		name='handle_ajax_json'),
	url(r'^ajaxJson/$', handle_ajax_json, name='ajax_json_test'),
	url(r'^ajaxLogin/$', handle_ajax_login,name = 'handle_ajax_login'),
	url(r'^ajaxLogout/$', handle_ajax_logout,name = 'handle_ajax_logout'),

) + static_url(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

