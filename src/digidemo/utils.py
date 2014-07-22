from django.core import serializers
import json

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


def extract_dict(obj, keys):
	'''
		Make a plain-dict copy of object, but only the values named in `keys`.
	'''
	return_dict = {}
	for key in keys:

		# try to get a value for key
		try:
			val = obj[key]
		except KeyError:
			raise KeyError(
				'extract_dict: object has no attribute `%s`.' % key)

		# add the value found for key
		return_dict[key] = val

	return return_dict


def obj_to_dict(model_instance, exclude=[]):

	# kludge to dict by serializing then json-parsing
	serial_array = serializers.serialize('json', [model_instance])

	# we want the fields, not the metadata junk
	serial_obj = json.loads(serial_array)[0]['fields']

	# add the primary key (it isn't included in obj['fields'])
	serial_obj['pk'] = model_instance.pk

	# remove excluded fields
	for field in exclude:
		if field in serial_obj:
			del serial_obj[field]


	return serial_obj


