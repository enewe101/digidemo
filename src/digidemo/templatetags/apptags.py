from django import template
from datetime import date, timedelta
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from digidemo.models import *
from digidemo import markdown as md

register = template.Library()


@register.filter(name='getAuthor')
def getAuthor(users, proposal):
    print users.get(id=proposal.author_id).user.first_name
    return users.get(id=proposal.author_id).avatar_name


@register.filter(name='getSummary')
def getSummary(proposal):
    returnText = proposal[0:200];
    returnText+= '......';
    return returnText


@register.filter(needs_autoescape=True)
def markdown(text, autoescape=None):
	if autoescape:
		esc = conditional_escape
	else:
		esc = lambda x: x
	
	html = md.markdown(esc(text))
	return mark_safe(html)
