from django import template
from datetime import date, timedelta
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from digidemo.models import *
from digidemo import markdown as md

register = template.Library()


@register.filter(name='getAuthor')
def getAuthor(users, proposal):
    return users.get(id=proposal.user_id).user.first_name


@register.filter(name='getSummary')
def getSummary(proposal):
    returnText = proposal[0:200];
    returnText+= '......';
    return returnText


@register.filter(name='getLoggedInUser')
def getLoggedInUser(request):
    print request.session.keys()
    if(request.session.has_key("user")):
        return(request.session['user'])
    return "false"


@register.filter(needs_autoescape=True)
def markdown(text, autoescape=None):
	if autoescape:
		esc = conditional_escape
	else:
		esc = lambda x: x
	
	html = md.markdown(esc(text))
	return mark_safe(html)


@register.filter()
def markdown_noescape(text):
	return md.markdown(text)
