from digidemo import settings
from django.test import TestCase, LiveServerTestCase
from django.core.files import File
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
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


#class EndToEndTests(LiveServerTestCase):
#	'''
#	Tests that comprise of a full request and render cycles
#	'''
#
#	def setUp(self):
#		createProposal()
#
#	def test_voting_widget(self):
#
#		# make a driven browser instance
#		driver = webdriver.Firefox()
#		
#		# navigate to the proposal overview
#		proposal = Proposal.objects.get()
#		proposal_url = proposal.get_overview_url()
#		driver.get(self.live_server_url + proposal_url)

#		print driver.title
#		inputElement = driver.find_element_by_name("q")
#		inputElement.send_keys("cheese!")
#		inputElement.submit()
#
#		try:
#			WebDriverWait(driver, 10).until(EC.title_contains("cheese!"))
#			print driver.title
#
#		finally:
#			pass

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


