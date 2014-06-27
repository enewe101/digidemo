function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

// sends the plain js object `data` to the django ajax function `endpoint`
// and optionally fires `success` or `error` with the plain text content.
function ajaxHtml(endpoint, data, handlers) {
	$.ajax({
		"url": handle_ajax_html_url + endpoint + '/',
		"data": data,
		"method":'POST',
		"dataType": 'text',
		"success": handlers['success'],
		"error": handlers['error']
	});
}


// sends the plain js object `data` to the django ajax function `endpoint`
// and optionally fires `success` or `error` with the parsed JSON response.
function ajax(endpoint, data, handlers) {

	$.ajax({
		"url": handle_ajax_json_url + endpoint + '/',
		"data": data,
		"method":'POST',
		"dataType": 'json',
		"success": handlers['success'],
		"error": handlers['error']
	});
}


// Serializes the form as name-value pairs in a JSON object, sends this to the 
// django ajax function `endpoint` and optionally fires `success` or `error` 
// with the parsed JSON response.
function ajaxForm(endpoint, form, handlers) {
	form_as_array = form.serializeArray();
	alert(form_as_array.toSource());
	as_dict = dict(form_as_array);
	ajax(endpoint, as_dict, handlers);

}


// Helper to turn an array of objects [{'name':<name>, 'value':<val>},...]
// into a flat object {<name>:<val>, ...}
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


registered_forms = {};
function register_form(form_id, endpoint, form_class, submit_id, handlers) {
	registered_forms[form_id] = {
		'form_id':form_id,
		'endpoint': endpoint,
		'form_class':form_class,
		'submit_id': submit_id, 
   		'handlers': handlers
	};
}	

function arm_form_id(form_id) {
	arm_form(registered_forms[form_id]);
}

function arm_form(registered_form) {
	var rf = registered_form;

	// bind the form's submit button to submit the form using ajaxForm to
	// its endpoint, and call its handlers
	$('#' + rf['submit_id']).click(function() {
		ajaxForm(
			rf['endpoint'],
			$('#' + rf['form_id']),
			(rf['handlers'] || {})
		)
	});
}

function arm_ajax_forms() {
	for(var form_id in registered_forms) {
		arm_form_id(form_id);
	}
}

