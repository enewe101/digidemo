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

	this.handlers = {
		'before': handlers['before'] || function(){},
		'success': handlers['success'] || function(){},
		'error': handlers['error'] || function(){},
		'after': handlers['after'] || function(){}
	};

	submit_button.click( $.proxy(
		function() {
			ajaxForm(
				endpoint,
				form,
				{
					'before': $.proxy(function(data) {
						this.pagehooks['before'](data, textStatus, jqXHR);
						this.handlers['before'](data); 
					}, this),

					'success': $.proxy(function(data, textStatus, jqXHR) {
						this.handlers['success'](data, textStatus, jqXHR);
						this.pagehooks['success'](data, textStatus, jqXHR);
					}, this),

					'error': $.proxy(function(data, textStatus, jqXHR) {
						this.handlers['error'](data, textStatus, jqXHR);
						this.pagehooks['error'](data, textStatus, jqXHR);
					}, this),

					'after': $.proxy(function(data, textStatus, jqXHR) {
						this.handlers['after'](data, textStatus, jqXHR);
						this.pagehooks['after'](data, textStatus, jqXHR);
					}, this)
				}
			);
		}, this)
	);
}


