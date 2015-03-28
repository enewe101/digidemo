function Highlightable(
	wrapper, on_highlight_start, on_highlight_abort, highlighted_class_name
) {

	// alias 'this' to keep context during event callbacks
	var that = this;
	
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
	var replacer = '</span>$1<span class="' + highlighted_class_name + '">';

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

	function highlightify(s) {
		s = s.replace(tag_matcher, replacer);
		s = '<span class="' + highlighted_class_name + '">' + s + '</span>';
		return s;
	}

	function _clear() {
		wrapper.html(original_html);
	}

	this.clear = function() {
		_clear();
	}


	function _highlight(html, trigger_callbacks, e) {

		if(!_is_unique(html)) {
			if(trigger_callbacks) {
				on_highlight_abort();
			}

		// if the user selects a region that is already highlighted, the
		// method will fail.  Clear the existing highlight so they can try 
		// again
		} else if (original_html.indexOf(html)<0) {
			_clear();
			return false;

		} else if (html != '') {

			var highlightified_html = highlightify(html);

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
	this.highlight = function(html) {
		return _highlight(html, false);
	};

	// make _is_unique public
	this.is_unique = function(html) {
		return _is_unique(html);
	};

	wrapper.mouseup(function(e) {
		quote = getSelectedHtml();
		var html = strip_extraneous_tags(quote);
		var success = _highlight(html, true, e);
	});

};


function Annotatable(wrapper, send_comment, doc_id, class_prefix) {

	// alias 'that' to keep context during event callbacks
	var that = this;

	send_comment = send_comment || function(a,b,c,d) {
		//alert(a + '; ' + b + '; ' + c + '; ' + d);
	}

	if(typeof doc_id === 'undefined') {
		doc_id = '';
	}

	if(typeof class_prefix === 'undefined') {
		class_prefix = 'highlight';
	}

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
	var annotator = $('<div/>').addClass(class_prefix + '_annotator');
	var commenter = $('<div/>').addClass(class_prefix + '_comment_wrapper');
	commenter.draggable();
	var comment_input = $('<textarea/>').addClass(class_prefix + '_textarea');
	var comment_cancel = $('<input type="button" value="cancel" />').addClass(
		class_prefix + '_cancel_button'
	);
	var comment_save = $('<input type="button" value="save" />').addClass(
		class_prefix + '_save_button'
	);

	// keep a list of annotation objects
	var annotations = [];

	// assemble annotation widgetry
	commenter.append(comment_input);
	commenter.append(comment_cancel);
	commenter.append(comment_save);

	function delay_highlight(html, high_html, quote, e) {
		$('body').append(annotator);

		// show and position the annotator button
		comment_Y = e.pageY - 24;
		comment_X = e.pageX;

		annotator.css('top', e.pageY - 24);
		annotator.css('left', e.pageX);
		annotator.css('display', 'block');

		keep_html = html;
		keep_high_html = high_html;
		keep_quote = quote;

		state = 'ready';
		return false
	}


	var highlightable = new Highlightable(
		wrapper, delay_highlight, null, class_prefix);


	// expose highlighting functionality of underlying highlighter
	function _highlight(html) {
		highlightable.highlight(html, false, null);
	}

	// make the highlighting functionality public
	this.highlight = function(html) {
		_highlight(html);
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
			annotations[i].clear_annotation_text();
		}
	}

	// make the clear annotation text functionality public
	this.clear_annotation_text = function() {
		_clear_annotation_text();
	};

	function highlight_and_comment() {
		highlightable.highlight(keep_html);
		$('body').append(commenter);
		commenter.css('display', 'block');
		commenter.css('top', comment_Y);
		commenter.css('left', comment_X);

		comment_html = keep_html;
		comment_quote = keep_quote;

		state = 'commenting';

	}

	function cancel_comment() {
		commenter.css('display', 'none');
		highlightable.clear();
		state = 'rest';
	}

	function save_comment() {
		send_comment(
			comment_input.val(),
			comment_html,
			comment_quote,
			doc_id
		)
		commenter.css('display', 'none');
		state = 'rest';
		var new_annotation = new Annotation(
			wrapper, 
			that, 
			comment_html, 
			comment_quote, 
			comment_input.val(),
			doc_id
		);
		annotations.push(new_annotation);
	}

	annotator.click(highlight_and_comment);
	comment_cancel.click(cancel_comment);
	comment_save.click(save_comment);

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


function Annotation(wrapper, annotatable, html, quote, annotation, data) {

	var locator = '<span id="annotation_locator"></span>';
	var marker = $('<div/>').addClass('annot_marker');
	marker.css('background-color', get_next_color());

	var annotation = $('<div/>').addClass('annotation').text(annotation);

	var state = 'dodge';

	function show_annotation() {
		annotatable.clear();
		annotatable.highlight(html);
		$('body').append(annotation);
		annotation.css({
			'display': 'block',
			'top': position.top + 20,
			'left': position.left
		});

		state = 'dodge';
	}

	// clicking on the annotation itself does not clear it
	annotation.click(function() {
		state = 'dodge';
	});

	// clears word-bubbles associated to annotations, but not highlight
	function _clear_annotation_text() {
		annotation.css('display', 'none');
	}

	// expose the clear_annotation_text functionality publicly
	this.clear_annotation_text = function() {
		if(state === 'dodge') {
			state = 'rest';
		} else {
			_clear_annotation_text();
		}
	}

	marker.click(show_annotation);

	// use a span to locate the annotation in the text
	var original_html = wrapper.html();
	var new_html = original_html.replace(html, html + locator)
	wrapper.html(new_html);
	var position = $('#annotation_locator').position();
	wrapper.html(original_html);

	marker.css({'top': position.top - 4, 'left': position.left});
	$('body').append(marker);

	show_annotation();
}


function SynchronizedAnnotatable(wrapper, send_comment, doc_id, class_prefix) {
	// load annotations
	// save annotations
}
