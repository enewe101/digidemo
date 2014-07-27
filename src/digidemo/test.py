import time
import copy
import unittest
from django.core.urlresolvers import reverse
from django.test import TestCase, LiveServerTestCase
from django.core.files import File
from digidemo import settings
from digidemo.models import *
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import filecmp
import os


def pyWait(predicate, timeout, period):

	start = time.time()
	max_time = start + timeout

	while time.time() < max_time:
		if predicate():
			return True
		time.sleep(period)
	
	return False


def setUpModule():
	global DRIVER, WAIT
	DRIVER = webdriver.Firefox()
	WAIT = WebDriverWait(DRIVER, 3)	


def tearDownModule():
	global DRIVER
	DRIVER.quit()

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



class ProposalTest(TestCase):
	'''
	Tests functionality related to the proposal model.
	'''

	def setUp(self):
		self.proposal = Proposal.objects.get(pk=1)

	def test_url_resolution(self):
		pk = self.proposal.pk
		self.assertTrue(
			self.proposal.get_overview_url().endswith(
			'/overview/%d/keystone-xl-pipeline-extension' % pk)
		)
		self.assertTrue(
			self.proposal.get_proposal_url().endswith(
			'/proposal/%d/keystone-xl-pipeline-extension' % pk)
		)
		self.assertTrue(
			self.proposal.get_discussion_url().endswith(
			'/discuss/%d/keystone-xl-pipeline-extension' % pk)
		)

		self.assertTrue(
			self.proposal.get_edit_url().endswith(
			'/edit/%d/keystone-xl-pipeline-extension' % pk)
		)



class QuestionRenderTest(LiveServerTestCase):
	'''
		tests that the test question in the database renders correctly
	'''

	def test_render(self):
		question = Question.objects.get(pk=1)
		DRIVER.get(self.live_server_url + question.get_url())

		DRIVER.find_element_by_class_name('discussion_title')
		DRIVER.find_element_by_id('q_upvote')
		DRIVER.find_element_by_id('q_score')
		DRIVER.find_element_by_id('q_downvote')

		





class SeleniumFormTest(LiveServerTestCase):

	@classmethod
	def setUpClass(cls):

		# SeleniumFormTest is an abstract test class.  It shouldn't be run
		# but classes that inherit from it should.
		if cls == SeleniumFormTest:
			raise unittest.SkipTest('abstract class')

		else:
			super(SeleniumFormTest, cls).setUpClass()


	FIELD_TYPES = ['SUBMIT', 'TEXTS', 'SELECTIONS']

	def fill_form_correctly_and_verify(self):

		# Fill and submit the form
		self.fill_and_submit(self.FORM_DATA)

		# verify that the proposal and related objects are found in the 
		# database
		self.check_valid()


	def fill_and_submit(self, data):
		self.fill_form(data)
		self.submit_form()
	

	def fill_form(self, data):

		# Accomodate the fact that the form elements may be dynamically
		# loaded, but timeout if form elements not found within three seconds

		# Apply the select choices
		if 'SELECTIONS' in data:
			for spec in data['SELECTIONS']:
				element_id, datum = spec[0], spec[1]
				elm = WAIT.until( lambda driver:
					Select(driver.find_element('id', element_id)))
				elm.select_by_visible_text(datum)

		# Enter text in text-based inputs
		if 'TEXTS' in data:
			for spec in data['TEXTS']:
				element_id, datum = spec[0], spec[1]
				elm = WAIT.until(lambda driver: 
					driver.find_element('id', element_id))
				elm.send_keys(datum)


	def clear_fields(self, data):

		# Accomodate the fact that the form elements may be dynamically
		# loaded, but timeout if form elements not found within three seconds

		# Apply the select choices
		if 'SELECTIONS' in data:
			for spec in data['SELECTIONS']:
				element_id = spec[0]
				elm = WAIT.until( lambda driver:
					Select(driver.find_element('id', element_id)))
				elm.select_by_visible_text('-'*9)

		# Enter text in text-based inputs
		if 'TEXTS' in data:
			for spec in data['TEXTS']:
				element_id = spec[0]
				elm = WAIT.until(lambda driver: 
					driver.find_element('id', element_id))
				elm.clear()


	def submit_form(self):
		# submit the form
		DRIVER.find_element('id', self.FORM_DATA['SUBMIT']).click()


	def get_current_url(self):
		return DRIVER.current_url


	def test_simple_add(self):
		# This test simply does a vanilla form filling, submission, and check
		DRIVER.get(self.ADD_FORM_URL)
		self.fill_form_correctly_and_verify()


	def test_form_errors(self):
		DRIVER.get(self.ADD_FORM_URL)
		self.fill_form(self.FORM_DATA)

		for field_type in self.FIELD_TYPES:
			if field_type in self.FORM_DATA and field_type != 'SUBMIT':
				for spec in self.FORM_DATA[field_type]:

					# check whether the field is specified as required
					required = False
					try:
						required = bool(spec[2] == 'require')
					except IndexError:
						pass

					# if required, try ommitting it; ensure error.
					if required:
						self.clear_fields({field_type: [spec]})
						self.submit_form()
						self.check_invalid()

						# replace the missing field
						self.fill_form({field_type: [spec]})


		# finally, confirm that the form submits correctly,
		# with all the fields filled
		self.submit_form()
		self.check_valid()

		


