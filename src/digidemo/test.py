import time
import copy
import unittest
from django.core.urlresolvers import reverse
from django.core.files import File
from django.test import TestCase, LiveServerTestCase
from django.utils.html import escape
from digidemo import settings, markdown as md
from digidemo.models import *
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import filecmp
import os

def pyWait(predicate, timeout=3, period=0.15):

	start = time.time()
	max_time = start + timeout

	while time.time() < max_time:
		if predicate():
			return True
		time.sleep(period)
	
	return False


def createUser():
	# Create an auth_user
	user = User.objects.create_user(
		'test_username', 'test@example.com', 'test_password')
	user.save()
	
	# Create an associated user profile
	user_profile = UserProfile(
		user=user,
		email_validated=True,
		rep=0,
		street='test_street',
		zip_code='H0H0H0',
		country='CAN',
		province='QC'
	)
	user_profile.save()
	return user


def text_is_similar(text_1, text_2):
	'''
		checks for equality in strings, ignoring any white space.
	'''
	MATCH_WSPACE = re.compile(r'\s')
	text_1 = MATCH_WSPACE.sub('', text_1)
	text_2 = MATCH_WSPACE.sub('', text_2)
	return text_1 == text_2



class SeleniumTestCase(LiveServerTestCase):
	'''
		This is an abstract test class.  It provides derived classes with
		access to a WebDriver and a WebDriverWait object.  Any classes
		designed to test the actual behavior of webpages in a browser should
		inheret from this class.  See the wiki for an explanation of 
		how to use WebDriver and WebDriverWait
	'''

	@classmethod
	def setUpClass(cls):
		cls.driver = webdriver.Firefox()
		cls.wait = WebDriverWait(cls.driver, 3)	
		super(SeleniumTestCase, cls).setUpClass()

	@classmethod
	def tearDownClass(cls):
		cls.driver.quit()
		super(SeleniumTestCase, cls).tearDownClass()


	def element_contains(self, element_id, content, use_html=True):
		'''
			returns a boolean indicating whether the element with html_id
			<element_id> contains the text <content>.  Ignores differences
			in whitespace.
		'''
		if use_html:
			found_content = (
				self.driver.find_element('id', element_id)
				.get_attribute('innerHTML')
			)
		else:
			found_content = self.driver.find_element('id', element_id).text


		if not text_is_similar(found_content, content):
			print '<<'
			print found_content
			print '-- is different from --'
			print content
			print '>>'
			return False

		else: return True


	def elements_contain(self, contents_spec, use_html=True):
		'''
			returns a boolean value indicating whether each of the indicated 
			html elements (html id given as keys of <contents_spec>)
			contains the corresponding content (given as values of 
			<content_spec>).  Ignores differences in whitespace
		'''

		valid = True
		for element_id, content in contents_spec.items():
			valid = (
				self.element_contains(element_id, content, use_html)
				and valid
			)

		return valid

	def click(self, element_id):
		self.driver.find_element('id', element_id).click()


class QuestionRenderTest(SeleniumTestCase):
	'''
		tests that the test question in the database renders correctly
	'''

	def test_render(self):
		question = Question.objects.get(pk=1)
		self.driver.get(self.live_server_url + question.get_url())

		# Make sure the voting widget showed up properly
		self.driver.find_element_by_id('QuestionVoteForm_q_upvote')
		self.driver.find_element_by_id('QuestionVoteForm_q_score')
		self.driver.find_element_by_id('QuestionVoteForm_q_downvote')

		# make sure the question contents displayed correctly
		title = self.driver.find_element_by_class_name('post_title')
		self.assertEqual(title.text, question.title)
		body = self.driver.find_element_by_class_name('post_body')
		self.assertEqual(body.text, question.text)

		# make sure that all the answers showed up
		answers = Answer.objects.filter(target=question)
		answer_divs = self.driver.find_elements_by_class_name('subpost_body')
		self.assertEqual(len(answer_divs), answers.count())
		space_match = re.compile(r'\s')
		for i in range(len(answer_divs)):
			a, a_div = answers[i], answer_divs[i]
			self.assertEqual(
				space_match.sub('', a_div.text), 
				space_match.sub('', a.text)
			)
			self.driver.find_element('id', 'AnswerVoteForm_%d_upvote'%(i+1))
			self.driver.find_element('id', 'AnswerVoteForm_%d_score'%(i+1))
			self.driver.find_element('id', 'AnswerVoteForm_%d_downvote'%(i+1))
		



