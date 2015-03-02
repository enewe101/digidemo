'''
	This module lists some words that should be translated.  They are included
	here because, within the app code, they only arise as variables, not 
	literals, which means that the `django-admin.py makemessages` command 
	can't actually see them.
'''

from django.utils.translation import ugettext as _

_('economy')
_('health')
_('education')
_('democracy')
_('environment')
_('culture')
_('readiness')
_('relations')
_('interesting')
_('activity')
_('newest')
