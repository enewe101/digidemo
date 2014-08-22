from django.conf.urls import patterns, include, url
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
        url(r'^userProfile/(?P<userName>\w+)/$', userProfile,name='userProfile'),
        
	#Testing login
	#   url(r'^Login/$',Login),
                       
	# Registration
	url(r'^userRegistration/$', userRegistration,name='userRegistration'),

	# test url
	url(r'^$', test, name='test'),

	# proposal-specific urls
	url(r'^add_proposal/$', add_proposal, name='add_proposal'),
	url(r'^overview/(?P<proposal_id>\w+)/.*$', overview, name='overview'),
	url(r'^proposal/(?P<proposal_id>\w+)/.*$', proposal, name='proposal'),
	url(r'^questions/(?P<proposal_id>\w+)/.*$', proposal_question_list, 
		name='proposal_question_list'),
	url(r'^ask-question/(?P<proposal_id>\w+)/.*$', ask_question, 
		name='ask_question'),
	url(r'^view-question/(?P<question_id>\w+)/.*$', view_question, 
		name='view_question'),
	url(r'^discuss/(?P<proposal_id>\w+)/.*$', discuss, name='discussion'),
	url(r'^edit/(?P<proposal_id>\w+)/.*$', edit, name='edit'),
	url(r'^history/(?P<proposal_id>\w+)/.*$', history, name='history'),

	# ajax urls
	url(r'^ajaxJson/(?P<view>\w+)/$', handle_ajax_json, 
		name='handle_ajax_json'),
	url(r'^ajaxJson/$', handle_ajax_json, name='ajax_json_test'),
        url(r'^ajaxLogin/$', handle_ajax_login,name = 'handle_ajax_login'),
        url(r'^ajaxLogout/$', handle_ajax_logout,name = 'handle_ajax_logout'),
)