class CommentTest(SeleniumTestCase):

	def test_petition_comment(self):
		# choose a petition, go to its page
		letter = Letter.objects.get(pk=1)
		comment_form_spec = {
			'url': self.live_server_url + letter.get_url(),
			'comment_class': Comment,
			'comment_textarea_id': 'LetterCommentForm_1_text',
			'toggler_id': '_w_toggle_hidden_comment_1',
			'comment_text': 'Test comment!',
			'comments_wrapper_id': 'comments_1',
			'comments_class': 'letter_comment',
			'username': User.objects.get(pk=1).username,
			'submit_id': 'LetterCommentForm_1_submit'
		}
		self.submit_comment(**comment_form_spec)


	def test_blank_petition_comment(self):
		# choose a petition, go to its page
		letter = Letter.objects.get(pk=1)
		comment_form_spec = {
			'url': self.live_server_url + letter.get_url(),
			'comment_class': Comment,
			'comment_textarea_id': 'LetterCommentForm_1_text',
			'toggler_id': '_w_toggle_hidden_comment_1',
			'comment_text': 'Test comment!',
			'comments_wrapper_id': 'comments_1',
			'comments_class': 'letter_comment',
			'username': User.objects.get(pk=1).username,
			'submit_id': 'LetterCommentForm_1_submit',
			'error_div_id': 'LetterCommentForm_1_text_errors',
			'error_text': 'This field is required.'
		}
		self.submit_blank_comment(**comment_form_spec)

	def test_question_comment(self):
		# choose a petition, go to its page
		question = Question.objects.get(pk=1)
		comment_form_spec = {
			'url': self.live_server_url + question.get_url(),
			'comment_class': QuestionComment,
			'comment_textarea_id': 'QuestionCommentForm_q_text',
			'toggler_id': '_w_toggle_hidden_comment_q',
			'comment_text': 'Test comment!',
			'comments_wrapper_id': 'comments_q',
			'comments_class': 'letter_comment',
			'username': User.objects.get(pk=1).username,
			'submit_id': 'QuestionCommentForm_q_submit'
		}
		self.submit_comment(**comment_form_spec)

	def test_blank_question_comment(self):
		# choose a petition, go to its page
		question = Question.objects.get(pk=1)
		comment_form_spec = {
			'url': self.live_server_url + question.get_url(),
			'comment_class': QuestionComment,
			'comment_textarea_id': 'QuestionCommentForm_q_text',
			'toggler_id': '_w_toggle_hidden_comment_q',
			'comment_text': 'Test comment!',
			'comments_wrapper_id': 'comments_q',
			'comments_class': 'letter_comment',
			'username': User.objects.get(pk=1).username,
			'submit_id': 'QuestionCommentForm_q_submit',
			'error_div_id': 'QuestionCommentForm_q_text_errors',
			'error_text': 'This field is required.'
		}
		self.submit_blank_comment(**comment_form_spec)

	def test_answer_comment(self):
		# choose a petition, go to its page
		question = Question.objects.get(pk=1)
		comment_form_spec = {
			'url': self.live_server_url + question.get_url(),
			'comment_class': AnswerComment,
			'comment_textarea_id': 'AnswerCommentForm_1_text',
			'toggler_id': '_w_toggle_hidden_comment_1',
			'comment_text': 'Test comment!',
			'comments_wrapper_id': 'comments_1',
			'comments_class': 'letter_comment',
			'username': User.objects.get(pk=1).username,
			'submit_id': 'AnswerCommentForm_1_submit'
		}
		self.submit_comment(**comment_form_spec)

	def test_blank_answer_comment(self):
		# choose a petition, go to its page
		question = Question.objects.get(pk=1)
		comment_form_spec = {
			'url': self.live_server_url + question.get_url(),
			'comment_class': AnswerComment,
			'comment_textarea_id': 'AnswerCommentForm_1_text',
			'toggler_id': '_w_toggle_hidden_comment_1',
			'comment_text': 'Test comment!',
			'comments_wrapper_id': 'comments_1',
			'comments_class': 'letter_comment',
			'username': User.objects.get(pk=1).username,
			'submit_id': 'AnswerCommentForm_1_submit',
			'error_div_id': 'AnswerCommentForm_1_text_errors',
			'error_text': 'This field is required.'
		}
		self.submit_blank_comment(**comment_form_spec)

	def test_answer_comment_2(self):
		# choose a petition, go to its page
		question = Question.objects.get(pk=1)
		comment_form_spec = {
			'url': self.live_server_url + question.get_url(),
			'comment_class': AnswerComment,
			'comment_textarea_id': 'AnswerCommentForm_2_text',
			'toggler_id': '_w_toggle_hidden_comment_2',
			'comment_text': 'Test comment!',
			'comments_wrapper_id': 'comments_2',
			'comments_class': 'letter_comment',
			'username': User.objects.get(pk=1).username,
			'submit_id': 'AnswerCommentForm_2_submit'
		}
		self.submit_comment(**comment_form_spec)

	def test_blank_answer_comment_2(self):
		# choose a petition, go to its page
		question = Question.objects.get(pk=1)
		comment_form_spec = {
			'url': self.live_server_url + question.get_url(),
			'comment_class': AnswerComment,
			'comment_textarea_id': 'AnswerCommentForm_2_text',
			'toggler_id': '_w_toggle_hidden_comment_2',
			'comment_text': 'Test comment!',
			'comments_wrapper_id': 'comments_2',
			'comments_class': 'letter_comment',
			'username': User.objects.get(pk=1).username,
			'submit_id': 'AnswerCommentForm_2_submit',
			'error_div_id': 'AnswerCommentForm_2_text_errors',
			'error_text': 'This field is required.'
		}
		self.submit_blank_comment(**comment_form_spec)


	def submit_comment(
			self,
			url,
			comment_class,
			comment_textarea_id,
			toggler_id,
			comment_text,
			comments_wrapper_id,
			comments_class,
			username,
			submit_id
		):

		# go to the given url
		self.driver.get(url)

		# get the comment textarea.  Initially it should be hidden empty.
		comment_textarea = self.driver.find_element('id', comment_textarea_id)
		self.assertFalse(comment_textarea.is_displayed())

		# reveal the comment form by clicking the toggler.  It should be empty
		comment_form_toggler = self.driver.find_element('id', toggler_id)
		comment_form_toggler.click()
		self.assertTrue(comment_textarea.is_displayed())
		self.assertEqual(comment_textarea.text, '')

		# Add a comment.  But first check how many comments there are.
		comments_wrapper = self.driver.find_element('id', comments_wrapper_id)
		comments = comments_wrapper.find_elements_by_class_name(
			comments_class)
		initial_num_comments = len(comments)
		comment_textarea.send_keys(comment_text)
		self.driver.find_element('id', submit_id).click()

		# Now expect that the number of comments will increse soon
		self.wait.until(lambda driver:
			len(comments_wrapper.find_elements_by_class_name(comments_class))
			== initial_num_comments + 1
		)
		last_comment = comments_wrapper.find_elements_by_class_name(
			comments_class)[-1]
		text = last_comment.find_element_by_class_name(
			'letter_comment_body').text
		author = last_comment.find_element_by_class_name(
			'comment_author').text
		self.assertEqual(text, comment_text)
		self.assertEqual(author, '~ ' + username)

		# Check that the comment can be found in the database
		comment_class.objects.get(text=comment_text)

		# Check that the comment textarea was hidden, and that when shown
		# it has been cleared of the last comment entered
		self.assertFalse(comment_textarea.is_displayed())
		comment_form_toggler.click()
		self.assertEqual(comment_textarea.get_attribute('value'), '')


	def submit_blank_comment(
			self,
			url,
			comment_class,
			comment_textarea_id,
			toggler_id,
			comment_text,
			comments_wrapper_id,
			comments_class,
			username,
			submit_id,
			error_div_id,
			error_text
		):

		# go to the given url
		self.driver.get(url)

		# get the comment textarea.  Initially it should be hidden empty.
		comment_textarea = self.driver.find_element('id', comment_textarea_id)
		self.assertFalse(comment_textarea.is_displayed())

		# reveal the comment form by clicking the toggler.  It should be empty
		comment_form_toggler = self.driver.find_element('id', toggler_id)
		comment_form_toggler.click()
		self.assertTrue(comment_textarea.is_displayed())
		self.assertEqual(comment_textarea.text, '')
		
		# Attempt to submit blank comment.  But first check how many 
		# comments there are.
		comments_wrapper = self.driver.find_element('id', comments_wrapper_id)
		comments = comments_wrapper.find_elements_by_class_name(
			comments_class)
		initial_num_comments = len(comments)
		self.driver.find_element('id', submit_id).click()

		# Now expect that an error will be displayed
		self.wait.until(lambda driver:
			driver.find_element('id', error_div_id).text == error_text)
		self.assertTrue('error' in comment_textarea.get_attribute('class'))

		# hide the comment textarea again
		comment_form_toggler.click()

		

