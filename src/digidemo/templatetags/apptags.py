import os
from datetime import date, timedelta
from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as __
from digidemo.models import *
from digidemo import markdown as md
from digidemo.shortcuts import get_profile

register = template.Library()

@register.filter(name='getAuthor')
def getAuthor(users, proposal):
    return users.get(id=proposal.user_id).user.first_name


@register.tag(name="localize_static")
def localize_image(parser, token):
	'''
		Supports a template tag that is similar to "static", but it 
		inserts the langage code in front of the file name so that
		to serve localized resources.  The path given should be the path to 
		the resource but where the language code is missing.

		e.g. {% localize_static "/path/to/resource.jpg" %}
		becomes /static-dir/path/to/en-ca_resource.jpg
		if the viewer's language code is en-ca
	'''

	try:
		tag_name, url = token.split_contents()

	except ValueError:
		raise template.TemplateSyntaxError(
			"%r tag requires an image url as its only argument" 
			% token.contents.split()[0]
	)


	return ImageUrlNode(url)


class ImageUrlNode(template.Node):
	'''
		Supports a template tag that is similar to "static", but it 
		inserts the langage code in front of the file name so that
		to serve localized resources.  The path given should be the path to 
		the resource but where the language code is missing.

		e.g. {% localize_static "/path/to/resource.jpg" %}
		becomes /static-dir/path/to/en-ca_resource.jpg
		if the viewer's language code is en-ca
	'''


	def __init__(self, url):
	    self.url = url
	
	def render(self, context):
		url = self.url
	
		# strip the quotes if the image url is enquoted
		double_quoted = url.startswith('"') and url.endswith('"')
		single_quoted = url.startswith("'") and url.endswith("'")
		if double_quoted or single_quoted:
			url = url[1:-1]
		
		# tag on the language code to the filename part of the resource
		language_code = context['request'].LANGUAGE_CODE
		base_name =  language_code + '_' + os.path.basename(url)
		dir_name = os.path.dirname(url)
		return static(os.path.join(dir_name,base_name))



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
			msg = __('You need to validate your email!')
			return mark_safe('title="%s"' % msg)

	else:
		msg = __('You need to login!')
		return mark_safe('title="%s"' % msg)



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
