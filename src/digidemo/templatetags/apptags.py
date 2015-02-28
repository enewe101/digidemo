from django import template
from datetime import date, timedelta
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from digidemo.models import *
from digidemo import markdown as md
from digidemo.shortcuts import get_profile

register = template.Library()


@register.filter(name='getAuthor')
def getAuthor(users, proposal):
    return users.get(id=proposal.user_id).user.first_name


@register.filter(name='getSummary')
def getSummary(proposal):
    returnText = proposal[0:200];
    returnText+= '......';
    return returnText


@register.filter(name='getTags')
def getTags(proposal):
    if(proposal is None):
        return "";
    returnString = "";
    
    for tag in proposal.tags.all():
        print tag.name;
        returnString = returnString + tag.name
        returnString = str(returnString) + ", "
    if(len(returnString)>0):
        returnString = returnString[:-1]
    return returnString

@register.filter(name='user_authenticated')
def user_authenticated(request):
	if request.user.is_authenticated():
		return True

@register.filter(name='email_validated')
def user_authenticated(request):
	if get_profile(request.user).email_validated:
		return True


@register.filter(name='login_tip')
def login_tip(request):
	if request.user.is_authenticated():
		if get_profile(request.user).email_validated:
			return ''
		else:
			return mark_safe('title="You need to validate your email!"')

	else:
		return mark_safe('title="You need to login!"')



@register.filter(name='getLoggedInUser')
def getLoggedInUser(request):
    
    if(request.user.is_authenticated()):
        return(request.user)
    return "false"


@register.filter(name='getFollowPostStatus')
def getFollowPostStatus(request,proposalID):
    #print request.session.keys()
    if(request.session.has_key("user")):
            proposal = Proposal.objects.get(pk=proposalID);
            userName = request.session['user'];
            userLoggedIn = User.objects.get(username = userName);
            userProfile = UserProfile.objects.get(user = userLoggedIn);
            if proposal in userProfile.followedProposals.all() :
                return "following";
            else :
                return "unfollowing";
    else:
        return "unlogged"

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