class AnswerFormTest(SeleniumTestCase):

	def test_submit_answer(self):
		question = Question.objects.get(pk=1)
		submit_answer_spec = {
			'url': self.live_server_url + question.get_url(),
			'textarea_id': 'AnswerForm__text',
			'answer_class_name': 'subpost',
			'answer_text': 'A new answer!',
			'answer_body_class': 'subpost_body',
			'toggle_id': '_w_toggle_hidden_subpost_form_switch',
			'submit_id': 'AnswerForm__submit',
		}

		self.submit_answer(**submit_answer_spec)

	def test_submit_blank_answer(self):
		question = Question.objects.get(pk=1)
		submit_answer_spec = {
			'url': self.live_server_url + question.get_url(),
			'textarea_id': 'AnswerForm__text',
			'answer_class_name': 'subpost',
			'answer_text': 'A new answer!',
			'answer_body_class': 'subpost_body',
			'answer_error_id': 'AnswerForm__text_errors',
			'error_message': 'This field is required.',
			'toggle_id': '_w_toggle_hidden_subpost_form_switch',
			'submit_id': 'AnswerForm__submit'
		}

		self.submit_blank_answer(**submit_answer_spec)

	def submit_blank_answer(
			self,
			url,
			textarea_id,
			answer_class_name,
			answer_text,
			answer_body_class,
			answer_error_id,
			error_message,
			toggle_id,
			submit_id,
		):

		# go to the given page
		self.driver.get(url)

		# count how many answers are on the page initially
		initial_num_answers = len(
			self.driver.find_elements_by_class_name(answer_class_name))

		# submit a blank answer
		textarea = self.driver.find_element('id', textarea_id)
		self.driver.find_element('id', submit_id).click()

		# An error message should be displayed
		error_text = self.driver.find_element('id', answer_error_id).text
		self.assertEqual(error_text, error_message)

		# And the textarea should be styled with the class error
		self.assertTrue('error' in textarea.get_attribute('class'))


	def submit_answer(
			self,
			url,
			textarea_id,
			answer_class_name,
			answer_text,
			answer_body_class,
			toggle_id,
			submit_id,
		):

		# go to the given page
		self.driver.get(url)

		# count how many answers are on the page initially
		initial_num_answers = len(
			self.driver.find_elements_by_class_name(answer_class_name))

		# submit a new answer
		textarea = self.driver.find_element('id', textarea_id)
		textarea.send_keys(answer_text)
		self.driver.find_element('id', submit_id).click()

		# the new answer should appear shortly on the page
		self.wait.until(lambda driver:
			len(driver.find_elements_by_class_name(answer_class_name)) 
			== initial_num_answers + 1)
		last_answer = self.driver.find_elements_by_class_name(
			answer_class_name)[-1]
		last_answer_text = last_answer.find_element_by_class_name(
				answer_body_class).text
		self.assertEqual(last_answer_text, answer_text)

		# the new answer should appear in the database too
		answer = Answer.objects.get(text=answer_text)
		self.assertEqual(answer.target.pk, 1)

		# the answer form should have been hidden.  When revealed, it should
		# be blank.
		self.assertFalse(textarea.is_displayed())
		self.driver.find_element('id', toggle_id).click()
		self.assertTrue(textarea.is_displayed())
		self.assertEqual(textarea.get_attribute('value'), '')


