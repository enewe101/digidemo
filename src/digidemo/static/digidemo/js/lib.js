

///////////////////////////////	
//  						 //
//  csrf-protection for ajax //
//  						 //
///////////////////////////////	

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



///////////////////////////////	
//  						 //
//  ajax convinience methods //
//  						 //
///////////////////////////////	

if(typeof ALERT_AJAX_ERRORS == 'undefined') {
	ALERT_AJAX_ERRORS = false;
}


// sends the plain js object `data` to the django ajax function `endpoint`
// and optionally fires `success` or `error` with the parsed JSON response.
function ajax(endpoint, data, handlers) {

	handlers = handlers || {};

	var error = handlers['error'] || alert_ajax_error;

	$.ajax({
		"url": handle_ajax_url + endpoint + '/',
		"data": data,
		"method":'POST',
		"dataType": 'json',
		"success": handlers['success'],
		"error": error
	});
}


// Serializes the form as name-value pairs in a JSON object, sends this to the 
// django ajax function `endpoint` and optionally fires `success` or `error` 
// with the parsed JSON response.
function ajaxForm(endpoint, form, handlers) {

	form_as_array = form.serializeArray();
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





//////////////////////
//  				//
//  widget manager  //
//  				//
//////////////////////

var widgets = {}

function register_widget(widget_id, widget, widget_class) {
	widgets[widget_id] = {
		'widget_id': widget_id,
		'widget_class': widget_class || '',
		'widget': widget	
	}
}

function register_form(form_id, endpoint, form_class, submit_id) {

	var form_widget = new FormWidget(
		$('#'+form_id), endpoint, $('#' + submit_id));

	register_widget(form_id, form_widget, form_class);

}






//////////////////////////
//  					//
//  generic FormWidget  //
//  					//
//////////////////////////


function FormWidget(form, endpoint, submit_button) {

	var events = ['before', 'success', 'error', 'after'];
	var hooks = make_page_hooks(this, events) 
	hooks.error = alert_ajax_error;

	submit_button.click( $.proxy(
		function() {
			ajaxForm(
				endpoint,
				form,
				{
					'before': $.proxy(function(data) {
						hooks['before']();
					}, this),

					'success': $.proxy(function(data, textStatus, jqXHR) {
						if(data.success) {
							hooks['success'](data, textStatus, jqXHR);
							render_errors(data);
						} else {
							hooks['error'](data, textStatus);
							render_errors(data);
						}

					}, this),

					'error': $.proxy(function(data, textStatus, jqXHR) {
						hooks['error'](data, textStatus, jqXHR);
						render_errors(data);
					}, this),

					'after': $.proxy(function(data, textStatus, jqXHR) {
						hooks['after']();
					}, this)
				}
			);
		}, this)
	);
}


function render_errors(data) {
	// Since errors were returned, iterate over the fields, and mark
	// those with errors using styling and errorr text
	for(field_id in data.errors) {

		// the special field "__all__" represents errors with the form
		// in general.  There is a special div for this
		if(field_id == '__all__') {
			all_errs = $('#{{form.form_class}}_{{include_id}}_errors')
			all_errs.text(data.errors[field_id].join('<br />'));
		}

		// All other errors are field-specific.  get the field
		field = $('#'+field_id)

		// Deal with all the errors
		if(data.errors[field_id].length) {

			// Check if the field is hidden.  If so, then it's our
			// fault
			if(field.attr('type') == 'hidden') {
				alert("Oops... there has been a javascript error and "
					+ "we don't have the codes to deal with it.  It "
					+ "might go away if you refresh your browser.");
				continue;

			// otherwise its bad form data (user's fault). Mark errors.
			} else {
				$('#'+field_id).addClass('error')
				$('#'+field_id+'_errors').text(
					data.errors[field_id].join('<br />'))
			}

		// make sure that any OK fields get their errors cleared
		} else {

			// (but for hidden fields, there's nothing to do)
			if(field.attr('type') == 'hidden') {
				continue;
			}

			console.log(field_id);
			$('#'+field_id+'_errors').text('');
			$('#'+field_id).removeClass('error');
		}
	}
}


//////////////////////////////////////////////	
//  						 				//
//  add color to visualize html structure   //
//  	(helps debug css and layout)		//
//  						 				//
//////////////////////////////////////////////

$(document).ready(function() {

	if(STRUCT) {
		// The standard colors
		colors = [
			'aqua', 'black', 'blue', 'fuchsia', 'gray', 'green', 'lime', 
			'maroon', 'navy', 'olive', 'orange', 'purple', 'red', 'silver', 'teal',
			'white', 'yellow'
		];

		// get all the elements
		$('*').each(function(i) {
			if($(this).css) {
				$(this).css('background-color', colors[i%colors.length]);
			}
		})
	}
});







//////////////////////////
//  					//
//    VoteForm widget   //
//  					//
//////////////////////////

function VoteForm(form_id, form_class, start_state, score, endpoint) {

	// do some validation
	if(!(typeof form_id == 'string')) {
		js_error('In VoteForm(form_id, form_class, start_state), id must be '
			+ 'an html-safe string');
	}

	start_state = parseInt(start_state);

	if($.inArray(start_state, [-1, 0, 1]) == -1) {
		js_error(
			"In vote_form, start_state must be -1, 0, or 1; found: "
			+ start_state);
	}
	
	// register the html form
	this.form = $('#' + form_id);
	this.valence = $('#' + form_id + ' input[name=valence]'); 
	
	// build the html elements for this widget
	this.html = {};
	this.html.upvote = $('<div id="'+form_id+'_upvote" class="upvote" />');
	this.html.score = $('<div id="'+form_id+'_score" class="score" />');
	this.html.downvote = $(
		'<div id="'+form_id+'_downvote" class="downvote" />');

	this.html.wrapper = $('<div id="'+form_id+'_wrapper" class="vote_form" />')
		.append([this.html.upvote, this.html.score, this.html.downvote]);


	// arm the upvote button.  Proxy makes the event handler use this context.
	this.html.upvote.click( $.proxy(
		function() {

			if(this.state == -1) {
				this.enter_state_1();

			} else if(this.state == 0) {
				this.enter_state_1();

			} else if(this.state == 1) {
				this.enter_state_0();

			} else {
				js_error('VoteForm: unexpected state: ' + this.state);
			}

			this.send_vote();
		}, this)
	);


	// arm the downvote button.  Proxy makes event handler use this context.
	this.html.downvote.click( $.proxy(
		function() {

			if (this.state == -1) {
				this.enter_state_0();

			} else if (this.state == 0) {
				this.enter_state_neg1();

			} else if (this.state == 1) {
				this.enter_state_neg1();

			} else {
				js_error('VoteForm: unexpected state: ' + this.state);
			}

			this.send_vote();
		}, this)
	);


	// state-changing functions
	this.enter_state_neg1 = function() {
		this.html.upvote.attr('class', 'upvote_off');
		this.html.downvote.attr('class', 'downvote_on');
		this.html.score.text(this.score - 1);
		this.state = -1;
	}

	this.enter_state_0 = function() {
		this.html.upvote.attr('class', 'upvote_off');
		this.html.downvote.attr('class', 'downvote_off');
		this.html.score.text(this.score);
		this.state = 0;
	}

	this.enter_state_1 = function() {
		this.html.upvote.attr('class', 'upvote_on');
		this.html.downvote.attr('class', 'downvote_off');
		this.html.score.text(this.score + 1);
		this.state = 1;
	}

	
	// this provides placeholders for callbacks that the page in which
	// this widget will be placed, can use
	var events = ['before', 'success', 'error', 'after'];
	var hooks = make_page_hooks(this, events);
	hooks.error = alert_ajax_error;

	// posts the vote using ajax
	this.send_vote = function() {

		this.valence.val(this.state);

		ajaxForm(
			endpoint,
		   	this.form,
			{
				'before': $.proxy(
					function(data, textStatus, jqXHR) {
						hooks.before(data, textStatus, jqXHR);
					}, 
					this
				),

				'success': $.proxy(
					function(data, textStatus, jqXHR) {
						if(data.success) {
							hooks.success(data, textStatus, jqXHR);
						} else {
							alert(data.toSource());
							hooks.error(data, textStatus, jqXHR);
						}
					}, 
					this
				),

				'error': $.proxy(
					function(data, textStatus, jqXHR) {
						hooks.error(data, textStatus, jqXHR);
					}, 
					this
				),

				'after': $.proxy(
					function(data, textStatus, jqXHR) {
						hooks.error(data, textStatus, jqXHR);
					}, 
					this
				)
			}
		);
	}


	// gets the html element for this widget
	this.get = function() {
		return this.html.wrapper;
	}


	// initilize the vote form into the state passed to the constructor
	if(start_state == -1) {
		this.score = score + 1;
		this.enter_state_neg1();

	} else if(start_state == 0) {
		this.score = score;
		this.enter_state_0();

	} else if(start_state == 1) {
		this.score = score - 1;
		this.enter_state_1();

	} else {
		js_error('VoteForm: unexpected start_state: ' + this.start_state);
	}

}


//////////////////////////////
//  						//
//   ResenderList widget	//
//  						//
//////////////////////////////

function ResenderList(wrapper, init_users) {

	wrapper = wrapper;
	var users = init_users;

	// public function.  Get the user avatar for user with given pk and then
	// put it in the wrapper div
	this.add_user = function(user_pk) {
		
		// if the user is already in the list, do nothing
		if($.inArray(user_pk, users) >= 0) {
			return;
		}

		// otherwise, we add the user, and append her avatar image
		users.push(user_pk);
		get_user_avatar_html(user_pk);

	}

	var get_user_avatar_html = function(user_pk) {
		ajax(
			'get_resender_avatar',
		   	{'user_pk':user_pk}, 
			{
				'success': $.proxy(function(data){
					if(data.success) {
						wrapper.prepend(data.html);
					} else {
						js_error(
							'get_user_avatar_html: json requesnt not accepted')
					}
				}, this)
			}
		);
	};


}



//////////////////
//  			//
//   js utils	//
//  			//
//////////////////

function js_error(err_msg) {
	if(django.DEBUG){
		alert(err_msg);
	}
}


function noop() {
}

function add_noops(handlers, events) {
	handlers = handlers || {};
	for(var i=0; i<events.length; i++) {
		var e = events[i];
		handlers[e] = handlers[e] || noop;
	}
	return handlers;
}

function alert_ajax_error(response, textStatus) { 

	// for responses with http error code
	if(response.status) {
		js_error(response.status + ': ' + response.responseText);

	// for http success but with application error code
	} else {
		js_error(response.msg);
	}
};

function conditional_ajax_error(handlers) {
	handlers = handlers || {}
	var error = handlers['error'];
	if(!error && ALERT_AJAX_ERRORS) {
		handlers['error'] = alert_ajax_error;
	}
	return handlers;
}


function make_page_hooks(obj, events) {

	// collect an array of valid hooks and initialize them to noop
	var valid_hooks = []
	var hooks = {}

	for(var i=0; i<events.length; i++) {
		valid_hooks.push(events[i]);
		hooks[events[i]] = noop;
	}

	// make a public hook assignment function
	var that = obj;
	that.hook = $.proxy( 
		function(hookname, f) {
			// do some validation
			// ensure hookname is valid
			if(!(hookname in hooks)) {
				js_error('hook error: ' + hookname 
					+ ' is not a valid hookname');
				return
			}

			// ensure hook is a function
			if(typeof f != 'function') {
				js_error('hook error: hook must be a function.  Got: ' 
					+ f);
			}

			// everything ok, assign the hook
			hooks[hookname] = f;
		},
		that
	);

	return hooks;
}


////////////////////
//                //
//	get Flourish  //
//                //
////////////////////

function get_flourish() {

	// Make HTML for a horizontal page division with a flourish
	var flourish = $('<div class="hr_flourish"></div>');
	flourish.append('<div class="hr"></div>');
	flourish.append('<div class="flourish"></div>');

	return flourish;
}


//////////////////////////
//  					//
//  ToggleHidden widget	//
//  					//
//////////////////////////

function ToggleHidden(toggle_div, content) {

	// determine initial state of the content: is it already displayed?
	var state = 'hidden';
	if(content.css('display') == 'block') {
		state = 'shown';
	}

	// create hooks support
	var hooks = make_page_hooks(this, ['on_show', 'on_hide']);

	// public
	this.toggle = function() {
		if(state == 'shown') {
			content.css('display', 'none');
			state = 'hidden';
			hooks.on_hide();

		} else if(state == 'hidden') {
			content.css('display', 'block');
			state = 'shown';
			hooks.on_show();

		} else {
			js_error('ToggleHidden: unexpected state');
		}
	}
	
	// register display toggling behavior to clickable element
	toggle_div.click(this.toggle);
}




//////////////////////
//  				//
//   Reply widget	//
//  				//
//////////////////////

function ReplyWidget(form, endpoint, submit_button) {

	var events = ['before', 'success', 'error', 'after'];
	var hooks = make_page_hooks(this, events);
	hooks.error = alert_ajax_error;

	// the ReplyWidget decorates a form widget
	var form_widget = new FormWidget(form, endpoint, submit_button);

	// get the reply text-area
	var reply_input = $('textarea[name=body]', form);

	// when the reply is successfully posted, clear the textarea,
	// and call the success hook
	var success = function(data, statusText, jqXHR) {
		reply_input.val('');
		hooks.success(data, statusText, jqXHR);
	}

	// forward hooks to the underlying form widget
	form_widget.hook('success', success);
	form_widget.hook('before', hooks.before);
	form_widget.hook('error', hooks.error);
	form_widget.hook('after', hooks.after);
}




//////////////////////
//  				//
//  Comment widget	//	Deprecated.  Just use FormWidget.
//  				//
//////////////////////

//function CommentWidget(form, endpoint, submit_button) {
//
//	var events = ['before', 'success', 'error', 'after'];
//	var hooks = make_page_hooks(this, events);
//	hooks.error = alert_ajax_error;
//
//	// the CommentWidget decorates a form widget
//	var form_widget = new FormWidget(form, endpoint, submit_button);
//
//	// get the comment text-area
//	var comment_input = $('textarea[name=body]', form);
//
//	// when the comment is successfully posted, clear the textarea,
//	// and call the success hook
//	var success = function(data, statusText, jqXHR) {
//		comment_input.val('');
//		hooks.success(data, statusText, jqXHR);
//	}
//
//	// forward hooks to the underlying form widget
//	form_widget.hook('success', success);
//	form_widget.hook('before', hooks.before);
//	form_widget.hook('error', hooks.error);
//	form_widget.hook('after', hooks.after);
//}


function AddFactorVersionWidget(add_link, form_wrapper, 
	num_forms_input, valence) {

	var events = ['success', 'error'];
	var hooks = make_page_hooks(this, events);
	hooks.error = alert_ajax_error;
	
	this.click_callback = $.proxy(function(){

		var num_forms = parseInt(num_forms_input.val());

		// a callback to put the new form when received
		var success = $.proxy(function (data, textStatus, jqXHR) {

			// call the success hook
			hooks.success(data.html, num_forms + 1);

			// insert the new form and increment the total number of forms
			form_wrapper.append(data.html);
			num_forms_input.val(num_forms + 1);
		}, this);

		ajax(
			'get_factor_form',
			{ 
				'valence': valence,
				'include_id': num_forms
			},
			{ 'success': success }
		);
	},this);

	add_link.click(this.click_callback);

}

