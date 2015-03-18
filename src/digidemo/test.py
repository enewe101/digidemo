# TODO: remove classmethod decorators from SeleniumTestCase

import filecmp
import os
import json
import time
import copy
import unittest
from urlparse import urljoin

from django.core.urlresolvers import reverse
from django.core.files import File
from django.core import mail
from django.test import TestCase, LiveServerTestCase
from django.utils.html import escape

from digidemo import settings, markdown as md
from digidemo.models import *
from digidemo.abstract_models import *
from digidemo.views import get_notification_message
from digidemo.shortcuts import get_profile, url_patch_lang

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

#def patch_broken_pipe_error():
#    """Monkey Patch BaseServer.handle_error to not write
#    a stacktrace to stderr on broken pipe.
#    http://stackoverflow.com/a/7913160"""
#    import sys
#    from SocketServer import BaseServer
#
#    handle_error = BaseServer.handle_error
#
#    def my_handle_error(self, request, client_address):
#        type, err, tb = sys.exc_info()
#        # there might be better ways to detect the specific erro
#        if repr(err) == "error(32, 'Broken pipe')":
#            # you may ignore it...
#            logging.getLogger('mylog').warn(err)
#        else:
#            handle_error(self, request, client_address)
#
#    BaseServer.handle_error = my_handle_error
#
#
#patch_broken_pipe_error()


REG_USERNAME = 'regularuser'

class FixtureLoadedTestCase(TestCase):
	fixtures = ['test_data']


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

	fixtures = ['test_data']

	LIVE_SERVER_URL = 'localhost:8081'

	@classmethod
	def setUpClass(cls):
		cls.driver = webdriver.Firefox()
		#cls.driver = webdriver.PhantomJS()
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

	# Find the element based on html id attribute
	#
	@classmethod
	def full_url(cls, url_without_domain):

		base_url = 'http://' + cls.get_live_server_url()
		full_url = urljoin(base_url, url_without_domain)

		return full_url

	# go to a url under the luminocracy domain.  The passed url should 
	# not have the domain, e.g., should be like those returned by reverse()
	#
	@classmethod
	def go(cls, url_without_domain):
		'''
			using a url without a domain, and an optional language code
			constructs the full url.  If no language code is specified, 
			english will be forced.
		'''

		full_url = cls.full_url(url_without_domain)
		cls.driver.get(full_url)


	# Checks that an element with a given id *does not exist* on the page
	#
	def assertNotFound(self, element_id):

		def func():
			self.find(element_id)

		self.assertRaises(NoSuchElementException, func)


	# Click the element. Just a convinience method. 
	#
	@classmethod
	def click(cls, element_id):
		cls.driver.find_element('id', element_id).click()

	# Find the element based on html id attribute
	#
	@classmethod
	def find(cls, element_id):
		return cls.driver.find_element('id', element_id)

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


	# login as a user whose email has not yet been validated
	# 
	@classmethod
	def login_notvalidateduser(cls):
		cls.login('notvalidated', 'notvalidated')


	# login as a super user (is_staff == True; is_superuser == True)
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


	def logout(cls):
		# click the avatar
		cls.click('logged_in_div')
		cls.click('logout')
	
		
class RegistrationFormTest(SeleniumTestCase):

	def test_client_side(self):
		pass



