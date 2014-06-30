from django import template
from datetime import date, timedelta
from digidemo.models import *

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
