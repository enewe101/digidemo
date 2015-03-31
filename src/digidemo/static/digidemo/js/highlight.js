function Highlightable(
	wrapper, on_highlight_start, on_highlight_abort, highlighted_class_name,
	color
) {

	// alias 'this' to keep context during event callbacks
	var that = this;

	color = color || 'yellow';
	
	// fires when a highlight is started.  The highlight
	// 		- can interrupt highlighting
	// 		- is passed selected html and the 'highlightified html'
	//
	on_highlight_start = (
		on_highlight_start || function(){return true;}
	)

	// fires when a selection isn't unique and so highlighting is aborted
	on_highlight_abort = on_highlight_abort || function(){};

	// class name used to make the highlight styling
	highlighted_class_name = highlighted_class_name || 'highlight'

	// these regexes help remove fictitious tags when getting selected html
	var start_tags = /^(<[^<>]+>)+/g;
	var end_tags = /(<[^<>]+>)$/g;

	// matches any htmlish tag
	var tag_matcher = /(<[^<>]+>)/g;

	// used to insert highlighting spans
	//var replacer = '</span>$1<span class="' + highlighted_class_name + '">';

	// used to remember the original html in the wrapper
	var original_html = wrapper.html();

	// used to store the selected text
	var quote = '';

	function getSelectedHtml() {
		var selection = rangy.getSelection();
		return selection.toHtml();
	}

	function strip_extraneous_tags(html) {
		// remove fake opening and closing tags
		html = html.replace(start_tags, '');
		html = html.replace(end_tags, '');
		return html;
	}

	function _is_unique(html) {

		// find the indeces of the first and last occurance
		// of the input string within the wrapper html
		var first = original_html.indexOf(html);
		var last = original_html.lastIndexOf(html);

		// if those indices are the same, then the 
		// html snippet is unique
		if(first === last){
			return true;
		}

		return false;
	}

	function highlightify(s, color) {
		var open_span = '<span class="' + highlighted_class_name + '">';
		if(typeof color !== 'undefined') {
			open_span = (
				'<span style="background-color:'+color+';" '
				+ 'class="' + highlighted_class_name + '">'
			)
		}
		replacer = '</span>$1' + open_span;

		s = s.replace(tag_matcher, replacer);
		s = open_span + s + '</span>';
		return s;
	}

	function _clear() {
		wrapper.html(original_html);
	}

	this.clear = function() {
		_clear();
	}

	this.has_match = function(html) {
		return original_html.indexOf(html)>=0
	};

	function _highlight(html, color, trigger_callbacks, e) {

		if(!_is_unique(html)) {
			if(trigger_callbacks) {
				on_highlight_abort();
			}

		// if the user selects a region that is already highlighted, the
		// method will fail.  Clear the existing highlight so they can try 
		// again
		} else if (!that.has_match(html)) {
			_clear();
			return false;

		} else if (html != '') {

			var highlightified_html = highlightify(html, color);

			// fire the callback, which may cause highlight
			// prevent the highlighting
			var proceed = true;
			if(trigger_callbacks) {
				proceed = on_highlight_start(
					html, highlightified_html, quote, e
				);
			}

			if(proceed) {

				_clear();

				// splice in the highlightified html
				wrapper.html(
					original_html.replace(
						html, highlightified_html
					)
				);

				// some stuff was highlighted!
				return true
			}
		}

		// nothing was highlighted
		return false;
	}

	// make _highlight public
	this.highlight = function(html, color) {
		return _highlight(html, color, false);
	};

	// make _is_unique public
	this.is_unique = function(html) {
		return _is_unique(html);
	};

	wrapper.mouseup(function(e) {
		quote = getSelectedHtml();
		var html = strip_extraneous_tags(quote);
		var success = _highlight(html, color, true, e);
	});

};


