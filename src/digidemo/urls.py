from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
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
	# front page urls
	url(r'^mainPage/$',mainPage, name='mainPage'),
	url(r'^mainPage/sort=(?P<sort_type>\w+)/$',mainPage,name='mainPage'),

	#Search results
	url(r'^search/$',search,name='search'),

	#userProfiles
        #Seeing the user Profile - Basic information and followed Posts
        
        url(r'^userProfile/(?P<userName>\w+)/$', userProfile,name='userProfile'),
        url(r'^userProfile/(?P<userName>\w+)/edit$',userProfileEdit,name='userProfileEdit'),

	# Registration
	url(r'^userRegistration/$', userRegistration,name='userRegistration'),

	# test url
	url(r'^$', test, name='test'),

	# proposal-specific urls
	url(r'^add_proposal/$', add_proposal, name='add_proposal'),
	url(r'^overview/(?P<proposal_id>\w+)/.*$', overview, name='overview'),
	url(r'^proposal/(?P<proposal_id>\w+)/.*$', proposal, name='proposal'),
	url(r'^questions/(?P<proposal_id>\w+)/.*$', QuestionListView().view, 
		name='questions'),
	url(r'^ask-question/(?P<proposal_id>\w+)/.*$', ask_question, 
		name='ask_question'),
	#url(r'^view-question/(?P<question_id>\w+)/.*$', view_question, 
	#	name='view_question'),
	url(r'^editors_area/(?P<target_id>\w+)/.*$', DiscussionListView().view, 
		name='editors_area'),
	url(r'^petitions/(?P<proposal_id>\w+)/.*$', 
		PetitionListView().view, name='petitions'),
	url(r'^view-discussion/(?P<post_id>\w+)/.*$', 
		DiscussionAreaView().view, name='view_discussion'),
	url(r'^edit/(?P<proposal_id>\w+)/.*$', edit, name='edit'),
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
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

