from digidemo import settings
from django.test import TestCase, LiveServerTestCase
from django.core.files import File
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from digidemo.models import *
import filecmp
import os

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


def createProposal():
	user = createUser()
	proposal = Proposal(
		title='Test Proposal Title',
		summary='''
This is a summary <script>do_evil()</script>

A new paragraph

- bullet
- bullet
			''',
		text ='''
This is the main text area &nbsp; 

A new papagraph in the main text area
			''',
		is_published=True,
		score=0,
		user=user
	)
	proposal.save()
	return proposal


class ProposalTest(TestCase):
	'''
	Tests functionality related to the proposal model.
	'''

	def setUp(self):
		self.proposal = createProposal()

	def test_url_resolution(self):
		pk = self.proposal.pk
		print self.proposal.get_overview_url()
		self.assertTrue(
			self.proposal.get_overview_url().endswith(
			'/overview/%d/test-proposal-title' % pk)
		)
		self.assertTrue(
			self.proposal.get_proposal_url().endswith(
			'/proposal/%d/test-proposal-title' % pk)
		)
		self.assertTrue(
			self.proposal.get_discussion_url().endswith(
			'/discuss/%d/test-proposal-title' % pk)
		)

		self.assertTrue(
			self.proposal.get_edit_url().endswith(
			'/edit/%d/test-proposal-title' % pk)
		)


class EndToEndTests(LiveServerTestCase):
	'''
	Tests that comprise of a full request and render cycles
	'''

	def setUp(self):
		createProposal()

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
		

	def get_and_test_vote_widget(self, vote_widget_test, driver):

		# abbreviate
		vwt = vote_widget_test

		driver.get(self.live_server_url + vwt['url'])

		# get the vote elements
		up_elm = driver.find_element('id', vwt['up_id'])
		down_elm = driver.find_element('id', vwt['down_id'])
		score_elm = driver.find_element('id', vwt['score_id'])

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

		# make a driven browser instance, navigate to specified url
		driver = webdriver.Firefox()

		# get the vote widget, and test its initial state
		widget = self.get_and_test_vote_widget(vwt, driver)

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

		driver.quit()
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
		driver = webdriver.Firefox()

		# get the vote widget, and test its initial state
		widget = self.get_and_test_vote_widget(vwt, driver)

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

		driver.quit()
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


