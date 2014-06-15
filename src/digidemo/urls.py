from django.conf.urls import patterns, include, url

from django.contrib import admin
import views 

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$',views.test, name='test'),
	url(r'^proposals/(?P<proposal_name>\w+)/$', views.proposal, name='proposal'),
)

