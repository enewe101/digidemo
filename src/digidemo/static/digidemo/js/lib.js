

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
// and optionally fires `success` or `error` with the plain text content.
function ajaxHtml(endpoint, data, handlers) {

	handlers = handlers || {};

	var error = handlers['error'];
	if (ALERT_AJAX_ERRORS) {
		var error = function(response, textStatus) { 
			alert(response.status + ': ' + response.responseText);
		};
	}

	$.ajax({
		"url": handle_ajax_html_url + endpoint + '/',
		"data": data,
		"method":'POST',
		"dataType": 'text',
		"success": handlers['success'],
		"error": error
	});
}


// sends the plain js object `data` to the django ajax function `endpoint`
// and optionally fires `success` or `error` with the parsed JSON response.
function ajax(endpoint, data, handlers) {

	handlers = handlers || {};

	var error = handlers['error'];
	if (ALERT_AJAX_ERRORS) {
		var error = function(response, textStatus) { 
			alert(response.status + ': ' + response.responseText);
		};
	}

	$.ajax({
		"url": handle_ajax_json_url + endpoint + '/',
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

function register_form(form_id, endpoint, form_class, submit_id, handlers) {

	var form_widget = new FormWidget(
		$('#'+form_id), endpoint, $('#' + submit_id), handlers);

	register_widget(form_id, form_widget, form_class);

}

function FormWidget(form, endpoint, submit_button, handlers) {

	handlers = handlers || {};

	this.pagehooks = {
		'before': function(){},
		'success': function(){},
		'error': function(){},
		'after': function(){}
	};

	submit_button.click( $.proxy(
		function() {
			ajaxForm(
				endpoint,
				form,
				{
					'before': $.proxy(function(data) {
						this.pagehooks['before']();
					}, this),

					'success': $.proxy(function(data, textStatus, jqXHR) {
						if(data.success) {
							this.pagehooks['success']();
						} else {
							this.pagehooks['error']();
						}

					}, this),

					'error': $.proxy(function(data, textStatus, jqXHR) {
						this.pagehooks['error']();
					}, this),

					'after': $.proxy(function(data, textStatus, jqXHR) {
						this.pagehooks['after']();
					}, this)
				}
			);
		}, this)
	);
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
	this.pagehooks = {
		'before': function(){},
		'success': function(){},
		'error': function(){},
		'after': function(){}
	}


	// posts the vote using ajax
	this.send_vote = function() {

		this.valence.val(this.state);

		ajaxForm(
			endpoint,
		   	this.form,
			{
				'before': $.proxy(
					function(data, textStatus, jqXHR) {
						this.pagehooks.before(data, textStatus, jqXHR);
					}, 
					this
				),

				'success': $.proxy(
					function(data, textStatus, jqXHR) {
						this.pagehooks.success(data, textStatus, jqXHR);
					}, 
					this
				),

				'error': $.proxy(
					function(data, textStatus, jqXHR) {
						this.pagehooks.error(data, textStatus, jqXHR);
					}, 
					this
				),

				'after': $.proxy(
					function(data, textStatus, jqXHR) {
						this.pagehooks.error(data, textStatus, jqXHR);
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

	this.wrapper = wrapper;
	this.users = init_users;

	this.add_user = function(user_pk) {
		
		// if the user is already in the list, do nothing
		if($.inArray(user_pk, this.users) >= 0) {
			alert('already in list!');
			return;
		}

		// otherwise, we add the user, and append her avatar image
		this.users.push(user_pk);
		this.get_user_avatar_html(user_pk);

	}

	this.get_user_avatar_html = function(user_pk) {
		ajaxHtml(
			'get_resender_avatar',
		   	{'user_pk':user_pk}, 
			{'success': $.proxy(function(html){
				alert('html')
				this.wrapper.prepend(html);
			}, this)}
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

function make_page_hooks(args) {

	// collect an array of valid hooks and initialize them to noop
	var valid_hooks = []
	var pagehooks = {}

	for(var i=1; i<arguments.length; i++) {
		var hookname = arguments[i];
		valid_hooks.push(hookname);
		pagehooks[hookname] = noop;
	}


	// make a public pagehook assignment function
	var that = arguments[0];
	that.pagehook = $.proxy( 
		function(hookname, f) {
			// do some validation
			// ensure hookname is valid
			if(!(hookname in pagehooks)) {
				js_error('pagehook error: ' + hookname 
					+ ' is not a valid hookname');
				return
			}

			// ensure hook is a function
			if(typeof f != 'function') {
				js_error('pagehook error: pagehook must be a function.  Got: ' 
					+ f);
			}

			// everything ok, assign the hook
			pagehooks[hookname] = f;
		},
		that
	);

	return pagehooks;
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

	// create pagehooks support
	var pagehooks = make_page_hooks(this, 'on_show', 'on_hide');

	// public
	this.toggle = function() {
		if(state == 'shown') {
			content.css('display', 'none');
			state = 'hidden';
			pagehooks.on_hide();

		} else if(state == 'hidden') {
			content.css('display', 'block');
			state = 'shown';
			pagehooks.on_show();

		} else {
			js_error('ToggleHidden: unexpected state');
		}
	}
	
	// register display toggling behavior to clickable element
	toggle_div.click(this.toggle);
}

