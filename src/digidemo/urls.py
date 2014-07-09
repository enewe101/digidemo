from django.conf.urls import patterns, include, url

from django.contrib import admin
from views import *
from ajax import *

admin.autodiscover()

urlpatterns = patterns('',
	# front page urls
	url(r'^mainPage/$',mainPage),
	url(r'^mainPage/sort=(?P<sort_type>\w+)/$',mainPage,name='mainPage'),

        #Testing login
     #   url(r'^Login/$',Login),
                       
	# Registration
	url(r'^userRegistration/$', userRegistration),

	# test url
	url(r'^$', test, name='test'),

	# proposal-specific urls
	url(r'^overview/(?P<proposal_name>\w+)/$', overview, name='overview'),
	url(r'^proposal/(?P<proposal_name>\w+)/$', overview, name='proposal'),
	url(r'^discuss/(?P<proposal_name>\w+)/$', discuss, name='discuss'),
        url(r'^edit/(?P<proposal_name>\w+)/$', edit, name='edit'),

	# ajax urls
	url(r'^ajaxJson/(?P<view>\w+)/$', handle_ajax_json, 
		name='handle_ajax_json'),
	url(r'^ajaxJson/$', handle_ajax_json, name='ajax_json_test'),
        url(r'^ajaxLogin/$', handle_ajax_login,name = 'handle_ajax_login'),
        url(r'^ajaxLogout/$', handle_ajax_logout,name = 'handle_ajax_logout'),
)

