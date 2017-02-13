from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class HomePageTest(LiveServerTestCase):
    ''' hello selenium '''

    browser = webdriver.Firefox()
    browser.get('http://localhost:8000')
    assert 'LMN' in browser.title
    browser.quit()


class BrowseArtists(LiveServerTestCase):

    fixtures = ['fn_testing_artists', 'fn_testing_venues', 'fn_testing_shows']

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_browsing_artists(self):

        # Start on home page

        self.browser.get(self.live_server_url)

        self.browser.implicitly_wait(3)

        # Find and click on artists link

        artist_list_link = self.browser.find_element_by_link_text('Artists')
        artist_list_link.click()

        # Assert all artists are shown, alphabetically (ACDC, REM, Yes)

        # TODO

        body = self.browser.find_element_by_tag_name('body').text

        # Assert that their names are links. These will fail with
        # an exception if not found.

        rem = self.browser.find_element_by_link_text('REM')
        acdc = self.browser.find_element_by_link_text('ACDC')
        yes = self.browser.find_element_by_link_text('Yes')

        # Assert that there is a link to view that artist's shows (which will lead to notes)

        rem_notes = self.browser.find_element_by_link_text('REM notes')
        acdc_notes = self.browser.find_element_by_link_text('ACDC notes')
        yes_notes = self.browser.find_element_by_link_text('Yes notes')

        # click on an artists name
        rem.click()

        # Assert that artist's info is shown on new page
        page = self.browser.find_element_by_tag_name('body').text
        self.assertContains(page, 'REM')
        self.assertContains(self.browser.current_url, 'artists/detail/\d+')

        # go back
        self.browser.back()

        # Click on venues' played link

        rem_notes.click()

        # assert list of venues that artist has played at is shown
        # Should be show pk = 1 venue 1 first ave on 2017-01-02 , show pk = 2 venue 2, turf club on 2016-11-02

        # Assert a link to add notes is shown for each show

        # click on one of the shows - get the first match
        see_notes_add_own = self.browser.find_element_by_partial_link_text('See notes for this')
        see_notes_add_own.click()

        # verify list of notes for that show are shown

        # should be two notes, awsome and ok, in that order

        first_note_div = self.browser.find_element_by_id('note_2')
        self.assertContains(first_note_div.text, 'awesome')
        self.assertContains(first_note_div.text, 'yay!')

        second_note_div = self.browser.find_element_by_id('note_1')
        self.assertContains(first_note_div.text, 'ok')
        self.assertContains(first_note_div.text, 'alright')


        # verify button (part of a form) to add user's own notes for that show is displayed

        add_notes = self.brower.find_element_by_tag_name('input')
        self.assertEqual(add_notes.text, 'Add your own notes')


    def test_searching_artists(self):
        pass



class BrowseVenues(LiveServerTestCase):

    fixtures = ['testing_artists', 'testing_venues']

    def test_browsing_venues(self):
        pass


    def test_searching_venues(self):
        pass



class Notes(LiveServerTestCase):

    def test_add_note_for_show(self):
        pass
        # Start at list of shows

        # click on 'see notes' link

        # verify list of notes displayed

        # verify add own note is displayed


    def test_add_note_redirect_to_login_and_back_to_add_note(self):
        pass
        # start at list of notes

        # click add note

        # verify redirect to login

        # login

        # verify redirect to add note form

        # enter note text and title

        # verify redirect to note detail


    def test_add_note_redirect_to_login_and_register_and_back_to_add_note(self):
        pass
        # start at list of notes

        # click add note

        # verify redirect to login

        # click register link

        # register account

        # verify redirect to add note form

        # enter note text and title

        # verify redirect to note detail


class TestRegistration(LiveServerTestCase):

    def test_login_from_home_page(self):
        pass

    def test_click_login_then_register_from_home_page(self):
        pass


class UserProfile(LiveServerTestCase):

    def test_notes_shown_on_profile_page(self):
        # todo notes have link to the user
        # notes have link to show
        pass
