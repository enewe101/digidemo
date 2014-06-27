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