class AnswerFormTest(SeleniumFormTest):

	def setUp(self):
		self.TEXT = 'Test answer text'
		self.FORM_DATA = {
			'TEXTS': [('AnswerForm_text', self.TEXT, 'require')],
			'SUBMIT': 'AnswerForm__submit' 
		}

		self.QUESTION = Question.objects.get(pk=1)
		self.ADD_FORM_URL = self.live_server_url + self.QUESTION.get_url()
		self.USER = User.objects.get(username='superuser')


	@unittest.skip('skip')
	def test_form_errors(self):
		super(AnswerFormTest, self).test_form_errors()


	def test_simple_add(self):
		super(AnswerFormTest, self).test_simple_add()


	def check_valid(self):

		# We may have to wait, but soon the new answer is in the db
		self.assertTrue(
			pyWait(lambda: Answer.objects.count(), 3, 0.15))

		answer = Answer.objects.get()
		self.assertEqual(answer.text, self.TEXT)
		self.assertEqual(answer.user, self.USER)
		self.assertEqual(answer.target, self.QUESTION)
		self.assertEqual(answer.score, 0)

		# check that the new answer is on the page
		reply_body = WAIT.until(
			lambda driver: driver.find_elements_by_class_name('reply_body'))

		# check for the voting elements.  When they are inserted, their id is
		# built from some user data.
		vote_id = (self.USER.username 
			+ str(Answer.objects.filter(target=self.QUESTION).count()))

		WAIT.until(
			lambda driver: driver.find_element('id', vote_id + '_upvote'))
		WAIT.until(
			lambda driver: driver.find_element('id', vote_id + '_score'))
		WAIT.until(
			lambda driver: driver.find_element('id', vote_id + '_downvote'))

		# check that the divider was introduced between the Q and A
		hr_flourishes = WAIT.until(
			lambda driver: driver.find_elements_by_class_name('flourish'))
		self.assertEqual(len(hr_flourishes), 2)


		# check that the entry box was hidden
		# TODO


class QuestionFormTest(SeleniumFormTest):
	'''
	Tests adding a question using the QuestionForm
	'''

	def setUp(self):

		self.TITLE = 'Test Title'
		self.TEXT = 'Test text.'
		self.FORM_DATA = {
			'TEXTS': [
				('QuestionForm_title', self.TITLE, 'require'),
				('QuestionForm_text', self.TEXT, 'require')
			],
			'SUBMIT': 'QuestionForm__submit'
		}

		self.PROPOSAL = Proposal.objects.get(pk=1)
		self.ADD_FORM_URL = (self.live_server_url 
			+ self.PROPOSAL.get_question_url())
		self.USER = User.objects.get(username='superuser')


	def check_valid(self):

		# check whether the new question was created
		question_set = self.PROPOSAL.question_set.filter(
			title=self.TITLE)
		self.assertEqual(question_set.count(), 1)

		# verify the question has the right data
		self.question = question_set[0]
		self.assertEqual(self.question.text, self.TEXT)
		self.assertEqual(self.question.user, self.USER)
		self.assertEqual(self.question.target, self.PROPOSAL)

		# check that we were redirected to the view-question page
		self.assertEqual(
			self.get_current_url(),
			self.live_server_url + self.question.get_url()
		)


	def check_invalid(self):

		# ensure the new question was not created
		question_set = self.PROPOSAL.question_set.filter(
			title=self.TITLE)
		self.assertEqual(question_set.count(), 0)

		# ensure we are faced with the form again (rather than redirected)
		self.assertEqual(self.get_current_url(), self.ADD_FORM_URL)


	def get_success_url(self):
		return self.question.get_url()




