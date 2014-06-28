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
				'before': $.proxy(function(data, textStatus, jqXHR) {
					return this.pagehooks.success(data, textStatus, jqXHR);
				}, this),
				'success': $.proxy(function(data, textStatus, jqXHR) {
					return this.pagehooks.success(data, textStatus, jqXHR);
				}, this),
				'error': $.proxy(function(data, textStatus, jqXHR) {
					return this.pagehooks.error(data, textStatus, jqXHR);
				}, this),
				'after': $.proxy(function(data, textStatus, jqXHR) {
					return this.pagehooks.error(data, textStatus, jqXHR);
				}, this)
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