class QuestionFormTest(SeleniumTestCase):
	'''
		Tests adding a question using the QuestionForm
	'''

	title_input_id = 'QuestionForm__title'
	title_text = 'Test Question Title?'

	textarea_id = 'QuestionForm__text'
	question_text = 'This is only a test?'

	texts = [
		(title_input_id, title_text),
		(textarea_id, question_text)
	]

	submit_id = 'QuestionForm__submit'


	def test_submit_question(self):

		# go to the submit question page 
		proposal = Proposal.objects.get(pk=1)
		url = self.live_server_url + proposal.get_question_url()
		self.driver.get(url)

		# fill out the inputs
		for t in self.texts:
			self.driver.find_element('id', t[0]).send_keys(t[1])

		# submit the form.  
		self.driver.find_element('id', self.submit_id).click()
		
		# We should be redirected to a page containing the question
		found_title_text = self.driver.find_element_by_class_name(
			'post_title').text
		self.assertEqual(found_title_text, self.title_text)
		found_question_text = self.driver.find_element_by_class_name(
			'post_body').text
		self.assertEqual(found_question_text, self.question_text)

		# The question should be in the database. (this automatically raises 
		# an error if no match for the query is found.)
		Question.objects.get(
			target=proposal, title=self.title_text, text=self.question_text)


	def test_submit_incomplete_question(self):
		FIELD_WRAPPER_ERROR_CLASS = 'field_wrapper_error'	

		# go to the submit question page 
		proposal = Proposal.objects.get(pk=1)
		url = self.live_server_url + proposal.get_question_url()
		self.driver.get(url)

		# submit without a title
		t = self.texts[1]
		body = self.driver.find_element('id', t[0])
		body.send_keys(t[1])

		# submit the form.  
		submit = self.driver.find_element('id', self.submit_id).click()

		# we should still face the form, and the title should have an 
		# error class and error message
		title = self.driver.find_element('id', self.texts[0][0])
		error_class = title.find_element_by_xpath('..').get_attribute('class')
		self.assertEqual(error_class, FIELD_WRAPPER_ERROR_CLASS)

		# submit without a question body
		t = self.texts[0]
		self.driver.find_element('id', self.texts[0][0]).send_keys(
			self.texts[0][1])
		self.driver.find_element('id', self.texts[1][0]).clear()
		self.driver.find_element('id', self.submit_id).click()

		# we should still face the form, and the title should have an 
		# error class and error message
		body = self.driver.find_element('id', self.texts[1][0])
		error_class = body.find_element_by_xpath('..').get_attribute('class')
		self.assertEqual(error_class, FIELD_WRAPPER_ERROR_CLASS)