class ProposalFormTest(SeleniumFormTest):
	'''
	Tests adding and editing proposals (proposal versions), and their 
	associated factors. 
	'''

	def setUp(self):
		# Text fields for proposal version
		self.TITLE = 'Test Title'
		self.SUMMARY = 'Test summary.'
		self.TEXT = 'Test text.'

		# The hardcoded logged in user's name.  Change this when logging in
		# users is ready
		self.USERNAME = 'superuser'

		## Second, Pair dummy datas with the form elements in which they 
		## are to be entered

		# Valence, textarea id, and input text for factors
		self.FACTOR_TEXTS = [
			(
				1 if val=='pos' else -1,
				'id_%s-%d-description' % (val,i),
				u'Test %s factor %d' % (val,i),
			) 
			for val in ['pos', 'neg'] for i in range(5) 
		]

		# Text to put in proposal version text inputs and textareas
		self.PLAIN_ENTRIES = [
			('ProposalVersionForm_title', self.TITLE, 'require'),
			('ProposalVersionForm_summary', self.SUMMARY, 'require'),
			('ProposalVersionForm_text', self.TEXT, 'require'),
		]
		self.FACTOR_ENTRIES = [(f[1],f[2]) for f in self.FACTOR_TEXTS]
		self.TEXTS = self.PLAIN_ENTRIES + self.FACTOR_ENTRIES

		# Sector selections to use in factors
		self.SELECTIONS = [ 
			('id_pos-0-sector', u'ECO', 'require'),
			('id_pos-1-sector', u'ENV'),
			('id_pos-2-sector', u'HEA'),
			('id_pos-3-sector', u'EDU'),
			('id_pos-4-sector', u'IR' ),
								      
			('id_neg-0-sector', u'SOC'),
			('id_neg-1-sector', u'SEC'),
			('id_neg-2-sector', u'DEM'),
			('id_neg-3-sector', u'ECO'),
			('id_neg-4-sector', u'ENV'),
		]

		self.FORM_DATA = {
			'SUBMIT': '__submit',
			'SELECTIONS': self.SELECTIONS,
			'TEXTS': self.TEXTS
		}

		self.ADD_FORM_URL = self.live_server_url + reverse('add_proposal')
		self.EDIT_FORM_URL = (self.live_server_url 
			+ Proposal.objects.get(title="Keystone XL Pipeline Extension")\
				.get_edit_url())


	def test_edit_proposal(self):
		DRIVER.get(self.EDIT_FORM_URL)

		# clear all the data.  Add extra factor forms first to prevent
		# selenium from complaining about not finding the elemnt to clear
		self.click_add_factor_forms()
		self.click_add_factor_forms()
		self.click_add_factor_forms()
		self.click_add_factor_forms()
		self.clear_all_fields()

		# populate it with new data and submit
		self.fill_form_correctly_and_verify()



	def test_edit_delete_factor(self):

		DRIVER.get(self.EDIT_FORM_URL)

		# Test clicking delete after description or sector (or neither) has
		# been cleared -- form should still validate
		DRIVER.find_element('id', 'id_neg-0-description').clear()
		elm = Select(DRIVER.find_element('id', 'id_pos-1-sector'))
		elm.select_by_visible_text('-'*9)

		# If we have description filled, sector blank, its ok (ignored) if
		# deleted is checked
		self.click_add_factor_forms() # we need to add a form for this
		elm = WAIT.until(lambda driver: 
			driver.find_element('id', 'id_neg-2-description'))
		elm.send_keys(self.SELECTIONS[6][1])

		# Check deleted on all the above factors (and one other)
		for id_stub in ['pos-0', 'neg-0', 'pos-1', 'neg-2']:
			DRIVER.find_element('id', 'id_%s-deleted' % id_stub).click()

		# we can also have sector selected on an add-form, as long as 
		# description is not selected too
		elm = Select(DRIVER.find_element('id', 'id_neg-1-sector'))
		elm.select_by_visible_text('HEA')


		# for convenience in verification, also change the title
		title_elm = DRIVER.find_element('id', 'ProposalVersionForm_title')
		title_elm.clear()
		title_elm.send_keys(self.TITLE)

		self.submit_form()

		# Make sure the form was submitted successfully
		self.verify_form_validated()

		p = Proposal.objects.get(title=self.TITLE)
		fs = p.factor_set.filter(deleted=False)
		self.assertEqual(fs.count(), 1)
		self.assertTrue(fs[0].description.startswith('Facilitating'))


	def clear_all_fields(self):
		for field_kind in ['SELECTIONS', 'TEXTS']:
			for idx in range(len(self.FORM_DATA[field_kind])):
				self.clear_field(field_kind, idx)


	def clear_and_return_field(self, field_kind, idx):

		# Get the datum that will be cleared from the form.  
		# Copy it into a form_data datastructure
		if field_kind.upper() == 'SELECTIONS':
			datum = self.FORM_DATA['SELECTIONS'][idx]
			return_datum = {'SELECTIONS': [datum], 'TEXTS': []}

		elif field_kind.upper() == 'TEXTS':
			datum = self.FORM_DATA['TEXTS'][idx]
			return_datum = {'SELECTIONS':[], 'TEXTS': [datum]}

		self.clear_field(field_kind, idx)
		return return_datum


	def clear_field(self, field_kind, idx):

		if field_kind.upper() == 'SELECTIONS':
			id_to_clear = self.FORM_DATA['SELECTIONS'][idx][0]
			elm = WAIT.until( lambda driver:
				Select(driver.find_element('id', id_to_clear)))
			elm.select_by_visible_text('---------')

		elif field_kind.upper() == 'TEXTS':
			id_to_clear = self.FORM_DATA['TEXTS'][idx][0]
			DRIVER.find_element('id', id_to_clear).clear()


	def clear_field_submit_ensure_error(self, field_kind, idx):
		return_datum = self.clear_and_return_field(field_kind, idx)
		self.submit_form()
		# We should be faced with the form again (same url) because of errors
		self.check_invalid()
		return return_datum
		

	def fill_form_correctly_and_verify(self):
		self.fill_and_submit(self.FORM_DATA)
		self.check_valid()


	def check_valid(self):
		self.check_db()
		self.verify_form_validated()


	def check_invalid(self):
		self.assertTrue(
			self.get_current_url() in [self.ADD_FORM_URL, self.EDIT_FORM_URL])


	def verify_form_validated(self):
		# We should be redirected to the proposal view page
		self.assertEqual(DRIVER.current_url, self.get_view_proposal_url())


	def get_view_proposal_url(self):
		return 	(
			self.live_server_url 
			+ Proposal.objects.get(title=self.TITLE).get_proposal_url())
	

	def fill_and_submit(self, data):
		self.fill_form(data)
		self.submit_form()


	def click_add_factor_forms(self):
		# click on the add another factor link to expose more factor forms
		# This implicitly tests that these links do reveal more factor forms
		for val in ['pos', 'neg']:
			element_id = 'add_%s_factor_form' % val
			DRIVER.find_element('id', element_id).click()


	def fill_form(self, data):

		# We'll add two extra factors, to test adding extra factors
		self.click_add_factor_forms()
		self.click_add_factor_forms()
	
		super(ProposalFormTest, self).fill_form(data)



	def check_db(self):
		## Third, look in the database to see if the new Proposal, 
		## ProposalVersion, Factors, and FactorVersions were created, and do
		## integrity checks

		# Get the proposal by title
		# Check data in fields of both the Proposal and ProposalVersion  
		proposal = Proposal.objects.get(title=self.TITLE)
		proposal_version = proposal.get_latest()
		for prop_obj in [proposal, proposal_version]:
			self.assertEqual(prop_obj.summary, self.SUMMARY) 
			self.assertEqual(prop_obj.text, self.TEXT) 
			self.assertEqual(prop_obj.user.username, self.USERNAME)
			self.assertSequenceEqual(prop_obj.tags.all(), [])

		self.assertEqual(proposal.original_user.username, self.USERNAME)

		# Default score should be 0
		self.assertEqual(proposal.score, 0)

		# Check foreign key back-link from ProposalVersion to Proposal
		self.assertEqual(proposal_version.proposal, proposal)

		# Check that all the factors were made
		factor_properties = []
		factor_version_properties = []
		for factor in proposal.factor_set.all():
			# While we're at it, check that the factor mirrors the content
			# of its latest factor version
			factor_version = factor.get_latest()

			# check integrity -- does factor version reference its factor
			self.assertEqual(factor_version.factor, factor)

			self.assertEqual(
				factor_version.proposal_version, proposal_version)
			self.assertFalse(factor.deleted)
			self.assertFalse(factor_version.deleted)
			
			# Accumulate all the factor properties together so that they
			# can be checked in a batch
			expected_factor_property_tuple = (
				factor.valence,
				factor.sector.short_name,
				factor.description,
			)

			expected_factor_version_property_tuple = (
				factor_version.valence,
				factor_version.sector.short_name,
				factor_version.description,
			)
			factor_properties.append(expected_factor_property_tuple)
			factor_version_properties.append(
				expected_factor_version_property_tuple)

		# Accumulate all the *expected* factor properties 
		expected_factor_properties = [(d[0],s[1], d[2]) 
			for s,d in zip(self.SELECTIONS, self.FACTOR_TEXTS)]


		self.assertItemsEqual(factor_properties, expected_factor_properties)
		self.assertItemsEqual(
			factor_version_properties, expected_factor_properties)