function Annotatable(wrapper, annotation_form, color, class_prefix) {

	// alias 'that' to keep context during event callbacks
	var that = this;

	color = color || 'yellow';

	if(typeof doc_id === 'undefined') {
		doc_id = '';
	}

	if(typeof class_prefix === 'undefined') {
		class_prefix = 'highlight';
	}

	annotation_form.register_annotatable(this);

	var state = 'rest';

	// remember what was selected
	var keep_html = '';
	var keep_quote = '';
	var keep_high_html = '';

	// remember what was highlighted
	var comment_html = '';
	var comment_quote = '';

	// stores the position at which that the annotation widget will appear
	var comment_X = null;
	var comment_Y = null;

	// make the annotation widgetry
	var annotator = $('<div/>').addClass(class_prefix + '_annotator')
	if(!django.IS_USER_AUTHENTICATED) {
		annotator.attr('title', 'You must log in to comment!');
	}
	var word_bubble_image = $('<img/>').attr(
		'src', django.STATIC_URL + 'digidemo/images/word_bubble_icon.png');
	annotator.append(word_bubble_image);


	// keep a list of annotation objects
	var annotations = [];

	function delay_highlight(html, high_html, quote, e) {
		$('body').append(annotator);

		// show and position the annotator button
		comment_Y = e.pageY - 40;
		comment_X = e.pageX;

		annotator.css('top', e.pageY - 40);
		annotator.css('left', e.pageX);
		annotator.css('display', 'block');

		keep_html = html;
		keep_high_html = high_html;
		keep_quote = quote;

		state = 'ready';
		return false
	}


	var highlightable = new Highlightable(
		wrapper, delay_highlight, null, class_prefix, color);


	// expose highlighting functionality of underlying highlighter
	function _highlight(html, color) {
		highlightable.highlight(html, color);
	}

	// make the highlighting functionality public
	this.highlight = function(html, color) {
		_highlight(html, color);
	}

	// expose clear functionality of underlying highlighter
	function _clear() {
		highlightable.clear();
	}

	// make the clear functionality public
	this.clear = function() {
		_clear();
	}

	// clears any open word-bubbles from annotations
	function _clear_annotation_text() {
		for(var i=0; i<annotations.length; i++) {
			annotations[i].hide();
		}
	}

	// make the clear annotation text functionality public
	this.clear_annotation_text = function() {
		_clear_annotation_text();
	};

	function highlight_and_comment() {
		highlightable.highlight(keep_html, color);

		annotation_form.show(
			that.save_comment,
			that.cancel_comment,
			comment_Y,
		   	comment_X,
			keep_html,
			keep_quote
		);


		comment_html = keep_html;
		comment_quote = keep_quote;

		state = 'commenting';

	}

	this.cancel_comment = function() {
		highlightable.clear();
		state = 'rest';
	}

	this.save_comment = function(
		comment_html, comment_quote, comment, comment_id
	) {

		state = 'rest';

		var new_annotation = new Annotation(
			wrapper, 
			that, 
			annotation_form,
			comment_html, 
			comment_quote, 
			comment,
			comment_id,
			{
				'username': django['USER']['username'],
				'rep': django['USER_PROFILE']['rep'],
				'avatar_url': (
					django['MEDIA_URL'] 
					+ django['USER_PROFILE']['avatar_img']
				)
			},
			true,
			color
		);
		annotations.push(new_annotation);
	}

	this.add_annotation = function(
		anchor, quote, text, annotation_id, user_data, do_show, color) {

		// check if the annotation that is being loaded actually matches 
		// html in the wrapper, and whether it matches uniquely.
		var has_match = highlightable.has_match(anchor);
		var is_unique = highlightable.is_unique(anchor);

		if(has_match && is_unique) {
			var new_annotation = new Annotation(
				wrapper, 
				that, 
				annotation_form,
				anchor, 
				quote, 
				text,
				annotation_id,
				user_data,
				do_show,
				color
			);
			annotations.push(new_annotation);
			return true;
		}
		return false
	};

	annotator.click(highlight_and_comment);

	$(document).click(function(){
		if(state === 'rest') {
			
		} else if(state === 'ready'){
			state = 'set';

		} else if(state === 'set') {
			annotator.css('display', 'none');
			state = 'rest';

		} else if (state=== 'commenting') {
			annotator.css('display', 'none');

		// this catches bad states and returns to rest
		} else {
			state = 'rest';
		}

		_clear_annotation_text();
		
	})
}


var color_inc = 0;
var colors = ['red', 'green', 'blue'];
function get_next_color() {
	color = colors[color_inc];
	color_inc = (color_inc + 1) % colors.length;
	return color;
}