class EmailValidation(SeleniumTestCase):

	def test_email_validated(self):

		'''
			Checks that, when a new user signs up:

				- initially their email is not validated
				- they get sent an email to confirm their email address
				- when their email is not validated, they are forwarded
					to the invalid_email page
				- they can resend the email confirmation mail from the 
					invalid email page
				- following the link in the email confirmation page makes 
					their email validated
				- loging in with a valid email forwards to the home page
		'''

		# register a new user
		self.driver.get(self.live_server_url + reverse('userRegistration'))
		self.puts({
			'UserRegisterForm__first_name': 'new',
			'UserRegisterForm__last_name': 'user',
			'UserRegisterForm__username': 'newuser',
			'UserRegisterForm__email': 'newuser@example.com',
			'UserRegisterForm__password': 'password',
			'UserRegisterForm__confirm_password': 'password',
		})
		self.click('UserRegisterForm__submit')

		# verify that the new user's email isn't validated
		user = User.objects.get(username='newuser')
		user_profile = get_profile(user)
		self.assertFalse(user_profile.email_validated)

		# verify that an entry was made into the EmailVerification table
		verification = EmailVerification.objects.get(user=user)

		# check whether a confirmation email was sent to the user
		self.assertEqual(len(mail.outbox),1)
		sent_mail = mail.outbox[0]
		self.assertEqual(sent_mail.subject, 'Welcome to luminocracy')
		self.assertEqual(sent_mail.to, ['newuser@example.com'])

		email_link = reverse(
			'verify_email', kwargs={'code': verification.code})

		body = (
			'To verify your account, click this link: https://luminocracy.org'
			+ email_link
		)
		self.assertEqual(sent_mail.body, body)

		# try logging in without validating email
		self.driver.get(self.live_server_url + reverse('login_required'))
		self.puts({
			'LoginForm__username': 'newuser',
			'LoginForm__password': 'password'
		})
		self.click('LoginForm__submit')
		self.assertEqual(
			self.driver.current_url,
			self.live_server_url + reverse('invalid_email')
		)

		# try clicking the resend email link
		self.click('resend_link')

		# check that we wound up at the send email page
		message_text = self.find('mail_sent_message').text
		expected_message_text = (
			'Nice! Check your mail for a link to confirm registration.')
		self.assertTrue(text_is_similar(message_text, expected_message_text))

		# check that another email was sent
		self.assertEqual(len(mail.outbox), 2)
		sent_mail = mail.outbox[1]
		self.assertEqual(sent_mail.subject, 'Welcome to luminocracy')
		self.assertEqual(sent_mail.to, ['newuser@example.com'])

		body = (
			'To verify your account, click this link: https://luminocracy.org'
			+ email_link
		)
		self.assertEqual(sent_mail.body, body)
		
		# simulate following the link in the email 
		self.driver.get(self.live_server_url + email_link)
		message_text = self.find('exclamation').text
		expected_message_text = 'Good to go!'
		self.assertTrue(text_is_similar(message_text, expected_message_text))

		# now check that the user's email has been verified
		user_profile = get_profile(user)
		self.assertTrue(user_profile.email_validated)

		# now try logging in, and check that user is sent to home page
		self.driver.get(self.live_server_url + reverse('login_required'))
		self.puts({
			'LoginForm__username': 'newuser',
			'LoginForm__password': 'password'
		})
		self.click('LoginForm__submit')
		self.assertEqual(
			self.driver.current_url,
			self.live_server_url + reverse('index')
		)








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
			'comment_textarea_id': 'AnswerCommentForm_3_text',
			'toggler_id': '_w_toggle_hidden_comment_3',
			'comment_text': 'Test comment 6!',
			'comments_wrapper_id': 'comments_3',
			'comments_class': 'letter_comment',
			'username': REG_USERNAME,
			'submit_id': 'AnswerCommentForm_3_submit'
		}
		self.submit_comment(**comment_form_spec)

	def blank_answer_comment_2(self):
		# choose a petition, go to its page
		question = Question.objects.get(pk=1)
		comment_form_spec = {
			'url': self.live_server_url + question.get_url(),
			'comment_class': AnswerComment,
			'comment_textarea_id': 'AnswerCommentForm_3_text',
			'toggler_id': '_w_toggle_hidden_comment_3',
			'comment_text': 'Test comment 7!',
			'comments_wrapper_id': 'comments_3',
			'comments_class': 'letter_comment',
			'username': REG_USERNAME,
			'submit_id': 'AnswerCommentForm_3_submit',
			'error_div_id': 'AnswerCommentForm_3_text_errors',
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

		# TODO: restore publish-subscribe testing after changes to 
		# publish-subscribe system have been made

		# ...and that she was subscribed to the thing she commented on
		#sub = Subscription.objects.get(
		#	user=user,
		#	reason='COMMENTER',
		#	subscription_id=comment.target.subscription_id
		#)

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
		self.assertTrue(text_is_similar(title.text, question.title))
		body = self.driver.find_element_by_class_name('post_body')
		self.assertTrue(text_is_similar(body.text, question.text))

		# TODO: this is fragile.  It should be based on the actual 
		# answer objects...

		# make sure that all the answers showed up
		answers = Answer.objects.filter(target=question).order_by('pk')
		answer_divs = self.driver.find_elements_by_class_name('subpost_body')
		self.assertEqual(len(answer_divs), answers.count())
		space_match = re.compile(r'\s')
		for i in range(len(answer_divs)):

			a, a_div = answers[i], answer_divs[i]
			self.assertEqual(
				space_match.sub('', a_div.text), 
				space_match.sub('', a.text)
			)

			pk = a.pk

			self.driver.find_element('id', 'AnswerVoteForm_%d_upvote'%(pk))
			self.driver.find_element('id', 'AnswerVoteForm_%d_score'%(pk))
			self.driver.find_element(
				'id', 'AnswerVoteForm_%d_downvote'%(pk))
		


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


# Test adding a discussion 
#
class AddDiscussionTest(SeleniumTestCase):
	'''
		Tests adding a discussion using the add discussion form.
		Ensures that added discussions display correctly.  Tests that 
		submitting an incomplete form triggers errors.
	'''

	TITLE = 'Test Discussion'
	TEXT = 'Charlie Brown, why do you test my patience?'
	ERROR = 'This field is required.'  
	
	def test_add_complete_discussion(self):
		'''
			Tests adding a discussion.  Ensures the discussion displays
			correctly after adding it, and that it is included in the 
			discussion list view for the proposal.
		'''

		# login a regular user
		self.login_regularuser()
		user = User.objects.get(username='regularuser')

		# visit the edit/discussion page for a proposal
		proposal = Proposal.objects.get(pk=1)
		url = self.live_server_url + proposal.get_start_discussion_url()
		self.driver.get(url)

		# use webdriver commands to insert the test discussion's title
		title_input_id = 'DiscussionForm__title'
		self.driver.find_element('id', title_input_id).send_keys(self.TITLE)

		# do similarly to insert the discussion text. 
		text_input_id = 'DiscussionForm__text'
		self.driver.find_element('id', text_input_id).send_keys(self.TEXT)

		# now click the form's submit button 
		submit_button_id = 'DiscussionForm__submit'
		self.driver.find_element('id', submit_button_id).click()

		# Check that the discussion was added to the database
		d = Discussion.objects.get(
			target=proposal,
			title=self.TITLE,
			text=self.TEXT,
			user=user,
			is_open=True
		)

		# get the ID, which is used to find the discussion within the
		# discussion list
		discussion_id = d.pk

		# check that the discussion displays correctly on the page.  Look
		# for the display of the title and text
		post_title_id = 'post__title'
		self.assertTrue(
			self.wait.until(lambda driver:
				self.driver.find_element('id', post_title_id).text
				== self.TITLE
			)
		)

		# do a similar check for the display of the discussion body text
		post_body_id = 'post__body'
		self.assertTrue(
			self.wait.until(lambda driver:
				self.driver.find_element('id', post_body_id).text
				== self.TEXT
			)
		)

		# now navigate to the discussion list view and check that the new
		# discussion also displays in the list

		# visit the edit/discussion page for a proposal
		proposal = Proposal.objects.get(pk=1)
		url = self.live_server_url + proposal.get_open_discussions_url()
		self.driver.get(url)

		# find the appropriate html element, and ensure that it has the
		# right content in it
		discussion_title_id = "discussion_title_%d" % discussion_id
		self.assertTrue(
			self.wait.until(lambda driver:
				text_is_similar(
					self.driver.find_element('id', discussion_title_id).text,
					self.TITLE
				)
			)
		)

		# do a similar check for the display of the discussion body text
		discussion_text_id = "discussion_text_%d" % discussion_id
		self.assertTrue(
			self.wait.until(lambda driver:
				text_is_similar(
					self.driver.find_element('id', discussion_text_id).text,
					self.TEXT
				)
			)
		)


	def test_add_incomplete_discussion(self):
		'''
			Tests error messaging when a discussion is added incorrectly.  
		'''

		# login a regular user
		self.login_regularuser()

		# visit the edit/discussion page for a proposal
		proposal = Proposal.objects.get(pk=1)
		url = self.live_server_url + proposal.get_start_discussion_url()
		self.driver.get(url)

		# Leave the test discussion's title blank
		title_input_id = 'DiscussionForm__title'
		self.driver.find_element('id', title_input_id).send_keys('')

		# do similarly to insert the discussion text. 
		text_input_id = 'DiscussionForm__text'
		self.driver.find_element('id', text_input_id).send_keys(self.TEXT)

		# now click the form's submit button 
		submit_button_id = 'DiscussionForm__submit'
		self.driver.find_element('id', submit_button_id).click()

		# use webdriver commands to insert text into the form and submit it
		# just like above.  Except leave the title blank!

		# An error message should be displayed
		# note -- you'll need to set the TITLE_ERROR to be what it actually
		# is (TITLE_ERROR is a class attribute defined above just inside the
		# start of this class definition)
		error_msg_id = "DiscussionForm__title_errors"
		self.assertTrue(
			self.wait.until(lambda driver:
				self.driver.find_element('id', error_msg_id).text
				== self.ERROR
			)
		)

		# Now do the same, but this time, leave the discussion body text
		# blank, and check that it shows an error.

		# visit the edit/discussion page for a proposal
		proposal = Proposal.objects.get(pk=1)
		url = self.live_server_url + proposal.get_start_discussion_url()
		self.driver.get(url)

		# use webdriver commands to insert the test discussion's title
		title_input_id = 'DiscussionForm__title'
		self.driver.find_element('id', title_input_id).send_keys(self.TITLE)

		# leave the test discussions body blank
		text_input_id = 'DiscussionForm__text'
		self.driver.find_element('id', text_input_id).send_keys('')

		# now click the form's submit button 
		submit_button_id = 'DiscussionForm__submit'
		self.driver.find_element('id', submit_button_id).click()		
		
		error_msg_id = "DiscussionForm__text_errors"
		self.assertTrue(
			self.wait.until(lambda driver:
				self.driver.find_element('id', error_msg_id).text
				== self.ERROR
			)
		)


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
	TEST_TAGS = 'tag1 tag2 '
	PROPOSAL_TAGS_ID = 'proposal_tags'
	PROPOSAL_TAGS_CLASS = 'ui-widget-content'
	TAGS_ERROR_ID = 'proposal_tags_errors'
	TAGS_ERROR_MSG = 'Please include at least one tag.'

	def test_edit_proposal_english(self):
		self.do_edit_proposal('en-ca')

	def test_edit_proposal_french(self):
		self.do_edit_proposal('fr-ca')

	def do_edit_proposal(self, language_code='en-ca'):

		self.login_regularuser()

		expected_id = self.expect_proposal_id()

		# Go to the edit page for a test proposal
		self.driver.get(self.get_url(language_code))
		self.assertTrue(language_code, self.driver.current_url)

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
			event_type=self.EVENT_TYPE,
			language=language_code
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

	def get_url(self, language_code='en-ca'):
		edit_url = url_patch_lang(
			Proposal.objects.get(pk=self.expect_proposal_id).get_edit_url(),
			language_code
		)
		return self.full_url(edit_url)


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
			event_type,
			language='en-ca'
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
		self.assertEqual(p.link_back, url_patch_lang(
			proposal.get_url_by_view_name('proposal'), language))

		# Check if a Publication was made against the tags
		tag_names = tags.split()
		tag_objects = [
			Tag.objects.get(name=tag_names[0]),
			Tag.objects.get(name=tag_names[1])
		]



class AddProposalTest(ProposalFormTest):

	check_pk = False
	REASON = 'AUTHOR'
	EVENT_TYPE = 'ISSUE'

	def get_url(self, language_code='en-ca'):
		add_url = url_patch_lang(reverse('add_proposal'), language_code)
		return self.full_url(add_url)

	def expect_proposal_id(self):
		return Proposal.objects.all().count() + 1

	def do_edit_proposal(self, language_code='en-ca'):

		super(AddProposalTest, self).do_edit_proposal(language_code)

		opp_code = 'fr-ca' if language_code == 'en-ca' else 'en-ca'
		print 'opp_code', opp_code

		self.go(url_patch_lang('', language_code))
		time.sleep(3)

		self.assertTrue(self.values[0] in self.find('trending').text)

		self.go(url_patch_lang('', opp_code))
		time.sleep(3)

		self.assertFalse(self.values[0] in self.find('trending').text)




class VoteTest(SeleniumTestCase):

	up_on_class = 'upvote_on'
	down_on_class = 'downvote_on'



	def test_question_vote(self):
		self.login_regularuser()
		url = self.live_server_url + Question.objects.get(pk=1).get_url()
		vote_spec = {
			'up_id': 'QuestionVoteForm_q_upvote',
			'score_id': 'QuestionVoteForm_q_score',
			'down_id': 'QuestionVoteForm_q_downvote',
			'url': url
		}

		self.do_vote(**vote_spec)


	def test_answer_vote(self):
		self.login_superuser()
		url = self.live_server_url + Question.objects.get(pk=1).get_url()
		vote_spec = {
			'up_id': 'AnswerVoteForm_1_upvote',
			'score_id': 'AnswerVoteForm_1_score',
			'down_id': 'AnswerVoteForm_1_downvote',
			'url': url
		}

		self.do_vote(**vote_spec)


	def test_discussion_vote(self):
		self.login_superuser()
		url = self.live_server_url + Discussion.objects.get(pk=1).get_url()
		vote_spec = {
			'up_id': 'DiscussionVoteForm_q_upvote',
			'score_id': 'DiscussionVoteForm_q_score',
			'down_id': 'DiscussionVoteForm_q_downvote',
			'url': url
		}

		self.do_vote(**vote_spec)


	def test_reply_vote(self):
		self.login_regularuser()
		url = self.live_server_url + Discussion.objects.get(pk=1).get_url()
		vote_spec = {
			'up_id': 'ReplyVoteForm_1_upvote',
			'score_id': 'ReplyVoteForm_1_score',
			'down_id': 'ReplyVoteForm_1_downvote',
			'url': url
		}

		self.do_vote(**vote_spec)


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


	def do_vote(self, up_id, score_id, down_id, url):

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



class TestNotificationMessage(FixtureLoadedTestCase):
	EXPECTED_MESSAGES = [
		"superuser started an issue in a topic you're watching",
		"superuser started an issue in a topic you're watching",
		"superuser started an issue in a topic you're watching",
		"superuser started an issue in a topic you're watching",
		"superuser edited an issue you're watching",
		"superuser edited an issue you're watching",
		"superuser edited an issue you're watching",
		"superuser edited an issue you're watching",
		"superuser asked a question in an issue you're watching",
		"superuser asked a question in an issue you're watching",
		"superuser asked a question in an issue you're watching",
		"superuser asked a question in an issue you're watching",
		"superuser answered a question you asked",
		"superuser answered a question you commented on",
		"superuser answered a question you're watching",
		"superuser answered a question you're watching",
		"superuser posted in an issue you're watching",
		"superuser posted in an issue you're watching",
		"superuser posted in an issue you're watching",
		"superuser posted in an issue you're watching",
		"superuser replied to a post you wrote",
		"superuser replied to a post you commented on",
		"superuser replied to a post you're watching",
		"superuser replied to a post you're watching",
		"superuser commented on a post you wrote",
		"superuser commented on a post you also commented on",
		"superuser commented on a post you're watching",
		"superuser commented on a post you're watching",
		"superuser sent a letter in relation to an issue you're watching",
		"superuser sent a letter in relation to an issue you're watching",
		"superuser sent a letter in relation to an issue you're watching",
		"superuser sent a letter in relation to an issue you're watching",
		"superuser signed a letter you wrote",
		"superuser signed a letter you commented on",
		"superuser signed a letter you're watching",
		"superuser signed a letter you're watching",
		"someone voted on your post",
		"someone voted on your post",
		"someone voted on your post",
		"someone voted on your post",
		"system says hi!",
		"system says hi!",
		"system says hi!",
		"system says hi!"
	]

	def test_message(self):
		# these constants are defined in models and abstract_models
		events = [e[0] for e in EVENT_TYPE_CHOICES]
		reasons = [r[0] for r in REASON_CHOICES]

		source_user = User.objects.get(pk=1)
		target_user = User.objects.get(pk=2)

		pointer = 0
		for e in events:
			for r in reasons:
				notification = Notification(
					source_user=source_user,
					target_user=target_user,
					event_type=e,
					reason=r,
					link_back='link_back',
					event_data='system says hi!'
				)
				found_message = get_notification_message(notification)
				expected_message = self.EXPECTED_MESSAGES[pointer]
				pointer += 1
				self.assertEqual(found_message, expected_message)


class TestLogin(SeleniumTestCase):

	'''
		Tests the login forms -- both the ajax and syncronous form.
		Ensures that errors are shown, and that logging in with username
		or email are allowed
	'''

	def test_ajax_login(self):
		# try logging in normally, this should work
		self.go(reverse('index'))
		self.click('login_div')
		self.puts({
			'username': 'regularuser',
			'password': 'regularuser'
		})
		self.click('submit_login')

		time.sleep(100)

		# The user's avatar should appear showing that the user is logged in
		self.wait.until(lambda driver: self.find('logged_in_div'))


	def test_ajax_login_email(self):

		# try logging in using email, this should work
		self.go(reverse('index'))
		self.click('login_div')
		self.puts({
			'username': 'regular@example.com',
			'password': 'regularuser'
		})
		self.click('submit_login')

		# The user's avatar should appear showing that the user is logged in
		self.wait.until(lambda driver: self.find('logged_in_div'))


	def test_ajax_login_incorrect(self):

		# try leaving username blank
		self.go(reverse('index'))
		self.click('login_div')
		self.puts({
			#'username': 'regular@example.com',
			'password': 'regularuser'
		})
		self.click('submit_login')

		# An error message should display
		self.assertTrue(
			self.wait.until( lambda driver: 
				'Incorrect username or password' in
				self.find('ajax_login_error').text
			)
		)

		# The logged in div should not be shown 
		self.assertNotFound('logged_in_div')

		# try leaving username blank
		self.go(reverse('index'))
		self.click('login_div')
		self.puts({
			'username': 'regularuser',
			#'password': 'regularuser'
		})
		self.click('submit_login')

		# An error message should display
		self.assertTrue(
			self.wait.until( lambda driver: 
				'Incorrect username or password' in
				self.find('ajax_login_error').text
			)
		)

		# The logged in div should not be shown 
		self.assertNotFound('logged_in_div')

		# try submitting incorrect credentials
		self.go(reverse('index'))
		self.click('login_div')
		self.puts({
			'username': 'regularuser',
			'password': 'wrong_password'
		})
		self.click('submit_login')

		# An error message should display
		self.assertTrue(
			self.wait.until( lambda driver: 
				'Incorrect username or password' in
				self.find('ajax_login_error').text
			)
		)

		# The logged in div should not be shown 
		self.assertNotFound('logged_in_div')



	def test_login(self):
		# Try logging in normally, this should work
		self.go(reverse('login_required'))
		self.puts({
			'LoginForm__username': 'regularuser',
			'LoginForm__password': 'regularuser'
		})
		self.click('LoginForm__submit')

		# We should have been redirected to the home page
		self.assertEqual(
			self.driver.current_url,
			self.full_url(reverse('index'))
		)

		# The logged in div should be shown at upper right of the status bar
		self.find('logged_in_div')


	def test_login_email(self):
		# Try logging in using email, this should work
		self.go(reverse('login_required'))
		self.puts({
			'LoginForm__username': 'regular@example.com',
			'LoginForm__password': 'regularuser'
		})
		self.click('LoginForm__submit')

		# We should have been redirected to the home page
		self.assertEqual(
			self.driver.current_url,
			self.full_url(reverse('index'))
		)

		# The logged in div should be shown at upper right of the status bar
		self.find('logged_in_div')


	def test_login_incorrect(self):
		# Try ommitting username on login 
		self.go(reverse('login_required'))
		self.puts({
			#'LoginForm__username': 'regular@example.com',
			'LoginForm__password': 'regularuser'
		})
		self.click('LoginForm__submit')

		# We should still face the login form, with an error message
		self.assertEqual(
			self.driver.current_url,
			self.full_url(reverse('login_required'))
		)
		self.assertTrue(
			'Incorrect username or password' in self.find('middle').text
		)

		# The logged in div should not be shown
		self.assertNotFound('logged_in_div')

		# Try ommitting password on login 
		self.go(reverse('login_required'))
		self.puts({
			'LoginForm__username': 'regular@example.com',
			#'LoginForm__password': 'regularuser'
		})
		self.click('LoginForm__submit')

		# We should still face the login form, with an error message
		self.assertEqual(
			self.driver.current_url,
			self.full_url(reverse('login_required'))
		)
		self.assertTrue(
			'Incorrect username or password' in self.find('middle').text
		)

		# The logged in div should not be shown
		self.assertNotFound('logged_in_div')

		# Try using an incorrect pair
		self.go(reverse('login_required'))
		self.puts({
			'LoginForm__username': 'regularuser',
			'LoginForm__password': 'wrong_password'
		})
		self.click('LoginForm__submit')

		# We should still face the login form, with an error message
		self.assertEqual(
			self.driver.current_url,
			self.full_url(reverse('login_required'))
		)
		self.assertTrue(
			'Incorrect username or password' in self.find('middle').text
		)

		# The logged in div should not be shown
		self.assertNotFound('logged_in_div')



class TestIssueLang(SeleniumTestCase):

	def test_french_issues(self):
		# go to main page, in french
		self.go(url_patch_lang('', 'fr-ca'))
		self.assertFalse(
			'Keystone XL Pipeline Extension' in self.find('trending').text)
		self.assertTrue(
			'Ceci n\'est pas un titre' in self.find('trending').text)


	def test_english_issues(self):
		# go to main page, in english
		self.go(url_patch_lang('', 'en-ca'))
		self.assertTrue(
			'Keystone XL Pipeline Extension' in self.find('trending').text)
		self.assertFalse(
			'Ceci n\'est pas un titre' in self.find('trending').text)


class TestLoginRequired(FixtureLoadedTestCase):
	'''
	Attempts to perform requests and POSTs that require login, without
	actually logging in, and verifies that these do not work.
	'''

	# This is a list of views that require logins to respond to a get request
	# They will be accessed by get request.  Each is a tuple, where the first
	# elment is a view's name, followed by a dictionary of keyword arguments.
	login_get_views = [
		('add_proposal',{}),
		('start_discussion', {'target_id': 1})
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
				'tags': 'tag1,tag2',
				'language': 'en-ca'
			},
			Proposal
		),

		('edit', {'issue_id':1}, 
			{
				'title': 'Test title edited', 
				'summary': 'test summary',
				'text': 'Test proposal text', 
				'user': 1, 
				'tags': 'tag1,tag2',
				'language': 'en-ca'
			},
			Proposal
		),
	]

	ajax_posts = [
		# votes
		('vote_answer', {'valence':1, 'user':1, 'target':2}, AnswerVote),
		('vote_question', {'valence':1, 'user':1, 'target':2}, QuestionVote),
		('vote_discussion', {'valence':1, 'user':1, 'target':1}, 
			DiscussionVote),
		('vote_reply', {'valence':1, 'user':1, 'target':2}, ReplyVote),

		# Comments
		('answer_comment', {'text':'Test comment', 'user':1, 'target':1},
			AnswerComment),
		('question_comment', {'text':'Test comment', 'user':1, 'target':1},
			QuestionComment),
		('comment', {'text':'Test comment', 'user':1, 'target':1},
			Comment),
		('reply_comment', {'text':'Test comment', 'user':1, 'target':1},
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

		# this time we'll login, but the user will not have a validated 
		# email
		for view_name, kwargs, post_data, post_class in self.login_post_views:
			url = reverse(view_name, kwargs=kwargs)

			self.client.login(
				username='notvalidated', password='notvalidated')

			# make sure the logged in user and posted user are the same
			post_data['user'] = User.objects.get(username='notvalidated').pk

			response = self.client.post(url, post_data, follow=True)

			# check that we were redirected to invalid_email page
			self.assert_was_redirected_to_invalid_email(response)

			# this function tries to retrieve the object we posted 
			def func():
				post_class.objects.get(title=post_data['title'])

			# since posting should have failed, the object should not exist
			self.assertRaises(post_class.DoesNotExist, func)

		# this time we'll login before posting, but the logged in user
		# won't match the user indicated in the form, so we'll still get
		# redirected to the login page
		for view_name, kwargs, post_data, post_class in self.login_post_views:

			self.client.login(
				username='regularuser', password='regularuser')

			# make sure the logged in user and pasted user are different
			post_data['user'] = User.objects.get(username='superuser').pk

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

			print view_name

			self.client.login(
				username='superuser', password='superuser')

			url = reverse(view_name, kwargs=kwargs)

			response = self.client.post(url, post_data, follow=True)

			# verify we got redirected
			self.assert_was_not_redirected_to_login(response)

			# this function tries to retrieve the object we posted 
			def func():
				post_class.objects.get(title=post_data['title'])

			# since posting would have succeeded, the object should exist
			self.assertEqual(
				post_class.objects.filter(title=post_data['title']).count(),
				1
			)


	def test_get_login_required(self):

		# Trying to navigate to these views without logging in causes 
		# redirection to the login page
		for view_name, kwargs in self.login_get_views:
			url = reverse(view_name, kwargs=kwargs)
			response = self.client.get(url, follow=True)
			self.assert_was_redirected_to_login(response)

		# Trying to navigate to these views when logged in without validated
		# email causes redirection to the invalid_email page
		self.client.login(username='notvalidated', password='notvalidated')
		for view_name, kwargs in self.login_get_views:
			url = reverse(view_name, kwargs=kwargs)
			response = self.client.get(url, follow=True)
			self.assert_was_redirected_to_invalid_email(response)


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


		# Now attempt any posts that had a user field.  This time, login
		# but login as a different user than what is posted in the user field
		for endpoint, post_data, post_class in self.ajax_posts:



			# This part of the test only applies when the post data contains
			# a 'user' field.
			if 'user' in post_data:

				# Login as user regularuser
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


		# Now attempt posts that had a user field.  This time, login
		# as a user that has not validated their email
		for endpoint, post_data, post_class in self.ajax_posts:

			# This part of the test only applies when the post data contains
			# a 'user' field.
			if 'user' in post_data:

				# Login as user regularuser
				self.client.login(
					username='notvalidated', password='notvalidated')

				post_data['user'] = User.objects.get(username='notvalidated').pk
				url = reverse('handle_ajax_json', kwargs={'view':endpoint})
				response = self.client.post(url, post_data)

				self.assert_caught_non_validated_user(response)

				# since the post failed, the object is not in the database
				self.assertEqual(
					post_class.objects.filter(**post_data).count(), 0)

		# logout regular user
		self.client.logout()

		# Now attempt all the posts again, and this time they should get
		# accepted.  Any posts that have a user field (which is equal to
		# 1) will now match the logged in user.
		for endpoint, post_data, post_class in self.ajax_posts:

			# Login as user superuser
			self.client.login(username='superuser', password='superuser')
			# make sure that the posted user is superuser too
			post_data['user'] = User.objects.get(username='superuser').pk

			url = reverse('handle_ajax_json', kwargs={'view':endpoint})
			response = self.client.post(url, post_data)
			self.assert_ajax_post_accepted(response, endpoint)

			# since the post was accepted, we should find object in database
			self.assertEqual(
				post_class.objects.filter(**post_data).count(), 1,
				'the post wasn\'t loaded via %s' % endpoint)



	def assert_was_not_redirected_to_login(self, request):

		login_required_url_fragment = reverse('login_required')

		# pull the urls out of the redirect chain
		redirect_urls = [r[0] for r in request.redirect_chain]

		# Ensure login_required_url_fragment isn't within any part of the
		# redirect chain
		self.assertFalse(
			any([login_required_url_fragment in r for r in redirect_urls])
		)

	def assert_was_redirected_to_login(self, request):
		self.assertTrue(
			reverse('login_required') in request.redirect_chain[-1][0])

	def assert_was_redirected_to_invalid_email(self, request):
		self.assertTrue(
			reverse('invalid_email') in request.redirect_chain[-1][0])


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


	def assert_caught_non_validated_user(self, repsonse):
		# the response is JSON formatted
		reply_data = json.loads(repsonse.content)

		# assert that the reply was denied, and the reason was a lack of
		# authentication
		self.assertFalse(reply_data['success'])
		self.assertEqual(reply_data['msg'], "user email not validated")


	def assert_ajax_post_denied(self, response, endpoint):
		# the response is JSON formatted
		reply_data = json.loads(response.content)

		# assert that the reply was denied, and the reason was a lack of
		# authentication
		self.assertFalse(reply_data['success'], 'the post to %s should '
			'have been denied.' % endpoint)
		self.assertEqual(reply_data['msg'], "user did not authenticate")


class PublishSubscribeTest(FixtureLoadedTestCase):
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
		do_subscribable, is used.  The tests that match this formula
		can be defined by a few args passed into do_subscribable.
		That goes for testing questions, comments, letters, etc.

		But testing Proposals is a bit more complex so it is done in its
		own test routine, different from do_subscribable.
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
		p = Publication.objects.get(
			subscription_id=sector.subscription_id,
			source_user=proposal_author,
			event_type='ISSUE',
			was_posted=False,
			event_data=proposal.text[:100],
			link_back=proposal.get_url_by_view_name('proposal')
		)


	def test_question(self):
		proposal = Proposal.objects.get(pk=1)
		question_author = User.objects.get(username='superuser')
		title = 'Question about publications'
		text = 'Hey, will this trigger a publication like it should?'
		self.do_subscribable(
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
		self.do_subscribable(
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
			self.do_subscribable(
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
			self.do_subscribable(
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
			self.do_subscribable(
				target,
				comment_class,
				{
					'text':text,
				},
				comment_author,
				'COMMENT',
				text[:100]
			)


	def do_subscribable(
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





from django.contrib.auth import authenticate

class NewTest(FixtureLoadedTestCase):

	def test_users(self):

		# try to authenticate the user
		username='regularuser'
		password='regularuser'

		user = authenticate(
			username=username,
			password=password
		)

		print type(user)

		self.assertTrue(False)




class UserProfileTest(FixtureLoadedTestCase):
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


