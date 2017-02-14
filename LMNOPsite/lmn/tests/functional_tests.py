from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import re, time

### TODO break into smaller tests?


class HomePageTest(LiveServerTestCase):
    ''' hello selenium '''

    browser = webdriver.Firefox()
    browser.get('http://localhost:8000')
    assert 'LMN' in browser.title
    browser.quit()


class BrowseArtists(LiveServerTestCase):

    fixtures = ['fn_testing_users', 'fn_testing_artists', 'fn_testing_venues', 'fn_testing_shows', 'fn_testing_notes']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_browsing_artists(self):

        # Start on home page
        self.browser.get(self.live_server_url)

        # When searching for elements, wait 3 seconds for element to appear of page. Needed
        # because page load time is slower than this script's execution time.
        self.browser.implicitly_wait(3)

        # Find and click on artists link
        artist_list_link = self.browser.find_element_by_link_text('Artists')
        artist_list_link.click()

        artists = [ 'ACDC' , 'REM', 'Yes' ]

        artist_divs = self.browser.find_elements_by_class_name('artist')

        for artist, div in zip (artists, artist_divs):

            # assert artist name is present
            assert artist in div.text

            # find a link is present with artist name - exception raised if not found
            div.find_element_by_link_text(artist)
            # Find the link to view that artist's shows (which will lead to notes). Again, exception raised
            div.find_element_by_link_text('%s notes' % artist)


        # Are we on the right page? Do this after finding elements so know page has loaded
        assert '/artists/list/' in self.browser.current_url
        assert 'Artist List' in self.browser.page_source  # Could also put the title in a div or header element, and find that, and verify correct text.

        # Get a link to one of the artists
        rem = self.browser.find_element_by_link_text('REM')

        # click this link
        rem.click()

        # Assert that artist's info is shown on new page
        # Assert that the URL is as expected. REM pk = 1.
        artist_name = self.browser.find_element_by_id('artist_name')
        assert 'REM' in artist_name.text
        assert '/artists/detail/1' in self.browser.current_url

        # go back
        self.browser.back()

        # Get a link to that artist's shows (and to notes)
        rem_notes = self.browser.find_element_by_link_text('REM notes')

        # Click on shows/notes link
        rem_notes.click()

        title = self.browser.find_element_by_id('title')
        # On correct page? Verify title, and URL
        assert 'Venues that REM has played at' in title.text
        print('url', self.browser.current_url)
        assert 'artists/venues_played/1' in self.browser.current_url

        # assert list of venues that artist has played at is shown, most recent first
        # Should be show pk = 2 venue 1 first ave on 2017-01-02 , show pk = 1 venue 2, turf club on 2016-11-02
        # Assert a link to add notes is shown for each show
        expected_shows =  [ { "pk" : 2 , "show_date" : "Jan. 2, 2017", "venue" : 'The Turf Club' },
        {"model" : "lmn.show", "pk" : 1 , "show_date" : "Nov. 4, 2016", "venue" : 'First Avenue' } ]

        show_divs = self.browser.find_elements_by_class_name('show')

        for show, div in zip (expected_shows, show_divs):
            assert show['venue'] in div.text
            assert show['show_date'] in div.text

        # click on one of the shows - get the first match (Turf Club, Jan 2)
        see_notes_add_own = self.browser.find_element_by_partial_link_text('See notes for this')
        see_notes_add_own.click()

        # verify list of notes for that show are shown
        # verify on correct page
        title = self.browser.find_element_by_id('show_title')
        assert 'Notes for REM at The Turf Club on Jan. 2, 2017' in title.text
        assert 'notes/for_show/2' in self.browser.current_url

        # should be two notes, awsome and ok, in that order - most recently posted first
        # Trying out a different way of finding and checking properties of elements. A loop is less typing :)

        print(self.browser.page_source)
        first_note_div = self.browser.find_element_by_id('note_2')
        # Is the title (in a H3 element) 'awesome' ?
        assert 'awesome' in first_note_div.find_element_by_tag_name('h3').text
        # Check note text
        assert 'yay!' in first_note_div.text
        # By correct user?
        assert 'bob' in first_note_div.find_element_by_class_name('user').text
        # Posted on the epected day?
        assert 'Posted on Feb. 13, 2017' in first_note_div.text

        # Repeat for second note
        second_note_div = self.browser.find_element_by_id('note_1')
        assert 'ok' in second_note_div.find_element_by_tag_name('h3').text
        assert 'alright' in second_note_div.text
        assert 'alice' in second_note_div.find_element_by_class_name('user').text
        # Posted on the epected day?
        assert 'Posted on Feb. 12, 2017' in second_note_div.text

        # verify input button to add user's own notes for that show is displayed
        add_notes = self.browser.find_element_by_tag_name('input')
        self.assertEqual(add_notes.get_attribute('value'), 'Add your own notes')

        # Adding a note requires authentication - will do this in another test.


    def test_searching_artists(self):

        self.browser.get(self.live_server_url + '/artists/list')

        # Verify title
        title = self.browser.find_element_by_id('title')
        assert 'All artists' in title.text

        # Find search form. Django gives each form input an id.

        search_input = self.browser.find_element_by_id('id_search_name')

        # ** Exact match search **

        # Enter text and submit form
        search_input.send_keys('Yes')  # one exact match
        search_input.submit()   # Convenience method to submit the form that the input belongs to.

        time.sleep(1)  # Wait for page to load. (yuck). TODO how to check for search page load?

        # Verify correct title
        title = self.browser.find_element_by_id('title')
        assert 'Artists matching \'Yes\'' in title.text

        print(self.browser.page_source)

        # Exactly one result for Yes
        assert 'Yes' in self.browser.page_source
        assert 'REM' not in self.browser.page_source
        assert 'ACDC' not in self.browser.page_source

        # ** partial text search **

        search_input = self.browser.find_element_by_id('id_search_name')

        # Enter text and submit form
        search_input.send_keys('e')  # should return two partial-text matches; search is case-insensitive
        search_input.submit()   # Convenience method to submit the form that the input belongs to.

        time.sleep(1)  # Wait for page to load. (ugh).

        # Verify correct title
        title = self.browser.find_element_by_id('title')
        assert 'Artists matching \'e\'' in title.text

        print(self.browser.page_source)
        assert 'Yes' in self.browser.page_source
        assert 'REM' in self.browser.page_source
        assert 'ACDC' not in self.browser.page_source

        # **  No matches **
        search_input = self.browser.find_element_by_id('id_search_name')

        # Enter text and submit form
        search_input.send_keys('ZZZ ZZZ')  # no exact matches
        search_input.submit()   # Convenience method to submit the form that the input belongs to.

        time.sleep(1)  # Wait for page to load. (meh).

        # Verify correct title
        title = self.browser.find_element_by_id('title')  # id with spaces in ??
        assert 'Artists matching \'ZZZ ZZZ\'' in title.text

        assert 'Yes' not in self.browser.page_source
        assert 'REM' not in self.browser.page_source
        assert 'ACDC' not in self.browser.page_source

        # "No artists found message"

        assert 'No artists found' in self.browser.page_source

        # Find and click 'clear' button

        clear = self.browser.find_element_by_partial_link_text('clear')
        clear.click()

        time.sleep(1)  # Wait for page to load. (still yuck).

        # After search cleared, verify all artists are shown

        assert 'Yes' in self.browser.page_source
        assert 'REM' in self.browser.page_source
        assert 'ACDC' in self.browser.page_source


