# TODO: remove classmethod decorators from SeleniumTestCase

import json
import time
import copy
import unittest
from django.core.urlresolvers import reverse
from django.core.files import File
from django.test import TestCase, LiveServerTestCase
from django.utils.html import escape
from digidemo import settings, markdown as md
from digidemo.models import *
from digidemo.abstract_models import *
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import filecmp
import os

REG_USERNAME = 'regularuser'

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

	LIVE_SERVER_URL = 'localhost:8081'

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


	# Check if the elements identified by their id's contain the given text
	# By default this matches the actual html found in the element, but it
	# can match based on the rendered text too (what you'd be able to 
	# copy/paste).
	#
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


	# Click the element. Just a convinience method. 
	#
	@classmethod
	def click(cls, element_id):
		cls.driver.find_element('id', element_id).click()


	# fill out the text (form) input with the string
	# 
	@classmethod
	def put(cls, text_input_id, string):
		cls.driver.find_element('id', text_input_id).send_keys(string)


	# Fill several text inputs with the provided text.  
	# (Uses html ids to find the inputs.)
	# 
	@classmethod
	def puts(cls, put_spec):
		'''
			Put spec is a dictionary -- keys are the html ids for text inputs
			and the values are the text to place in the inputs
			e.g. 
				{'some_input_id': 'some_text', 'another_input': 'more_text'}
		'''
		for text_input_id, text in put_spec.items():
			cls.put(text_input_id, text)


	# login as a regular user
	# 
	@classmethod
	def login_regularuser(cls):
		cls.login('regularuser', 'regularuser')


	# login as a super user (actually same as regular user right now)
	#
	@classmethod
	def login_superuser(cls):
		cls.login('superuser', 'superuser')


	# This should only be used to access the live server url inside class
	# methods.  Otherwise, just use self.live_server_url itself
	# 
	@classmethod
	def get_live_server_url(cls):
		return cls.LIVE_SERVER_URL


	# Go to login page and login using provided credentials
	# 
	@classmethod
	def login(cls, username, password):


		# Go to the login page
		LOGIN_URL = '/login_required/'
		cls.driver.get(cls.get_live_server_url() + LOGIN_URL)

		# login with the credentials
		cls.puts({
			'LoginForm__username': username,
			'LoginForm__password': password
		})

		cls.click('LoginForm__submit')
		


## Useful if you have a few tests one class that need to login. 
## it logs in the user once when the test class is first made.
## Make sure to put it *after* SeleniumTestCase!! 
## 
## e.g.
##	MyTetClass(SeleniumTestCase, RegularuserMixin): ...
##
## of regular user at the start of a test class's execution.  
##
#class RegularuserMixin(object):
#	@classmethod
#	def setUpClass(cls):
#		super(RegularuserMixin, cls).setUpClass()
#		print 'doing mixin'
#		cls.login_regularuser()