class FormTest(SeleniumTestCase):

	def fill_form(self, form_data_spec, clear=[]):

		# clear is an optional element_id or list thereof for elements to
		# be cleared.  Helpful for filling all fields except certain ones.
		if isinstance(clear, basestring):
			clear = [clear]

		for form_element_id, form_data in form_data_spec.items():

			# form_data might just be the text to input itself
			if isinstance(form_data, basestring):
				input_type = 'text'
				input_val = form_data

			else:
				input_val = form_data['value']
				try:
					input_type = form_data['input_type']
				except KeyError:
					input_type = 'text'


			# first clear the input
			self.clear_input(form_element_id, input_type)

			# if this element was listed in the clear argument, 
			# then that's all we do
			if form_element_id in clear:
				continue

			# Next, delegate filling the element to the appropriate method
			self.fill_input(form_element_id, input_val, input_type)
			

	def fill_input(self, element_id, input_val, input_type):
		if input_type == 'text':
			self.driver.find_element('id', element_id).send_keys(input_val)

		elif input_type == 'select':
			Select(self.driver.find_element('id', element_id)).select_by_value(
				input_val)


	def clear_input(self, element_id, input_type):

		if input_type is None or input_type == 'text':
			self.driver.find_element('id', element_id).clear()

		elif input_type == 'select':
			# may not be implemented correctly
			Select(self.find_element('id', element_id)).select_by_value(
				'None')


