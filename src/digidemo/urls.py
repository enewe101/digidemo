from django.conf.urls import patterns, include, url

from django.contrib import admin
from views import test, overview, discuss, mainPage, login, userRegistration
from ajax import handle_ajax_json, handle_ajax_html

admin.autodiscover()

urlpatterns = patterns('',
	# front page urls
	url(r'^mainPage/$',mainPage),
	url(r'^mainPage/sort=(?P<sort_type>\w+)/$',mainPage,name='mainPage'),

	# test url
	url(r'^$', test, name='test'),

	# proposal-specific urls
	url(r'^overview/(?P<proposal_name>\w+)/$', overview, name='overview'),
	url(r'^proposal/(?P<proposal_name>\w+)/$', overview, name='proposal'),
	url(r'^discuss/(?P<proposal_name>\w+)/$', discuss, name='discuss'),

	# ajax urls
	url(r'^ajaxJson/(?P<view>\w+)/$', handle_ajax_json, 
		name='handle_ajax_json'),
	url(r'^ajaxHtml/(?P<view>\w+)/$', handle_ajax_html, 
		name='handle_ajax_html'),
	url(r'^ajaxJson/$', handle_ajax_json, name='ajax_json_test'),
	url(r'^ajaxHtml/$', handle_ajax_html, name='ajax_html_test'),
        url(r'^userRegistration/$', userRegistration),
)

