
def get_or_none(model, **kwargs):
	'''
	Use to get the matching object, or None if it doesn't exist.  This 
	should be used when a unique match is expected.

	If there's multiple objects returned, model.MultipleObjectsReturned would 
	be raised.
	'''

	try:
		return model.objects.get(**kwargs)

	except (model.DoesNotExist, model.MultipleObjectsReturned), e:
		return None

