from django.test import TestCase, Client

from django.core.urlresolvers import reverse

from ..models import Venue, Artist, Note, Show
from django.contrib.auth.models import User

import re


class TestEmptyView(TestCase):
    def test_with_no_artists_returns_empty_list(self):
        pass


class TestArtistViews(TestCase):

    fixtures = ['testing_artists']

    def test_all_artists_displays_all_alphabetically(self):
        response = self.client.get(reverse('lmn:artist_list'))

        # .* matches 0 or more of any character. Test to see if
        # these names are present, in the right order

        regex = '.*Queen.*Sharon Jones.*Yes.*'
        response_text = str(response.content)
        print(response.content)

        self.assertTrue(re.match(regex, response_text))

        self.assertEqual(len(response.context['artists']), 3)
        self.assertTemplateUsed(response, 'lmn/artists/artist_list.html')


    def test_artists_search_clear_link(self):
        response = self.client.get( reverse('lmn:artist_list') , {'search_name' : 'Queen'} )

        # There is a clear link, it's url is the main venue page
        all_artists_url = reverse('lmn:artist_list')
        self.assertContains(response, all_artists_url)


    def test_artist_search_no_search_results(self):
        response = self.client.get( reverse('lmn:artist_list') , {'search_name' : 'REM'} )
        self.assertNotContains(response, 'Yes')
        self.assertNotContains(response, 'Sharon Jones')
        self.assertNotContains(response, 'Queen')
        # Check the length of artists list is 0
        self.assertEqual(len(response.context['artists']), 0)
        self.assertTemplateUsed(response, 'lmn/artists/artist_list.html')


    def test_artist_search_partial_match_search_results(self):

        response = self.client.get(reverse('lmn:artist_list'), {'search_name' : 's'})
        # Should be two responses, Yes and Sharon Jones
        self.assertContains(response, 'Yes')
        self.assertContains(response, 'Sharon Jones')
        self.assertNotContains(response, 'Queen')
        # Check the length of artists list is 2
        self.assertEqual(len(response.context['artists']), 2)
        self.assertTemplateUsed(response, 'lmn/artists/artist_list.html')


    def test_artist_search_one_search_result(self):

        response = self.client.get(reverse('lmn:artist_list'), {'search_name' : 'Queen'} )
        self.assertNotContains(response, 'Sharon Jones')
        self.assertNotContains(response, 'Yes')
        self.assertContains(response, 'Queen')
        # Check the length of artists list is 1
        self.assertEqual(len(response.context['artists']), 1)
        self.assertTemplateUsed(response, 'lmn/artists/artist_list.html')


    def test_artist_detail(self):

        ''' Artist 1 details displayed in correct template '''
        # kwargs to fill in parts of url. Not get or post params

        response = self.client.get(reverse('lmn:artist_detail', kwargs={'artist_pk' : 1} ))
        self.assertContains(response, 'Sharon Jones')
        self.assertEqual(response.context['artist'].name, 'Sharon Jones')
        self.assertEqual(response.context['artist'].pk, 1)

        self.assertTemplateUsed(response, 'lmn/artists/artist_detail.html')


    def test_get_artist_that_does_not_exist_returns_404(self):
        response = self.client.get(reverse('lmn:artist_detail', kwargs={'artist_pk' : 10} ))
        self.assertEqual(response.status_code, 404)


    def test_venues_for_artist(self):
        pass
        #TODO