class ProposalFormTest(FormTest):

	values = ['Test Proposal Title', 'This is only a test summary.',
				'This is only a test body.']
	form_data = {
		'ProposalVersionForm__title': {

			'value': values[0],
			'error_id': 'ProposalVersionForm__title_errors',
			'display_id': 'proposal_title',
			'expect': 'Test Proposal Title'

		}, 'ProposalVersionForm__summary': {

			'value': values[1],
			'error_id': 'ProposalVersionForm__summary_errors',
			'display_id': 'proposal_summary',
			'expect': md.markdown('This is only a test summary.')

		}, 'ProposalVersionForm__text': {

			'value': values[2], 
			'error_id': 'ProposalVersionForm__text_errors',
			'display_id': 'proposal_text',
			'expect': md.markdown('This is only a test body.')

		}
	}

	test_proposal_pk = 1
	submit_id = 'ProposalVersionForm__submit'
	escape_text = '<&>'
	error_msg = 'This field is required.'
	error_class = 'field_wrapper_error'
	username = 'superuser'	# TODO: test proper login

	def test_edit_proposal_ensure_escape(self):
		form_data_needs_escape = dict([
			(k, self.escape_text) for k in self.form_data.keys()])

		expect_escaped_data = {
			'proposal_title': escape(self.escape_text),
			'proposal_summary': md.markdown(escape(self.escape_text)),
			'proposal_text': md.markdown(escape(self.escape_text))
		}

		# Go to the edit page for a test proposal
		proposal = Proposal.objects.get(pk=self.test_proposal_pk)
		url = self.live_server_url + proposal.get_edit_url() 
		self.driver.get(url)

		# Fill and submit the form with data that should get escaped
		self.fill_form(form_data_needs_escape)
		self.driver.find_element('id', self.submit_id).click()

		# check that the proposal was correctly loaded
		self.assertTrue(self.elements_contain(expect_escaped_data))

		# check the database
		proposal = Proposal.objects.get(pk=self.test_proposal_pk)
		self.check_db(proposal, self.escape_text, 
			self.escape_text, self.escape_text, self.username)


	def check_db(self, proposal, title, summary, text, username):
		self.assertEqual(title, proposal.title)
		self.assertEqual(summary, proposal.summary)
		self.assertEqual(text, proposal.text)
		self.assertEqual(username, proposal.user.username)

		proposal_version = proposal.get_latest()
		self.assertEqual(title, proposal_version.title)
		self.assertEqual(summary, proposal_version.summary)
		self.assertEqual(text, proposal_version.text)
		self.assertEqual(username, proposal_version.user.username)


	def test_edit_proposal_incomplete(self):

		# html id's for the divs that contain error messages

		# Go to the edit page for a test proposal
		proposal = Proposal.objects.get(pk=self.test_proposal_pk)
		url = self.live_server_url + proposal.get_edit_url() 
		self.driver.get(url)

		# we'll submit the form several times, 
		# each time ommitting a different field
		for ommitted_id, spec in self.form_data.items():

			error_id = spec['error_id']

			self.fill_form(self.form_data, clear=ommitted_id)
			self.click(self.submit_id)

			# Check for the error message
			self.assertTrue(self.element_contains(error_id, self.error_msg,
				use_html=False))

			# Check that the input was styled with an error styling
			ommitted_elm = self.driver.find_element('id', ommitted_id)
			wrapper = ommitted_elm.find_element_by_xpath('..')
			self.assertTrue(
				self.error_class in wrapper.get_attribute('class'))


	def test_edit_proposal(self):

		# Go to the edit page for a test proposal
		proposal = Proposal.objects.get(pk=self.test_proposal_pk)
		url = self.live_server_url + proposal.get_edit_url() 
		self.driver.get(url)

		# Fill and submit the form with valid data
		self.fill_form(self.form_data)
		self.driver.find_element('id', self.submit_id).click()

		# check that the proposal was correctly loaded
		expect_data = dict([
			(v['display_id'], v['expect']) for v in self.form_data.values()
		])
		self.assertTrue(self.elements_contain(expect_data))

		# check the database
		proposal = Proposal.objects.get(pk=self.test_proposal_pk)
		self.check_db(proposal, *self.values, username=self.username)
			



