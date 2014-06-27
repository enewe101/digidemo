function arm_proposal_form(
	parent_id,
	endpoint,
	upvoted_img,
	downvoted_img) {

	var form = $('#' + parent_id + ' .vote_form');
	var upvote = $('#' + parent_id + ' .upvote');
	var downvote = $('#' + parent_id + ' .downvote');
	var score = $('#' + parent_id + ' .score');
	var valence = $('#' + parent_id + ' input[name=valence]');

	arm_cast_vote(
		upvote, downvote, form, score, 1, upvoted_img, endpoint, valence);
	arm_cast_vote(
		downvote, upvote, form, score, -1, downvoted_img, endpoint, valence);
}


function arm_cast_vote(
	widget,
   	other_widget,
   	form,
   	score,
   	vote,
   	vote_widget_img,
	endpoint,
	valence) {

	// make the callback function to cary out voting when widget clicked
	var callback =  function() {


		// visual feedback
		$(this).attr('src', vote_widget_img);
		score.text(parseInt(score.text())+vote)

		// disable any more voting on this proposal
		$(this).off('click');
		other_widget.off('click');

		// set the valence in the voting form (+1 or -1)
		valence.val(vote);

		// submit the vote form by ajax
		ajaxForm(
			endpoint, 
			form,
			function(data){alert('success')},
			function(data){alert('error')}
		);
	};

	widget.on('click', callback);
}