# Tests the leaving comments.  Tests the comment forms for all the various
# types of comments and places they occur.  Tests that submitting an empty
# comment generates an error message for the user.  
#
class CommentTest(SeleniumTestCase):

	def test_comments(self):

		# login the regular user
		self.login_regularuser()

		# try out all the comment forms
		self.petition_comment()
		self.blank_petition_comment()
		self.question_comment()
		self.blank_question_comment()
		self.answer_comment()
		self.blank_answer_comment()
		self.answer_comment_2()
		self.blank_answer_comment_2()


	def petition_comment(self):
		# choose a petition, go to its page
		letter = Letter.objects.get(pk=1)
		comment_form_spec = {
			'url': self.live_server_url + letter.get_url(),
			'comment_class': Comment,
			'comment_textarea_id': 'LetterCommentForm_1_text',
			'toggler_id': '_w_toggle_hidden_comment_1',
			'comment_text': 'Test comment 1!',
			'comments_wrapper_id': 'comments_1',
			'comments_class': 'letter_comment',
			'username': REG_USERNAME,
			'submit_id': 'LetterCommentForm_1_submit'
		}
		self.submit_comment(**comment_form_spec)


	def blank_petition_comment(self):
		# choose a petition, go to its page
		letter = Letter.objects.get(pk=1)
		comment_form_spec = {
			'url': self.live_server_url + letter.get_url(),
			'comment_class': Comment,
			'comment_textarea_id': 'LetterCommentForm_1_text',
			'toggler_id': '_w_toggle_hidden_comment_1',
			'comment_text': 'Test comment 2!',
			'comments_wrapper_id': 'comments_1',
			'comments_class': 'letter_comment',
			'username': REG_USERNAME,
			'submit_id': 'LetterCommentForm_1_submit',
			'error_div_id': 'LetterCommentForm_1_text_errors',
			'error_text': 'This field is required.'
		}
		self.submit_blank_comment(**comment_form_spec)

	def question_comment(self):
		# choose a petition, go to its page
		question = Question.objects.get(pk=1)
		comment_form_spec = {
			'url': self.live_server_url + question.get_url(),
			'comment_class': QuestionComment,
			'comment_textarea_id': 'QuestionCommentForm_q_text',
			'toggler_id': '_w_toggle_hidden_comment_q',
			'comment_text': 'Test comment 3!',
			'comments_wrapper_id': 'comments_q',
			'comments_class': 'letter_comment',
			'username': REG_USERNAME,
			'submit_id': 'QuestionCommentForm_q_submit'
		}
		self.submit_comment(**comment_form_spec)

	def blank_question_comment(self):
		# choose a petition, go to its page
		question = Question.objects.get(pk=1)
		comment_form_spec = {
			'url': self.live_server_url + question.get_url(),
			'comment_class': QuestionComment,
			'comment_textarea_id': 'QuestionCommentForm_q_text',
			'toggler_id': '_w_toggle_hidden_comment_q',
			'comment_text': 'Test comment 3.5!',
			'comments_wrapper_id': 'comments_q',
			'comments_class': 'letter_comment',
			'username': REG_USERNAME,
			'submit_id': 'QuestionCommentForm_q_submit',
			'error_div_id': 'QuestionCommentForm_q_text_errors',
			'error_text': 'This field is required.'
		}
		self.submit_blank_comment(**comment_form_spec)

	def answer_comment(self):
		# choose a petition, go to its page
		question = Question.objects.get(pk=1)
		comment_form_spec = {
			'url': self.live_server_url + question.get_url(),
			'comment_class': AnswerComment,
			'comment_textarea_id': 'AnswerCommentForm_1_text',
			'toggler_id': '_w_toggle_hidden_comment_1',
			'comment_text': 'Test comment 4!',
			'comments_wrapper_id': 'comments_1',
			'comments_class': 'letter_comment',
			'username': REG_USERNAME,
			'submit_id': 'AnswerCommentForm_1_submit'
		}
		self.submit_comment(**comment_form_spec)

	def blank_answer_comment(self):
		# choose a petition, go to its page
		question = Question.objects.get(pk=1)
		comment_form_spec = {
			'url': self.live_server_url + question.get_url(),
			'comment_class': AnswerComment,
			'comment_textarea_id': 'AnswerCommentForm_1_text',
			'toggler_id': '_w_toggle_hidden_comment_1',
			'comment_text': 'Test comment 5!',
			'comments_wrapper_id': 'comments_1',
			'comments_class': 'letter_comment',
			'username': REG_USERNAME,
			'submit_id': 'AnswerCommentForm_1_submit',
			'error_div_id': 'AnswerCommentForm_1_text_errors',
			'error_text': 'This field is required.'
		}
		self.submit_blank_comment(**comment_form_spec)

	def answer_comment_2(self):
		# choose a petition, go to its page
		question = Question.objects.get(pk=1)
		comment_form_spec = {
			'url': self.live_server_url + question.get_url(),
			'comment_class': AnswerComment,
			'comment_textarea_id': 'AnswerCommentForm_2_text',
			'toggler_id': '_w_toggle_hidden_comment_2',
			'comment_text': 'Test comment 6!',
			'comments_wrapper_id': 'comments_2',
			'comments_class': 'letter_comment',
			'username': REG_USERNAME,
			'submit_id': 'AnswerCommentForm_2_submit'
		}
		self.submit_comment(**comment_form_spec)

	def blank_answer_comment_2(self):
		# choose a petition, go to its page
		question = Question.objects.get(pk=1)
		comment_form_spec = {
			'url': self.live_server_url + question.get_url(),
			'comment_class': AnswerComment,
			'comment_textarea_id': 'AnswerCommentForm_2_text',
			'toggler_id': '_w_toggle_hidden_comment_2',
			'comment_text': 'Test comment 7!',
			'comments_wrapper_id': 'comments_2',
			'comments_class': 'letter_comment',
			'username': REG_USERNAME,
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
		comment = comment_class.objects.get(text=comment_text)

		# Make sure the commenter was subscribed to her comment...
		user = User.objects.get(username=username)
		sub = Subscription.objects.get(
			user=user,
			reason="AUTHOR",
			subscription_id=comment.subscription_id
		)

		# ...and that she was subscribed to the thing she commented on
		sub = Subscription.objects.get(
			user=user,
			reason='COMMENTER',
			subscription_id=comment.target.subscription_id
		)

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

		# TODO: this is fragile.  It should be based on the actual 
		# answer objects...

		# make sure that all the answers showed up
		answers = Answer.objects.filter(target=question)
		answer_divs = self.driver.find_elements_by_class_name('subpost_body')
		self.assertEqual(len(answer_divs), answers.count())
		space_match = re.compile(r'\s')
		for i in range(len(answer_divs)):

			# Answer 42 got deleted from the test data.  
			# Witness the fragility! (see above TODO)
			if i==41:
				continue

			a, a_div = answers[i], answer_divs[i]
			self.assertEqual(
				space_match.sub('', a_div.text), 
				space_match.sub('', a.text)
			)
			self.driver.find_element('id', 'AnswerVoteForm_%d_upvote'%(i+1))
			self.driver.find_element('id', 'AnswerVoteForm_%d_score'%(i+1))
			self.driver.find_element('id', 'AnswerVoteForm_%d_downvote'%(i+1))
		


# Test submitting an answer using the answer form, and ensure that submitting
# a blank answer causes an error message to be shown.
#
class AnswerFormTest(SeleniumTestCase):

	def test_answer_form(self):

		# login regular user
		self.login_regularuser()

		# try submitting an answer.  Test that you can't submit blank answer
		self.submit_answer_subtest()
		self.submit_blank_answer_subtest()


	def submit_answer_subtest(self):
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

	def submit_blank_answer_subtest(self):
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
		self.assertTrue(
			self.wait.until(lambda driver:
				self.driver.find_element('id', answer_error_id).text
				== error_message
			)
		)

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



# Test adding a question.  Make sure that submitting an incomplete form causes
# an error message to be displayed.
#
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

	def test_question_form(self):

		# login a regular user
		self.login_regularuser()

		# test valid answer and incomplete answer submission
		self.submit_incomplete_question()
		self.submit_question()


	def submit_question(self):

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


	def submit_incomplete_question(self):
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


# Test editing proposals with the ProposalVersionForm.  Ensure that 
# incomplete forms cause an error to be shown, and that html special 
# characters get escaped.
#
class ProposalFormTest(FormTest):

	values = ['Test proposal title', 'This is only a test summary.',
				'This is only a test body.']
	form_data = {
		'ProposalVersionForm__title': {

			'value': values[0],
			'error_id': 'ProposalVersionForm__title_errors',
			'display_id': 'proposal_title',
			'expect': values[0]

		}, 'ProposalVersionForm__summary': {

			'value': values[1],
			'error_id': 'ProposalVersionForm__summary_errors',
			'display_id': 'proposal_summary',
			'expect': md.markdown(values[1])

		}, 'ProposalVersionForm__text': {

			'value': values[2], 
			'error_id': 'ProposalVersionForm__text_errors',
			'display_id': 'proposal_text',
			'expect': md.markdown(values[2])

		}
		
	}

	check_pk = True
	submit_id = 'ProposalVersionForm__submit'
	escape_text = '<&>'
	error_msg = 'This field is required.'
	error_class = 'field_wrapper_error'
	username = REG_USERNAME
	expect_proposal_id = 1

	REASON = 'EDITOR'
	EVENT_TYPE = 'EDIT_ISSUE'
	TEST_TAGS = 'tag1 tag2'
	PROPOSAL_TAGS_ID = 'proposal_tags'
	PROPOSAL_TAGS_CLASS = 'ui-widget-content'
	TAGS_ERROR_ID = 'proposal_tags_errors'
	TAGS_ERROR_MSG = 'Please include at least one tag.'

	def test_edit_proposal(self):

		self.login_regularuser()

		expected_id = self.expect_proposal_id()

		# Go to the edit page for a test proposal
		self.driver.get(self.get_url())

		# Fill and submit the form with valid data
		self.fill_form(self.form_data)
		self.driver.find_element(
			'id', 'proposal_tags_input').find_element_by_class_name(
			self.PROPOSAL_TAGS_CLASS).send_keys(self.TEST_TAGS)

		self.click('ProposalVersionForm__sectors_1')
		self.click('ProposalVersionForm__sectors_5')
		self.driver.find_element('id', self.submit_id).click()

		# check that the proposal was correctly loaded
		expect_data = dict([
			(v['display_id'], v['expect']) for v in self.form_data.values()
		])
		self.assertTrue(self.elements_contain(expect_data))

		# check the database
		sectors = [
			Sector.objects.get(name='environment'),
			Sector.objects.get(name='culture')
		]
		self.check_db(
			expected_id, *self.values, username=self.username,
			tags=self.TEST_TAGS, sectors=sectors, 
			event_type=self.EVENT_TYPE
		)


	# TODO: This should check the case where user has not entered any tags
	def test_edit_proposal_incomplete(self):

		self.login_regularuser()

		# Go to the edit page for a test proposal
		self.driver.get(self.get_url())

		# we'll submit the form several times, 
		# each time ommitting a different field
		for ommitted_id, spec in self.form_data.items():

			error_id = spec['error_id']

			self.fill_form(self.form_data, clear=ommitted_id)

			# clear existing tags, and insert specified ones
			self.driver.find_element(
				'id', 'proposal_tags_input').find_element_by_class_name(
				self.PROPOSAL_TAGS_CLASS).send_keys('\b'*5 + self.TEST_TAGS)

			self.click('ProposalVersionForm__sectors_1')
			self.click('ProposalVersionForm__sectors_5')
			self.click(self.submit_id)

			# Check for the error message
			self.assertTrue(self.element_contains(error_id, self.error_msg,
				use_html=False))

			# Check that the input was styled with an error styling
			ommitted_elm = self.driver.find_element('id', ommitted_id)
			wrapper = ommitted_elm.find_element_by_xpath('..')
			self.assertTrue(
				self.error_class in wrapper.get_attribute('class'))


		# Now Check that not submitting tags raises a user-facing error
		# Fill out the form, but omit tags.
		self.fill_form(self.form_data, clear=ommitted_id)

		self.driver.find_element(
			'id', 'proposal_tags_input').find_element_by_class_name(
			self.PROPOSAL_TAGS_CLASS).send_keys('\b'*5)

		self.click('ProposalVersionForm__sectors_1')
		self.click('ProposalVersionForm__sectors_5')
		self.click(self.submit_id)

		# check for the user-facing error
		self.assertTrue(
			self.element_contains(self.TAGS_ERROR_ID, self.TAGS_ERROR_MSG))

		# Check that the tagit elment got styled up with error class
		ommitted_elm = self.driver.find_element('id', self.PROPOSAL_TAGS_ID)
		wrapper = ommitted_elm.find_element_by_xpath('..')
		self.assertTrue(
			self.error_class in wrapper.get_attribute('class'))


	def test_edit_proposal_ensure_escape(self):
		self.login_regularuser()

		expected_id = self.expect_proposal_id()

		form_data_needs_escape = dict([
			(k, self.escape_text) for k in self.form_data.keys()])

		expect_escaped_data = {
			'proposal_title': escape(self.escape_text),
			'proposal_summary': md.markdown(escape(self.escape_text)),
			'proposal_text': md.markdown(escape(self.escape_text))
		}

		# Go to the edit page for a test proposal
		self.driver.get(self.get_url())

		# Fill and submit the form with data that should get escaped
		self.fill_form(form_data_needs_escape)

		self.driver.find_element(
			'id', 'proposal_tags_input').find_element_by_class_name(
			self.PROPOSAL_TAGS_CLASS).send_keys(self.TEST_TAGS)

		self.click('ProposalVersionForm__sectors_1')
		self.click('ProposalVersionForm__sectors_5')
		self.driver.find_element('id', self.submit_id).click()


		# check that the proposal was correctly loaded
		self.assertTrue(self.elements_contain(expect_escaped_data))

		# check the database
		sectors = [
			Sector.objects.get(name='environment'),
			Sector.objects.get(name='culture')
		]
		self.check_db(expected_id, self.escape_text, 
			self.escape_text, self.escape_text, self.username, 
				self.TEST_TAGS, sectors, self.EVENT_TYPE)

	def get_url(self):
		return (self.live_server_url 
			+ Proposal.objects.get(pk=self.expect_proposal_id).get_edit_url())


	def expect_proposal_id(self):
		return 1


	def check_db(
			self, 
			expected_id, 
			title, 
			summary, 
			text, 
			username, 
			tags, 
			sectors,
			event_type
		):

		proposal = Proposal.objects.get(title=title)
		user = User.objects.get(username=username)

		# this switch is used to turn of checking the primary key for
		# the AddProposalTest, which inherits from this test
		if self.check_pk:
			self.assertEqual(expected_id, proposal.pk)

		self.assertEqual(summary, proposal.summary)
		self.assertEqual(text, proposal.text)
		self.assertEqual(username, proposal.user.username)

		proposal_version = proposal.get_latest()
		self.assertEqual(title, proposal_version.title)
		self.assertEqual(summary, proposal_version.summary)
		self.assertEqual(text, proposal_version.text)
		self.assertEqual(username, proposal_version.user.username)

		# Check if a Subscription was made
		sub_id = proposal.subscription_id
		s = Subscription.objects.get(subscription_id=sub_id, user=user, 
			reason=self.REASON)

		# check if a publication was made against the proposal
		p = Publication.objects.get(
			subscription_id=proposal.subscription_id,
			source_user=user,
			event_type=event_type
		)
		self.assertEqual(p.was_posted, False)
		self.assertEqual(p.event_data, proposal.text[:100])
		self.assertEqual(p.link_back, 
			proposal.get_url_by_view_name('proposal'))

		# Check if a Publication was made against the tags
		tag_names = tags.split()
		tag_objects = [
			Tag.objects.get(name=tag_names[0]),
			Tag.objects.get(name=tag_names[1])
		]

		for tag in tag_objects:

			p = Publication.objects.get(
				subscription_id=tag.subscription_id,
				source_user=user,
				event_type=event_type
			)
			self.assertEqual(p.was_posted, False)
			self.assertEqual(p.event_data, proposal.text[:100])
			self.assertEqual(p.link_back, 
				proposal.get_url_by_view_name('proposal'))

		for sector in sectors:
			# Check if a Publication was made against the sector
			p = Publication.objects.get(
				subscription_id=sector.subscription_id)
			self.assertEqual(p.source_user, user)
			self.assertEqual(p.event_type, event_type)
			self.assertEqual(p.was_posted, False)
			self.assertEqual(p.event_data, proposal.text[:100])
			self.assertEqual(p.link_back, 
				proposal.get_url_by_view_name('proposal'))


class AddProposalTest(ProposalFormTest):

	check_pk = False
	REASON = 'AUTHOR'
	EVENT_TYPE = 'ISSUE'

	def get_url(self):
		return self.live_server_url + reverse('add_proposal')

	def expect_proposal_id(self):
		return Proposal.objects.all().count() + 1



class VoteTest(SeleniumTestCase):

	up_on_class = 'upvote_on'
	down_on_class = 'downvote_on'


	def test_all_votes(self):
		self.login_regularuser()

		self.QuestionVote()
		self.AnswerVote()
		# self.NewAnswerVote()
		self.DiscussionVote()
		self.ReplyVote()
		# self.NewReplyVote()


	def QuestionVote(self):
		url = self.live_server_url + Question.objects.get(pk=2).get_url()
		vote_spec = {
			'up_id': 'QuestionVoteForm_q_upvote',
			'score_id': 'QuestionVoteForm_q_score',
			'down_id': 'QuestionVoteForm_q_downvote',
			'url': url
		}

		self.vote_test(**vote_spec)


	def AnswerVote(self):
		url = self.live_server_url + Question.objects.get(pk=1).get_url()
		vote_spec = {
			'up_id': 'AnswerVoteForm_2_upvote',
			'score_id': 'AnswerVoteForm_2_score',
			'down_id': 'AnswerVoteForm_2_downvote',
			'url': url
		}

		self.vote_test(**vote_spec)


	# Can't do new-answer vote, because a user cannot vote on their own
	# answer.  However, this used to work before user authentication
	# was added.
	def NewAnswerVote(self):
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


	def DiscussionVote(self):
		url = self.live_server_url + Discussion.objects.get(pk=2).get_url()
		vote_spec = {
			'up_id': 'DiscussionVoteForm_q_upvote',
			'score_id': 'DiscussionVoteForm_q_score',
			'down_id': 'DiscussionVoteForm_q_downvote',
			'url': url
		}

		self.vote_test(**vote_spec)


	def ReplyVote(self):
		url = self.live_server_url + Discussion.objects.get(pk=1).get_url()
		vote_spec = {
			'up_id': 'ReplyVoteForm_26_upvote',
			'score_id': 'ReplyVoteForm_26_score',
			'down_id': 'ReplyVoteForm_26_downvote',
			'url': url
		}

		self.vote_test(**vote_spec)


	# Can't do new-reply vote, because a user cannot vote on their own
	# answer.  However, this used to work before user authentication
	# was added.
	def NewReplyVote(self):
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



class TestLoginRequired(TestCase):
	'''
	Attempts to perform requests and POSTs that require login, without
	actually logging in, and verifies that these do not work.
	'''

	# This is a list of views that require logins to respond to a get request
	# They will be accessed by get request.  Each is a tuple, where the first
	# elment is a view's name (i.e. third argument in urls.py), and the 
	# second is a dictionary of keyword arguments.  (positional arguments 
	# aren't supported right now because we don't use them.
	login_get_views = [
		('add_proposal',{}),
		('start_discussion', {'target_id': 1}),

	]

	# lists views that should require login, which is to be tested.
	# Each view is specified by a triple
	# 	1) views name
	#	2) keyword dictionary associated to url (reverse url resolution)
	#	3) dictionary of post data
	# 
	login_post_views = [
		('ask_question', {'target_id':1}, 
			{'title': 'Test title', 'text': 'Test text', 
				'user':1, 'target':1}, Question
		),
		('start_discussion', {'target_id':1}, 
			{'title': 'Test title', 'text': 'Test text', 
				'user':1, 'target':1}, Discussion
		),

		('start_petition', {'target_id':1}, 
			{
				'title': 'Test petitien title',
				'text': 'Test text', 
				'user':1,
				'target':1,
				'valence': 1,
				'recipients': 1
			}, 
			Letter
		),

		('add_proposal', {}, 
			{
				'title': 'Test title', 
				'summary': 'test summary',
				'text': 'Test proposal text', 
				'user': 1, 
				'tags': 'tag1,tag2'
			},
			Proposal
		),

		('edit', {'issue_id':1}, 
			{
				'title': 'Test title edited', 
				'summary': 'test summary',
				'text': 'Test proposal text', 
				'user': 1, 
				'tags': 'tag1,tag2'
			},
			Proposal
		),
	]

	ajax_posts = [
		# votes
		('vote_answer', {'valence':1, 'user':1, 'target':1}, AnswerVote),
		('vote_question', {'valence':1, 'user':1, 'target':1}, QuestionVote),
		('vote_discussion', {'valence':1, 'user':1, 'target':1}, 
			DiscussionVote),
		('vote_proposal', {'valence':1, 'user':1, 'target':1}, ProposalVote),
		('vote_letter', {'valence':1, 'user':1, 'target':1}, LetterVote),
		('vote_reply', {'valence':1, 'user':1, 'target':39}, ReplyVote),

		# Comments
		('answer_comment', {'text':'Test comment', 'user':1, 'target':1},
			AnswerComment),
		('question_comment', {'text':'Test comment', 'user':1, 'target':1},
			QuestionComment),
		('comment', {'text':'Test comment', 'user':1, 'target':1},
			Comment),
		('reply_comment', {'text':'Test comment', 'user':1, 'target':39},
			ReplyComment),
		('discussion_comment', {'text':'Test comment', 'user':1, 'target':1},
			DiscussionComment),
		
		# subposts
		('answer', {'text':'Test answer', 'user':1, 'target':1}, Answer),
		('reply', {'text':'Test reply', 'user':1, 'target':1}, Reply),

		# petitions
		('send_letter', 
			{
				'text': 'Test letter',
				'user':1,
				'target':1,
				'title':'Test letter title',
				'valence': 1,
				'recipients': 1
			},
			Letter
		),
		('resend_letter', 
			{
				'parent_letter': 1,
				'text': 'Test signing letter',
				'user': 1,
				'target': 1,
				'title':'Test letter title',
				'valence': -1,
				'recipients': 1
			},
			Letter
		),

	]

	def test_post_views(self):

		# if we don't login posts will cause redirection to the login page
		for view_name, kwargs, post_data, post_class in self.login_post_views:
			url = reverse(view_name, kwargs=kwargs)
			response = self.client.post(url, post_data, follow=True)

			# check that we were redirected to the login page
			self.assert_was_redirected_to_login(response)

			# this function tries to retrieve the object we posted 
			def func():
				post_class.objects.get(title=post_data['title'])

			# since posting should have failed, the object should not exist
			self.assertRaises(post_class.DoesNotExist, func)


		# this time we'll login before posting, but the logged in user
		# won't match the user indicated in the form, so we'll still get
		# redirected to the login page
		for view_name, kwargs, post_data, post_class in self.login_post_views:

			if 'user' in post_data:

				self.client.login(
					username='regularuser', password='regularuser')

				# ensure that we have posted {user:1}, to be sure that we
				# correctly test that the logged in user matches the posted 
				# user
				self.assertTrue(post_data['user']==1,
					"In the post_data you need to set the user to be 1 so "
					"that identity matching can be tested!")

				url = reverse(view_name, kwargs=kwargs)
				response = self.client.post(url, post_data, follow=True)

				# verify we got redirected
				self.assert_was_redirected_to_login(response)

				# this function tries to retrieve the object we posted 
				def func():
					post_class.objects.get(title=post_data['title'])

				# since posting would have failed, the object should not exist
				self.assertRaises(post_class.DoesNotExist, func)

		# This time we'll login as the same user that is posted in the
		# form, so the post should be successful.  We will not be sent
		# to the login page, and the object will be added to the database.
		for view_name, kwargs, post_data, post_class in self.login_post_views:

			self.client.login(
				username='superuser', password='superuser')

			url = reverse(view_name, kwargs=kwargs)
			response = self.client.post(url, post_data, follow=True)

			# verify we got redirected
			self.assert_was_not_redirected_to_login(response)

			# this function tries to retrieve the object we posted 
			def func():
				post_class.objects.get(title=post_data['title'])

			# since posting would have failed, the object should not exist
			self.assertEqual(
				post_class.objects.filter(title=post_data['title']).count(),
				1
			)


	def test_get_login_required(self):
		for view_name, kwargs in self.login_get_views:
			url = reverse(view_name, kwargs=kwargs)
			response = self.client.get(url, follow=True)
			self.assert_was_redirected_to_login(response)


	def test_ajax_login_required(self):

		# first attempt all the posts without having logged in.
		# They should all get denied.
		for endpoint, post_data, post_class in self.ajax_posts:
			url = reverse('handle_ajax_json', kwargs={'view':endpoint})
			response = self.client.post(url, post_data)
			self.assert_ajax_post_denied(response, endpoint)

			# since the post failed, we can't find the object in the database
			self.assertEqual(
				post_class.objects.filter(**post_data).count(), 0)


		# TODO: show that attempt to retrieve from db gives DoesNotExist

		# Now attempt any posts that had a user field.  This time, login
		# but login as a different user than what is posted in the user field
		for endpoint, post_data, post_class in self.ajax_posts:

			# This part of the test only applies when the post data contains
			# a 'user' field.
			if 'user' in post_data:

				# Login as user 2
				self.client.login(
					username='regularuser', password='regularuser')

				# ensure that we have posted {user:1}, to be sure that we
				# correctly test that the logged in user matches the posted 
				# user
				self.assertTrue(post_data['user']==1,
					"In the post_data you need to set the user to be 1 so "
					"that identity matching can be tested!")

				url = reverse('handle_ajax_json', kwargs={'view':endpoint})
				response = self.client.post(url, post_data)
				self.assert_caught_non_matching_user(response)

				# since the post failed, the object is not in the database
				self.assertEqual(
					post_class.objects.filter(**post_data).count(), 0)

		# logout regular user
		self.client.logout()

		# Now attempt all the posts again, and this time they should get
		# accepted.  Any posts that have a user field (which is equal to
		# 1) will now match the logged in user.
		for endpoint, post_data, post_class in self.ajax_posts:

			# Login as user 1
			self.client.login(username='superuser', password='superuser')

			url = reverse('handle_ajax_json', kwargs={'view':endpoint})
			response = self.client.post(url, post_data)
			self.assert_ajax_post_accepted(response, endpoint)

			# since the post was accepted, we should find object in database
			self.assertEqual(
				post_class.objects.filter(**post_data).count(), 1,
				'the post wasn\'t loaded via %s' % endpoint)



	def assert_was_not_redirected_to_login(self, request):
		self.assertFalse(
			reverse('login_required') in request.redirect_chain[-1][0])

	def assert_was_redirected_to_login(self, request):
		self.assertTrue(
			reverse('login_required') in request.redirect_chain[-1][0])


	def assert_ajax_post_accepted(self, response, endpoint):
		reply_data = json.loads(response.content)
		self.assertTrue(reply_data['success'],
			('post to %s should have been accepted... ' %endpoint) + reply_data.pop('msg','') + str(reply_data.pop('errors','')))


	def assert_caught_non_matching_user(self, repsonse):
		# the response is JSON formatted
		reply_data = json.loads(repsonse.content)

		# assert that the reply was denied, and the reason was a lack of
		# authentication
		self.assertFalse(reply_data['success'])
		self.assertEqual(reply_data['msg'], "authenticated user did not "
			"match the user that requested the form")


	def assert_ajax_post_denied(self, response, endpoint):
		# the response is JSON formatted
		reply_data = json.loads(response.content)

		# assert that the reply was denied, and the reason was a lack of
		# authentication
		self.assertFalse(reply_data['success'], 'the post to %s should '
			'have been denied.' % endpoint)
		self.assertEqual(reply_data['msg'], "user did not authenticate")


class PublishSubscribeTest(TestCase):
	'''
		Tests that creating various subscribable objects always leads 
		to two things:
		1) The author is subscribed to the created object
		2) A Publication is isued against target objects.  For example,
			if a Question is being posted within a certain Proposal, then 
			a Publication shoulid be issued for that Proposal, so that
			any users subscribed to the Proposal will be notified of the 
			new Question

		For most kinds of subsrcibable objects, the tests that need to
		be run are pretty formulaic.  So, a helper function, 
		do_subscribable_test, is used.  The tests that match this formula
		can be defined by a few args passed into do_subscribable_test.
		That goes for testing questions, comments, letters, etc.

		But testing Proposals is a bit more complex so it is done in its
		own test routine, different from do_subscribable_test.
	'''

	# TODO: implement these three tests



	def test_sign_letter(self):
		pass

	def test_all_votes(self):
		pass

	def test_proposal(self):

		# get a few ingredients together so we can make a proposal
		proposal_author = User.objects.get(username='regularuser')
		tag = Tag.objects.get(pk=1)
		sector = Sector.objects.get(pk=1)

		# make a proposal
		proposal = Proposal(
			title='test proposal 1', 
			summary='test proposal 1',
			text='test proposal 1',
			original_user=proposal_author,
			user=proposal_author
		)
		proposal.save(suppress_subscribe=True, suppress_publish=True)
		proposal.tags.add(tag)
		proposal.sectors.add(sector)
		proposal.publish(event_type='ISSUE')
		proposal.subscribe(reason='AUTHOR')

		# make an associated proposal version
		proposal_version = ProposalVersion(
			proposal=proposal,
			title='test proposal 1', 
			summary='test proposal 1',
			text='test proposal 1',
			user=proposal_author
		)
		proposal_version.save()
		proposal_version.tags.add(tag)
		proposal_version.sectors.add(sector)
		proposal_version.save()

		# Check if a Subscription was made
		sub_id = proposal.subscription_id
		s = Subscription.objects.get(subscription_id=sub_id)
		self.assertEqual(s.user, proposal_author)

		# Check if a Pubscription was made against the Proposal
		p = Publication.objects.get(subscription_id=proposal.subscription_id)
		self.assertEqual(p.source_user, proposal_author)
		self.assertEqual(p.event_type, 'ISSUE')
		self.assertEqual(p.was_posted, False)
		self.assertEqual(p.event_data, proposal.text[:100])
		self.assertEqual(p.link_back, 
			proposal.get_url_by_view_name('proposal'))


		# Check if a Publication was made against the tag
		p = Publication.objects.get(subscription_id=tag.subscription_id)
		self.assertEqual(p.source_user, proposal_author)
		self.assertEqual(p.event_type, 'ISSUE')
		self.assertEqual(p.was_posted, False)
		self.assertEqual(p.event_data, proposal.text[:100])
		self.assertEqual(p.link_back, 
			proposal.get_url_by_view_name('proposal'))

		# Check if a Publication was made against the sector
		p = Publication.objects.get(subscription_id=sector.subscription_id)
		self.assertEqual(p.source_user, proposal_author)
		self.assertEqual(p.event_type, 'ISSUE')
		self.assertEqual(p.was_posted, False)
		self.assertEqual(p.event_data, proposal.text[:100])
		self.assertEqual(p.link_back, 
			proposal.get_url_by_view_name('proposal'))


	def test_question(self):
		proposal = Proposal.objects.get(pk=1)
		question_author = User.objects.get(username='superuser')
		title = 'Question about publications'
		text = 'Hey, will this trigger a publication like it should?'
		self.do_subscribable_test(
			proposal,
			Question,
			{
				'title': title,
				'text': text,
			},
			question_author,
			'QUESTION',
			text[:100]
		)


	def test_letter(self):
		author = User.objects.get(username='superuser')
		title = 'A tesnt post'
		text = 'Hey, will this trigger a publication like it should?'
		valence = '1'
		proposal = Proposal.objects.get(pk=1)
		self.do_subscribable_test(
			proposal,
			Letter,
			{
				'title': title,
				'text': text,
				'valence': valence
			},
			author,
			'LETTER',
			text[:100]
		)


	def test_untitled_posts(self):
		classes = [
			(Question, Answer, 'ANSWER'),
			(Discussion, Reply, 'REPLY')
		]

		author = User.objects.get(username='superuser')
		text = 'Hey, will this trigger a publication like it should?'
		for target_class, notifier_class, event_type in classes:
			target = target_class.objects.get(pk=1)
			self.do_subscribable_test(
				target,
				notifier_class,
				{
					'text': text,
				},
				author,
				event_type,
				text[:100]
			)
				

	def test_titled_posts(self):
		classes = [
			(Proposal, Question, 'QUESTION'),
			(Proposal, Discussion, 'DISCUSSION')
		]

		author = User.objects.get(username='superuser')
		title = 'A tesnt post'
		text = 'Hey, will this trigger a publication like it should?'
		for target_class, notifier_class, event_type in classes:
			target = target_class.objects.get(pk=1)
			self.do_subscribable_test(
				target,
				notifier_class,
				{
					'title': title,
					'text': text,
				},
				author,
				event_type,
				text[:100]
			)


	def test_all_comments(self):
		classes = [
			(Question, QuestionComment),
			(Answer, AnswerComment),
			(Discussion, DiscussionComment),
			(Reply, ReplyComment),
			(Letter, Comment)
		]

		comment_author = User.objects.get(username='regularuser')
		for target_class, comment_class in classes:
			target = target_class.objects.get(pk=1)
			text = 'Yo this is a test comment!'
			self.do_subscribable_test(
				target,
				comment_class,
				{
					'text':text,
				},
				comment_author,
				'COMMENT',
				text[:100]
			)


	def do_subscribable_test(
			self, 
			target, 
			subscribable_class, 
			subscribable_constructor_args,
			subscribable_author,
			event_type,
			event_data,
		):

		# Now create a subscribable associated to the target
		subscribable_constructor_args['target'] = target
		subscribable_constructor_args['user'] = subscribable_author
		subscribable = subscribable_class(**subscribable_constructor_args)
		subscribable.save()

		# Check if a Subscription was made
		sub_id = subscribable.subscription_id
		s = Subscription.objects.get(subscription_id=sub_id)
		self.assertEqual(s.user, subscribable_author)

		# Check for a Publication of the Subscribable against the Target
		p = Publication.objects.get(
			subscription_id=target.subscription_id,
			source_user=subscribable_author,
			event_type=event_type,
			was_posted=False,
			event_data=event_data,
			link_back=subscribable.get_url()
		)






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