class EndToEndTests(LiveServerTestCase):
	'''
	Tests that comprise of a full request and render cycles
	'''

	def setUp(self):
		self.proposal = Proposal.objects.get(pk=1)

	def test_discussion_voting_widget(self):

		# navigate to the proposal overview
		proposal = Proposal.objects.get(pk=1)
		discussion_url = proposal.get_discussion_url()

		# specify the expected vote element class_names
		vote_test_specs = {
			'url': discussion_url,
			'up_id': '1_upvote',
			'down_id': '1_downvote',
			'score_id': '1_score',
			'up_on': 'upvote_on',
			'up_off': 'upvote_off',
			'down_on': 'downvote_on',
			'down_off': 'downvote_off'
		}

		# test upvote element behavior, and check if it registers in db
		new_score = self.upvote_test(vote_test_specs)
		discussion = Proposal.objects.get(pk=1).discussion_set.all()[0]
		self.assertTrue(discussion.score == new_score)
		
		# test downvote element behavior, and check if it registers in db
		new_score = self.downvote_test(vote_test_specs)
		discussion = Proposal.objects.get(pk=1).discussion_set.all()[0]
		self.assertTrue(discussion.score == new_score)
		

	def test_letter_voting_widget(self):

		# navigate to the proposal overview
		proposal = Proposal.objects.get(pk=1)
		proposal_url = proposal.get_overview_url()

		# specify the expected vote element class_names
		vote_test_specs = {
			'url': proposal_url,
			'up_id': '1_upvote',
			'down_id': '1_downvote',
			'score_id': '1_score',
			'up_on': 'upvote_on',
			'up_off': 'upvote_off',
			'down_on': 'downvote_on',
			'down_off': 'downvote_off'
		}

		# test upvote element behavior, and check if it registers in db
		new_score = self.upvote_test(vote_test_specs)
		letter = Proposal.objects.get(pk=1).letter_set.all()[0]
		self.assertTrue(letter.score == new_score)
		
		# test downvote element behavior, and check if it registers in db
		new_score = self.downvote_test(vote_test_specs)
		letter = Proposal.objects.get(pk=1).letter_set.all()[0]
		self.assertTrue(letter.score == new_score)
		

	def test_proposal_voting_widget(self):

		# navigate to the proposal overview
		proposal = Proposal.objects.get(pk=1)
		proposal_url = proposal.get_overview_url()

		# specify the expected vote element class_names
		vote_test_specs = {
			'url': proposal_url,
			'up_id': 'proposal_vote_upvote',
			'down_id': 'proposal_vote_downvote',
			'score_id': 'proposal_vote_score',
			'up_on': 'upvote_on',
			'up_off': 'upvote_off',
			'down_on': 'downvote_on',
			'down_off': 'downvote_off'
		}

		# test upvote element behavior, and check if it registers in db
		new_score = self.upvote_test(vote_test_specs)
		proposal = Proposal.objects.get(pk=1)
		self.assertTrue(proposal.score == new_score)
		
		# test downvote element behavior, and check if it registers in db
		new_score = self.downvote_test(vote_test_specs)
		proposal = Proposal.objects.get(pk=1)
		self.assertTrue(proposal.score == new_score)
		

	def get_and_test_vote_widget(self, vote_widget_test):

		# abbreviate
		vwt = vote_widget_test

		DRIVER.get(self.live_server_url + vwt['url'])

		# get the vote elements
		up_elm = DRIVER.find_element('id', vwt['up_id'])
		down_elm = DRIVER.find_element('id', vwt['down_id'])
		score_elm = DRIVER.find_element('id', vwt['score_id'])

		# check that vote widget class names are correct
		up_class = up_elm.get_attribute('class')
		down_class = down_elm.get_attribute('class')
		self.assertTrue(up_class == vwt['up_on'] or up_class == vwt['up_off'])
		if up_class == vwt['up_off']:
			self.assertTrue(down_class == vwt['down_off'])
		else:
			self.assertTrue(down_class == vwt['down_on'] 
				or down_class == vwt['down_off'])

		# get the current score
		score = int(score_elm.text)
		
		widget = {'up_elm':up_elm, 'down_elm':down_elm, 'score_elm':score_elm,
			'up_class':up_class, 'down_class':down_class, 'score':score}

		return widget


	def upvote_test(
		self, vote_widget_test):
		'''
		`vote_test_specs` should look like this:

		{
			'url': <url on which vote widget is found>,
			'up_id': <html id for upvote widget element>,
			'down_id': <html id for downvote widget element>,
			'score_id': <html id for div displaying score>,
			'up_on': <name of class for upvote on>,
			'up_off': <name of calass for upvote off>,
			'down_on': <name of class for downvote on>,
			'down_off': <name of calass for downvote off>,
		}
		'''
		
		# abbreviate
		vwt = vote_widget_test

		# get the vote widget, and test its initial state
		widget = self.get_and_test_vote_widget(vwt)

		# click the upvote and see if it toggled class and changed score
		widget['up_elm'].click()
		new_upvote_class = widget['up_elm'].get_attribute('class')
		new_downvote_class = widget['down_elm'].get_attribute('class')
		new_score = int(widget['score_elm'].text)

		# check that the score and element class were updated correctly
		if widget['up_class'] == vwt['up_off']:
			self.assertTrue(new_upvote_class == vwt['up_on'])

			if widget['down_class'] == vwt['down_off']:
				self.assertTrue(new_score == widget['score'] + 1)

			else:
				self.assertTrue(new_score == widget['score'] + 2)

		else:
			self.assertTrue(new_upvote_class == vwt['up_off'])
			self.assertTrue(new_score == widget['score'] - 1)

		self.assertTrue(new_downvote_class == vwt['down_off'])

		return new_score 


	def downvote_test(
		self, vote_widget_test):
		'''
		`vote_test_specs` should look like this:

		{
			'url': <url on which vote widget is found>,
			'up_id': <html id for upvote widget element>,
			'down_id': <html id for downvote widget element>,
			'score_id': <html id for div displaying score>,
			'up_on': <name of class for upvote on>,
			'up_off': <name of calass for upvote off>,
			'down_on': <name of class for downvote on>,
			'down_off': <name of calass for downvote off>,
		}
		'''
		
		# abbreviate
		vwt = vote_widget_test

		# make a driven browser instance, navigate to specified url
		DRIVER.get(self.live_server_url + vwt['url'])

		# get the vote widget, and test its initial state
		widget = self.get_and_test_vote_widget(vwt)

		# click the upvote and see if it toggled class and changed score
		widget['down_elm'].click()
		new_downvote_class = widget['down_elm'].get_attribute('class')
		new_upvote_class = widget['up_elm'].get_attribute('class')
		new_score = int(widget['score_elm'].text)

		# check that the score and element class were updated correctly
		if widget['down_class'] == vwt['down_off']:
			self.assertTrue(new_downvote_class == vwt['down_on'])

			if widget['up_class'] == vwt['up_off']:
				self.assertTrue(new_score == widget['score'] - 1)

			else:
				self.assertTrue(new_score == widget['score'] - 2)

		else:
			self.assertTrue(new_downvote_class == vwt['down_off'])
			self.assertTrue(new_score == widget['score'] + 1)

		self.assertTrue(new_upvote_class == vwt['up_off'])

		return new_score 


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