function Annotation(
	wrapper, annotatable, annotation_form, html, quote, annotation_text, 
	annotation_id, data, do_show, color
) {

	// determines whether the annotation shows when added.  Default is to show
	if(typeof do_show === 'undefined') do_show = true;

	var editable = false;
	if(django['USER'] && data['username']==django['USER']['username']) {
		editable = true;
	}

	var locator = '<span id="annotation_locator"></span>';
	var marker = $('<div/>').addClass('annot_marker');
	var color = color || get_next_color();
	marker.css('background-color', color);
	if(editable) {
		marker.css('border', 'solid 1px rgb(170, 0, 212)');
	} else {
		marker.css('border', 'solid 1px ' + color);
	}

	var annotation = $('<div/>').addClass('annotation');
	var user_id = $('<div/>').addClass('user_id');
	var avatar_image = $('<img/>').addClass('avatar_image_micro').attr(
		'src', data['avatar_url']
	);
	var user_info = $('<div/>').addClass('user_info');
	var username = $('<div/>').addClass('username').text(data['username']);
	var user_rep = $('<div/>').text(data['rep']);
	var annotation_text_span = $('<span/>').text(annotation_text);

	user_info.append(username).append(user_rep);
	user_id.append(avatar_image).append(user_info);
	annotation.append(user_id).append(annotation_text_span);

	function show_edit_form() {
		annotatable.clear();
		_clear_annotation_text();
		annotatable.highlight(html, color);

		annotation_form.show(
			save,
			show_annotation,
			position.top + 20,
		   	position.left,
			html,
			quote,
			annotation_text,
			annotation_id
		);
	}

	function save(html, quote, comment_text) {
		annotation_text_span.text(comment_text);
		show_annotation();
	}

	function _delete() {
		ajax(
			'delete_inline_comment',
			{'comment_id': annotation_id},
			{
				'success': function(data, textStatus, jqXHR){ 
					fully_hide();
				}
			}
		);

	}

	if(editable) {
		var edit_div = $('<div/>').addClass('edit_annotation_div');
		var edit_link = $('<a/>').text('edit');
		var delete_link = $('<a/>').text('delete');

		edit_link.click(show_edit_form);
		delete_link.click(_delete);

		edit_div.append(edit_link).append(delete_link);
		annotation.append(edit_div);
	}

	var state = 'hidden';

	function show_annotation() {
		annotatable.clear();
		annotatable.highlight(html, color);
		$('body').append(annotation);
		annotation.css({
			'display': 'block',
			'top': position.top + 20,
			'left': position.left
		});

		state = 'ignore_hide';
	}


	// clicking on the annotation itself does not clear it
	annotation.click(function() {
		state = 'ignore_hide';
	});

	// clears word-bubbles associated to annotations, but not highlight
	function _clear_annotation_text() {
		annotation.css('display', 'none');
	}

	// expose the clear_annotation_text functionality publicly
	this.clear_annotation_text = function() {
		_clear_annotation_text();
	}

	// hides everything except the marker
	function _hide() {
		_clear_annotation_text();
		state = 'hidden';
	}

	//expose hide publicly
	this.hide = function() {
		if(state === 'ignore_hide') {
			state = 'showing';
		} else if(state === 'showing') {
			_hide();
		} else if (state === 'hidden') {
			// do nothing
		} else if (state === 'fully_hidden') {
			// do nothing
		}
	}

	// hides everything including the marker
	function fully_hide() {
		_clear_annotation_text();
		marker.css('display', 'none');
		annotatable.clear();
		state = 'fully_hidden'
	}
	
	marker.click(show_annotation);

	// use a span to locate the annotation in the text
	var original_html = wrapper.html();
	var new_html = original_html.replace(html, html + locator)
	wrapper.html(new_html);
	var position = $('#annotation_locator').position();
	wrapper.html(original_html);

	marker.css({'top': position.top - 4, 'left': position.left-4});
	$('body').append(marker);

	if(do_show) show_annotation();
}


function GenericAnnotationForm(send_comment) {

	send_comment = send_comment || function(a,b,c) {
		alert(a + '; ' + b + '; ' + c);
	}

	var annotatable = null;

	// alias 'that' to preserve context in event callbacks
	var that = this;

	var html = '';
	var quote = '';

	this.show = function(X,Y,_html,_quote) {
		html = _html;
		quote = _quote;

		$('body').append(wrapper);
		wrapper.css('display', 'block');
		wrapper.css('top', X);
		wrapper.css('left', Y);
	};

	this.register_annotatable = function(annot) {
		annotatable = annot;
	}

	function cancel() {
		that.hide()
		annotatable.cancel_comment();
	}

	this.hide = function() {
		 wrapper.css('display', 'none');
	}

	function save() {
		var comment = comment_input.val()
		send_comment(
			comment,
			html,
			quote
		)

		that.hide();

		// need to get all this into AnnForm scope
		annotatable.save_comment(
			html, quote, comment, doc_id
		);

	}

	var class_prefix = 'highlight';
	var wrapper = $('<div/>').addClass(class_prefix + '_comment_wrapper');
	wrapper.draggable();
	var comment_input = $('<textarea/>').addClass(class_prefix + '_textarea');
	var comment_cancel = $('<input type="button" value="cancel" />').addClass(
		class_prefix + '_cancel_button'
	);
	var comment_save = $('<input type="button" value="save" />').addClass(
		class_prefix + '_save_button'
	);
	wrapper.append(comment_input);
	wrapper.append(comment_cancel);
	wrapper.append(comment_save);
	comment_cancel.click(cancel);
	comment_save.click(save);

	this.wrapper = wrapper;

}