class VoteTest(SeleniumTestCase):

	up_on_class = 'upvote_on'
	down_on_class = 'downvote_on'


	def test_QuestionVote(self):
		url = self.live_server_url + Question.objects.get(pk=1).get_url()
		vote_spec = {
			'up_id': 'QuestionVoteForm_q_upvote',
			'score_id': 'QuestionVoteForm_q_score',
			'down_id': 'QuestionVoteForm_q_downvote',
			'url': url
		}

		self.vote_test(**vote_spec)


	def test_AnswerVote(self):
		url = self.live_server_url + Question.objects.get(pk=1).get_url()
		vote_spec = {
			'up_id': 'AnswerVoteForm_1_upvote',
			'score_id': 'AnswerVoteForm_1_score',
			'down_id': 'AnswerVoteForm_1_downvote',
			'url': url
		}

		self.vote_test(**vote_spec)


	def test_NewAnswerVote(self):
		url = self.live_server_url + Question.objects.get(pk=1).get_url()
		self.driver.get(url)

		post_id = 1 + len(self.driver.find_elements_by_class_name('subpost'))

		self.driver.find_element('id', 'AnswerForm__text').send_keys('test')
		self.click('AnswerForm__submit')

		vote_spec = {
			'up_id': 'AnswerVoteForm_%d_upvote' % post_id,
			'score_id': 'AnswerVoteForm_%d_score' % post_id,
			'down_id': 'AnswerVoteForm_%d_downvote' % post_id,
			'url': url
		}

		self.vote_test(**vote_spec)


	def test_DiscussionVote(self):
		url = self.live_server_url + Discussion.objects.get(pk=1).get_url()
		vote_spec = {
			'up_id': 'DiscussionVoteForm_q_upvote',
			'score_id': 'DiscussionVoteForm_q_score',
			'down_id': 'DiscussionVoteForm_q_downvote',
			'url': url
		}

		self.vote_test(**vote_spec)


	def test_ReplyVote(self):
		url = self.live_server_url + Discussion.objects.get(pk=1).get_url()
		vote_spec = {
			'up_id': 'ReplyVoteForm_26_upvote',
			'score_id': 'ReplyVoteForm_26_score',
			'down_id': 'ReplyVoteForm_26_downvote',
			'url': url
		}

		self.vote_test(**vote_spec)


	def test_NewReplyVote(self):
		# figure out what the next post id will be
		user = User.objects.get(pk=1)
		post_id = 1 + Reply.objects.filter(user=user).order_by('-pk')[0].pk

		url = self.live_server_url + Discussion.objects.get(pk=1).get_url()
		self.driver.get(url)

		self.driver.find_element('id', 'ReplyForm__text').send_keys('test')
		self.click('ReplyForm__submit')

		vote_spec = {
			'up_id': 'ReplyVoteForm_%d_upvote' % post_id,
			'score_id': 'ReplyVoteForm_%d_score' % post_id,
			'down_id': 'ReplyVoteForm_%d_downvote' % post_id,
			'url': url
		}

		self.vote_test(**vote_spec)
	def get_elements(self):
		self.up_elm = self.driver.find_element('id', self.up_id)
		self.score_elm = self.driver.find_element('id', self.score_id)
		self.down_elm = self.driver.find_element('id', self.down_id)
		

	def get_voting_status(self):
		is_up_on = self.up_elm.get_attribute('class') == self.up_on_class
		is_down_on = self.down_elm.get_attribute('class') == self.down_on_class

		# the user may have either upvoted or downvoted, or neither
		# but not both
		state = 0
		if is_up_on:
			state = 1
			self.assertTrue(not is_down_on) 
		elif is_down_on:
			state = -1
			self.assertTrue(not is_up_on)

		score = int(self.score_elm.text)

		return (is_up_on, is_down_on, state, score)


	def vote_test(self, up_id, score_id, down_id, url):

		self.up_id = up_id
		self.score_id = score_id
		self.down_id = down_id

		# go to the right page
		self.driver.get(url)

		# get the vote widget elements
		self.get_elements()

		# what's the current voting state?
		is_up_on1, is_down_on1, state1, score1 = self.get_voting_status()

		# try upvoting, and get the new state
		self.up_elm.click()

		# get status after the vote
		is_up_on2, is_down_on2, state2, score2 = self.get_voting_status()

		# check that the right state transition occured
		if state1 == 1:
			self.assertEqual(state2, 0)
			self.assertEqual(score2, score1 - 1)

		elif state1 == 0:
			self.assertEqual(state2, 1)
			self.assertEqual(score2, score1 + 1)

		elif state1 == -1:
			self.assertEqual(state2, 1)
			self.assertEqual(score2, score1 + 2)

		# check that the vote was recorded by refreshing the page
		self.driver.get(url)

		# we should be in the same state as before refreshing
		self.get_elements()
		is_up_on3, is_down_on3, state3, score3 = self.get_voting_status()
		self.assertEqual(state3, state2)
		self.assertEqual(score3, score2)

		# now try downvoting
		self.down_elm.click()

		# get status after the vote
		is_up_on4, is_down_on4, state4, score4 = self.get_voting_status()

		# check that the right state transition occured
		if state3 == 1:
			self.assertEqual(state4, -1)
			self.assertEqual(score4, score3 - 2)

		elif state3 == 0:
			self.assertEqual(state4, -1)
			self.assertEqual(score4, score3 - 1)

		elif state3 == -1:
			self.assertEqual(state4, 0)
			self.assertEqual(score4, score3 + 1)

		# check that the vote was recorded by refreshing the page
		self.driver.get(url)

		# we should be in the same state as before refreshing
		self.get_elements()
		is_up_on5, is_down_on5, state5, score5 = self.get_voting_status()
		self.assertEqual(state5, state4)
		self.assertEqual(score5, score4)