class TestVenues(TestCase):

        fixtures = ['testing_venues']

        def test_with_venues_displays_all_alphabetically(self):
            response = self.client.get(reverse('lmn:venue_list'))

            # .* matches 0 or more of any character. Test to see if
            # these names are present, in the right order

            regex = '.*First Avenue.*Target Center.*The Turf Club.*'
            response_text = str(response.content)
            print(response.content)

            self.assertTrue(re.match(regex, response_text))

            self.assertEqual(len(response.context['venues']), 3)
            self.assertTemplateUsed(response, 'lmn/venues/venue_list.html')


        def test_venue_search_clear_link(self):
            response = self.client.get( reverse('lmn:venue_list') , {'search_name' : 'Fine Line'} )

            # There is a clear link, it's url is the main venue page
            all_venues_url = reverse('lmn:venue_list')
            self.assertContains(response, all_venues_url)


        def test_venue_search_no_search_results(self):
            response = self.client.get( reverse('lmn:venue_list') , {'search_name' : 'Fine Line'} )
            self.assertNotContains(response, 'First Avenue')
            self.assertNotContains(response, 'Turf Club')
            self.assertNotContains(response, 'Target Center')
            # Check the length of venues list is 0
            self.assertEqual(len(response.context['venues']), 0)
            self.assertTemplateUsed(response, 'lmn/venues/venue_list.html')


        def test_venue_search_partial_match_search_results(self):
            response = self.client.get(reverse('lmn:venue_list'), {'search_name' : 'c'})
            # Should be two responses, Yes and Sharon Jones
            self.assertNotContains(response, 'First Avenue')
            self.assertContains(response, 'Turf Club')
            self.assertContains(response, 'Target Center')
            # Check the length of venues list is 2
            self.assertEqual(len(response.context['venues']), 2)
            self.assertTemplateUsed(response, 'lmn/venues/venue_list.html')


        def test_venue_search_one_search_result(self):

            response = self.client.get(reverse('lmn:venue_list'), {'search_name' : 'Target'} )
            self.assertNotContains(response, 'First Avenue')
            self.assertNotContains(response, 'Turf Club')
            self.assertContains(response, 'Target Center')
            # Check the length of venues list is 1
            self.assertEqual(len(response.context['venues']), 1)
            self.assertTemplateUsed(response, 'lmn/venues/venue_list.html')


        def test_venue_detail(self):

            ''' venue 1 details displayed in correct template '''
            # kwargs to fill in parts of url. Not get or post params

            response = self.client.get(reverse('lmn:venue_detail', kwargs={'venue_pk' : 1} ))
            self.assertContains(response, 'First Avenue')
            self.assertEqual(response.context['venue'].name, 'First Avenue')
            self.assertEqual(response.context['venue'].pk, 1)

            self.assertTemplateUsed(response, 'lmn/venues/venue_detail.html')


        def test_get_venue_that_does_not_exist_returns_404(self):
            response = self.client.get(reverse('lmn:venue_detail', kwargs={'venue_pk' : 10} ))
            self.assertEqual(response.status_code, 404)


        def get_artists_for_venue(self):
            pass
            # TODO


class TestShows(TestCase):
    pass

class TestNoteList(TestCase):

    def test_notes_list(self):
        pass

    def test_notes_for_user(self):
        pass


class TestAddNotesRedirectToLogin(TestCase):
    pass

class TestAddNotesWhenUserLoggedIn(TestCase):
    fixtures = ['testing_users', 'testing_artists', 'testing_shows', 'testing_venues', 'testing_notes']

    # TODO add note for non-existent show is error

    def setUp(self):
        user = User.objects.first()
        self.client.force_login(user)


    def test_can_save_new_note_for_show_blank_data_is_error(self):

        new_note_url = reverse('lmn:new_note', kwargs={'show_pk':1})

        # No post params
        response = self.client.post(new_note_url, follow=True)
        # No note saved, should show same page
        self.assertTemplateUsed('lmn/notes/new_note.html')

        # no title
        response = self.client.post(new_note_url, {'text':'blah blah' }, follow=True)
        self.assertTemplateUsed('lmn/notes/new_note.html')

        # no text
        response = self.client.post(new_note_url, {'title':'blah blah' }, follow=True)
        self.assertTemplateUsed('lmn/notes/new_note.html')

        # nothing added to database
        self.assertEqual(Note.objects.count(), 2)   # 2 test notes provided in fixture, should still be 2



    def test_redirect_to_note_detail_after_save(self):

        new_note_url = reverse('lmn:new_note', kwargs={'show_pk':1})

        response = self.client.post(new_note_url, {'text':'ok', 'title':'blah blah' }, follow=True)
        self.assertRedirects(response, reverse('lmn:note_detail', kwargs={'note_pk':3}))

        latest_note = Note.objects.filter(text='ok', title='blah blah').all()
        self.assertEqual(len(latest_note), 1)

        self.assertEqual(Note.objects.count(), 3)   # 2 test notes provided in fixture, should still be 2



class TestUserAuthentication(TestCase):
    pass
