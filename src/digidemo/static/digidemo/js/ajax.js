function ajax(endpoint, data, success, error) {
	$.ajax({
		"url": ajax_handler_url + endpoint + '/',
		"data": data,
		"method":'POST',
		"dataType": 'json',
		"success": success,
		"error": error
	});
}

function ajaxForm(endpoint, form, success, error) {

	form_as_array = form.serializeArray();
	as_dict = dict(form_as_array);
	ajax(endpoint, as_dict, success, error);

}

function dict(arr) {
	var dict = {}

	for(var i=0; i<arr.length; i++) {

		var name = arr[i]['name'];
		var val = arr[i]['value'];

		if(name in dict) {

			if($.isArray(dict[name])) {
				dict[name].push(val)

			} else {
				dict[name] = [dict[name], val];
			}

		} else {
			dict[name] = val;
		}
	}

	return dict;
}
