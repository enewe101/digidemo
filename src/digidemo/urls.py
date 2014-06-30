from django.conf.urls import patterns, include, url

from django.contrib import admin
from views import test, overview, proposal, discuss, send_letter,mainPage,login
from ajax import handle_ajax_json, handle_ajax_html

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^mainPage/$',mainPage),
	url(r'^mainPage/sort=(?P<sort_type>\w+)/$',mainPage,name='mainPage'),
	url(r'^$', test, name='test'),
	url(r'^overview/(?P<proposal_name>\w+)/$', overview, name='overview'),
	url(r'^proposal/(?P<proposal_name>\w+)/$', proposal, name='proposal'),
	url(r'^discuss/(?P<proposal_name>\w+)/$', discuss, name='discuss'),
	url(r'^send_letter/$', send_letter, name='send_letter'),
	url(r'^ajaxJson/(?P<view>\w+)/$', handle_ajax_json, 
		name='handle_ajax_json'),
	url(r'^ajaxHtml/(?P<view>\w+)/$', handle_ajax_html, 
		name='handle_ajax_html'),
	url(r'^ajaxJson/$', handle_ajax_json, name='ajax_json_test'),
	url(r'^ajaxHtml/$', handle_ajax_html, name='ajax_html_test'),
)

