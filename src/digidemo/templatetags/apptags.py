from django import template
from datetime import date, timedelta
from digidemo.models import *

register = template.Library()


@register.filter(name='getAuthor')
def getAuthor(users, proposal):
    return users.get(id=proposal.author_id).fname

@register.filter(name='getSummary')
def getSummary(proposal):
    returnText = proposal[0:200];
    returnText+= '......';
    return returnText