class UserProfileTest(TestCase):
	'''
	Tests the user profile model object.  This makes sure that avatar images
	are saved to the correct folder and are properly copied
	'''

	TEST_AVATAR_RELATIVE_PATH = '../data/test/test_avatar.jpg'
	TEST_AVATAR_COPY_RELATIVE_PATH = '../media/avatars/test_avatar.jpg'
	REP_EVENTS = {
		'up_proposal': 10,
		'dn_proposal': -2,
		'up_letter': 10,
		'dn_letter': -2,
		'do_downvote': -2,
		'up_comment': 5,
		'dn_comment': -2,
		'up_discussion': 10,
		'dn_discussion': -2,
	}

	def tearDown(self):
		try:
			os.remove(self.TEST_AVATAR_COPY_RELATIVE_PATH)
		except OSError:
			pass


	def setUp(self):
		# Create an auth_user
		self.user = User.objects.create_user(
			'test_username', 'test@example.com', 'test_password')
		
		# Create an associated user profile
		self.user_profile = UserProfile(
			user=self.user,
			email_validated=True,
			rep=0,
			street='test_street',
			zip_code='H0H0H0',
			country='CAN',
			province='QC'
		)
		self.user_profile.save()


	def test_user_avatar_img(self):

		# give the user an avatar
		image_fh = open(self.TEST_AVATAR_RELATIVE_PATH)
		self.user_profile.avatar_img.save('test_avatar.jpg', File(image_fh))

		self.assertTrue(filecmp.cmp(
			self.TEST_AVATAR_RELATIVE_PATH,
			self.TEST_AVATAR_COPY_RELATIVE_PATH
		))


	def test_user_rep(self):

		pk = self.user_profile.pk
		for event, rep in self.REP_EVENTS.items():

			# give the user reputation
			self.user_profile.apply_rep(event)
			self.user_profile.save()

			# check if the user got reputation
			self.assertTrue(UserProfile.objects.get(pk=pk).rep == rep)

			# remove rep
			self.user_profile.undo_rep(event)
			self.user_profile.save()

			# check if the user got reputation removed
			self.assertTrue(UserProfile.objects.get(pk=pk).rep == 0)