class BrowseVenues(LiveServerTestCase):

    fixtures = ['fn_testing_users', 'fn_testing_artists', 'fn_testing_venues', 'fn_testing_shows', 'fn_testing_notes']

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_browsing_venues(self):

        # Start on home page
        self.browser.get(self.live_server_url)

        # When searching for elements, wait 3 seconds for element to appear of page. Needed
        # because page load time is slower than this script's execution time.
        self.browser.implicitly_wait(3)

        # Find and click on venues link
        venue_list_link = self.browser.find_element_by_link_text('Venues')
        venue_list_link.click()

        venues = [ 'First Avenue' , 'Target Center', 'The Turf Club' ]

        venue_divs = self.browser.find_elements_by_class_name('venue')

        for venue, div in zip (venues, venue_divs):

            # assert venue name is present
            assert venue in div.text

            # find a link is present with venue name - exception raised if not found
            div.find_element_by_link_text(venue)
            # Find the link to view that venue's shows (which will lead to notes). Again, exception raised
            div.find_element_by_link_text('%s notes' % venue)


        # Are we on the right page? Do this after finding elements so know page has loaded
        assert '/venues/list/' in self.browser.current_url
        assert 'Venue List' in self.browser.page_source  # Could also put the title in a div or header element, and find that, and verify correct text.

        # Get a link to one of the venues
        rem = self.browser.find_element_by_link_text('REM')

        # click this link
        rem.click()

        # Assert that venue's info is shown on new page
        # Assert that the URL is as expected. REM pk = 1.
        venue_name = self.browser.find_element_by_id('venue_name')
        assert 'REM' in venue_name.text
        assert '/venues/detail/1' in self.browser.current_url

        # go back
        self.browser.back()

        # Get a link to that venue's shows (and to notes)
        rem_notes = self.browser.find_element_by_link_text('REM notes')

        # Click on shows/notes link
        rem_notes.click()

        title = self.browser.find_element_by_id('title')
        # On correct page? Verify title, and URL
        assert 'Venues that REM has played at' in title.text
        print('url', self.browser.current_url)
        assert 'venues/venues_played/1' in self.browser.current_url

        # assert list of venues that venue has played at is shown, most recent first
        # Should be show pk = 2 venue 1 first ave on 2017-01-02 , show pk = 1 venue 2, turf club on 2016-11-02
        # Assert a link to add notes is shown for each show
        expected_shows =  [ { "pk" : 2 , "show_date" : "Jan. 2, 2017", "venue" : 'The Turf Club' },
        {"model" : "lmn.show", "pk" : 1 , "show_date" : "Nov. 4, 2016", "venue" : 'First Avenue' } ]

        show_divs = self.browser.find_elements_by_class_name('show')

        for show, div in zip (expected_shows, show_divs):
            assert show['venue'] in div.text
            assert show['show_date'] in div.text

        # click on one of the shows - get the first match (Turf Club, Jan 2)
        see_notes_add_own = self.browser.find_element_by_partial_link_text('See notes for this')
        see_notes_add_own.click()

        # verify list of notes for that show are shown
        # verify on correct page
        title = self.browser.find_element_by_id('show_title')
        assert 'Notes for REM at The Turf Club on Jan. 2, 2017' in title.text
        assert 'notes/for_show/2' in self.browser.current_url

        # should be two notes, awsome and ok, in that order - most recently posted first
        # Trying out a different way of finding and checking properties of elements. A loop is less typing :)

        print(self.browser.page_source)
        first_note_div = self.browser.find_element_by_id('note_2')
        # Is the title (in a H3 element) 'awesome' ?
        assert 'awesome' in first_note_div.find_element_by_tag_name('h3').text
        # Check note text
        assert 'yay!' in first_note_div.text
        # By correct user?
        assert 'bob' in first_note_div.find_element_by_class_name('user').text
        # Posted on the epected day?
        assert 'Posted on Feb. 13, 2017' in first_note_div.text

        # Repeat for second note
        second_note_div = self.browser.find_element_by_id('note_1')
        assert 'ok' in second_note_div.find_element_by_tag_name('h3').text
        assert 'alright' in second_note_div.text
        assert 'alice' in second_note_div.find_element_by_class_name('user').text
        # Posted on the epected day?
        assert 'Posted on Feb. 12, 2017' in second_note_div.text

        # verify input button to add user's own notes for that show is displayed
        add_notes = self.browser.find_element_by_tag_name('input')
        self.assertEqual(add_notes.get_attribute('value'), 'Add your own notes')

        # Test artist with no shows
        self.browser.back() # To list of shows
        self.browser.back() # to list of artists

        no_shows_artists = document.find_element_by_link_text('Yes notes')
        # This page should say 'we have no records that this artist has played at'
        no_shows_artists.click()
        no_show_para = document.find_element_by_id('no_results')
        assert 'no records of venues' in no_show_para.text

        # Adding a note requires authentication - will do this in another test.



    def test_searching_venues(self):

            self.browser.get(self.live_server_url + '/venues/list')

            # Verify title
            title = self.browser.find_element_by_id('title')
            assert 'All venues' in title.text

            # Find search form. Django gives each form input an id.

            search_input = self.browser.find_element_by_id('id_search_name')

            # ** Exact match search **

            # Enter text and submit form
            search_input.send_keys('First Avenue')  # one exact match
            search_input.submit()   # Convenience method to submit the form that the input belongs to.

            time.sleep(1)  # Wait for page to load. (yuck). TODO how to check for search page load?

            # Verify correct title
            title = self.browser.find_element_by_id('title')
            assert 'Venues matching \'First Avenue\'' in title.text

            # Exactly one result for First Avenue
            assert 'First Avenue' in self.browser.page_source
            assert 'Target Center' not in self.browser.page_source
            assert 'The Turf Club' not in self.browser.page_source
            # Check for no "No venues found" message
            assert 'No venues found' not in self.browser.page_source

            # ** partial text search **

            search_input = self.browser.find_element_by_id('id_search_name')

            # Enter text and submit form
            search_input.send_keys('a')  # should return two partial-text matches; search is case-insensitive
            search_input.submit()   # Convenience method to submit the form that the input belongs to.

            time.sleep(1)  # Wait for page to load. (ugh).

            # Verify correct title
            title = self.browser.find_element_by_id('title')
            assert 'Venues matching \'a\'' in title.text

            assert 'First Avenue' in self.browser.page_source
            assert 'Target Center' in self.browser.page_source
            assert 'The Turf Club' not in self.browser.page_source
            # Check for no "No venues found" message
            assert 'No venues found' not in self.browser.page_source

            # **  No matches **
            search_input = self.browser.find_element_by_id('id_search_name')

            # Enter text and submit form
            search_input.send_keys('ZZZ ZZZ')  # no exact matches
            search_input.submit()   # Convenience method to submit the form that the input belongs to.

            time.sleep(1)  # Wait for page to load. (meh).

            # Verify correct title
            title = self.browser.find_element_by_id('title')  # id with spaces in ??
            assert 'Venues matching \'ZZZ ZZZ\'' in title.text

            assert 'First Avenue' not in self.browser.page_source
            assert 'Target Center' not in self.browser.page_source
            assert 'The Turf Club' not in self.browser.page_source

            # Check for "No venues found" message
            assert 'No venues found' in self.browser.page_source

            # Find and click 'clear' button

            clear = self.browser.find_element_by_partial_link_text('clear')
            clear.click()

            time.sleep(1)  # Wait for page to load. (still yuck).

            # After search cleared, verify all venues are shown

            assert 'First Avenue' in self.browser.page_source
            assert 'Target Center' in self.browser.page_source
            assert 'The Turf Club' in self.browser.page_source



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
