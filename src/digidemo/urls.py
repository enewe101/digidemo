from django.conf.urls import patterns, include, url

from django.contrib import admin
from views import test, proposal, send_letter
from ajax import handle_ajax

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', test, name='test'),
	url(r'^proposals/(?P<proposal_name>\w+)/$', proposal, name='proposal'),
	url(r'^send_letter/$', send_letter, name='send_letter'),
	url(r'^ajax/(?P<view>\w+)/$', handle_ajax, name='handle_ajax'),
	url(r'^ajax/$', handle_ajax, name='ajax'),
)

