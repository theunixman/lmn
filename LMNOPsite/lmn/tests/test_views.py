from django.test import TestCase, Client

from django.core.urlresolvers import reverse

from ..models import Venue, Artist, Note, Show
from django.contrib.auth.models import User

import re, datetime
from datetime import timezone


class TestEmptyView(TestCase):
    def test_with_no_artists_returns_empty_list(self):
        pass


class TestArtistViews(TestCase):

    fixtures = ['testing_artists', 'testing_venues', 'testing_shows']

    def test_all_artists_displays_all_alphabetically(self):
        response = self.client.get(reverse('lmn:artist_list'))

        # .* matches 0 or more of any character. Test to see if
        # these names are present, in the right order

        regex = '.*ACDC.*REM.*Yes.*'
        response_text = str(response.content)

        self.assertTrue(re.match(regex, response_text))

        self.assertEqual(len(response.context['artists']), 3)
        self.assertTemplateUsed(response, 'lmn/artists/artist_list.html')


    def test_artists_search_clear_link(self):
        response = self.client.get( reverse('lmn:artist_list') , {'search_name' : 'ACDC'} )

        # There is a clear link, it's url is the main venue page
        all_artists_url = reverse('lmn:artist_list')
        self.assertContains(response, all_artists_url)


    def test_artist_search_no_search_results(self):
        response = self.client.get( reverse('lmn:artist_list') , {'search_name' : 'Queen'} )
        self.assertNotContains(response, 'Yes')
        self.assertNotContains(response, 'REM')
        self.assertNotContains(response, 'ACDC')
        # Check the length of artists list is 0
        self.assertEqual(len(response.context['artists']), 0)
        self.assertTemplateUsed(response, 'lmn/artists/artist_list.html')


    def test_artist_search_partial_match_search_results(self):

        response = self.client.get(reverse('lmn:artist_list'), {'search_name' : 'e'})
        # Should be two responses, Yes and REM
        self.assertContains(response, 'Yes')
        self.assertContains(response, 'REM')
        self.assertNotContains(response, 'ACDC')
        # Check the length of artists list is 2
        self.assertEqual(len(response.context['artists']), 2)
        self.assertTemplateUsed(response, 'lmn/artists/artist_list.html')


    def test_artist_search_one_search_result(self):

        response = self.client.get(reverse('lmn:artist_list'), {'search_name' : 'ACDC'} )
        self.assertNotContains(response, 'REM')
        self.assertNotContains(response, 'Yes')
        self.assertContains(response, 'ACDC')
        # Check the length of artists list is 1
        self.assertEqual(len(response.context['artists']), 1)
        self.assertTemplateUsed(response, 'lmn/artists/artist_list.html')


    def test_artist_detail(self):

        ''' Artist 1 details displayed in correct template '''
        # kwargs to fill in parts of url. Not get or post params

        response = self.client.get(reverse('lmn:artist_detail', kwargs={'artist_pk' : 1} ))
        self.assertContains(response, 'REM')
        self.assertEqual(response.context['artist'].name, 'REM')
        self.assertEqual(response.context['artist'].pk, 1)

        self.assertTemplateUsed(response, 'lmn/artists/artist_detail.html')


    def test_get_artist_that_does_not_exist_returns_404(self):
        response = self.client.get(reverse('lmn:artist_detail', kwargs={'artist_pk' : 10} ))
        self.assertEqual(response.status_code, 404)


    def test_venues_played_at_most_recent_shows_first(self):
        # Artist 1 (REM) has played at venue 2 (Turf Club) on two dates

        url = reverse('lmn:venues_for_artist', kwargs={'artist_pk':1})
        response = self.client.get(url)
        shows = list(response.context['shows'].all())
        print('SHOWS' , shows)
        show1, show2 = shows[0], shows[1]
        self.assertEqual(2, len(shows))

        self.assertEqual(show1.artist.name, 'REM')
        self.assertEqual(show1.venue.name, 'The Turf Club')

        expected_date = datetime.datetime(2017, 2, 2, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(0, (show1.show_date - expected_date).total_seconds())

        self.assertEqual(show2.artist.name, 'REM')
        self.assertEqual(show2.venue.name, 'The Turf Club')
        expected_date = datetime.datetime(2017, 1, 2, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(0, (show2.show_date - expected_date).total_seconds())

        # Artist 2 (ACDC) has played at venue 1 (First Ave)

        url = reverse('lmn:venues_for_artist', kwargs={'artist_pk':2})
        response = self.client.get(url)
        shows = list(response.context['shows'].all())
        show1 = shows[0]
        self.assertEqual(1, len(shows))

        self.assertEqual(show1.artist.name, 'ACDC')
        self.assertEqual(show1.venue.name, 'First Avenue')
        expected_date = datetime.datetime(2017, 1, 21, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(0, (show1.show_date - expected_date).total_seconds())

        # Artist 3 , no shows

        url = reverse('lmn:venues_for_artist', kwargs={'artist_pk':3})
        response = self.client.get(url)
        shows = list(response.context['shows'].all())
        self.assertEqual(0, len(shows))



class TestVenues(TestCase):

        fixtures = ['testing_venues']

        def test_with_venues_displays_all_alphabetically(self):
            response = self.client.get(reverse('lmn:venue_list'))

            # .* matches 0 or more of any character. Test to see if
            # these names are present, in the right order

            regex = '.*First Avenue.*Target Center.*The Turf Club.*'
            response_text = str(response.content)

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
            # Should be two responses, Yes and REM
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



        def test_artists_played_at_venue_most_recent_first(self):
            # Artist 1 (REM) has played at venue 2 (Turf Club) on two dates

            url = reverse('lmn:artists_at_venue', kwargs={'venue_pk':2})
            response = self.client.get(url)
            shows = list(response.context['shows'].all())
            print('SHOWS' , shows)
            show1, show2 = shows[0], shows[1]
            self.assertEqual(2, len(shows))

            self.assertEqual(show1.artist.name, 'REM')
            self.assertEqual(show1.venue.name, 'The Turf Club')

            expected_date = datetime.datetime(2017, 2, 2, 0, 0, tzinfo=timezone.utc)
            self.assertEqual(0, (show1.show_date - expected_date).total_seconds())

            self.assertEqual(show2.artist.name, 'REM')
            self.assertEqual(show2.venue.name, 'The Turf Club')
            expected_date = datetime.datetime(2017, 1, 2, 0, 0, tzinfo=timezone.utc)
            self.assertEqual(0, (show2.show_date - expected_date).total_seconds())

            # Artist 2 (ACDC) has played at venue 1 (First Ave)

            url = reverse('lmn:artists_at_venue', kwargs={'venue_pk':1})
            response = self.client.get(url)
            shows = list(response.context['shows'].all())
            show1 = shows[0]
            self.assertEqual(1, len(shows))

            self.assertEqual(show1.artist.name, 'ACDC')
            self.assertEqual(show1.venue.name, 'First Avenue')
            expected_date = datetime.datetime(2017, 1, 21, 0, 0, tzinfo=timezone.utc)
            self.assertEqual(0, (show1.show_date - expected_date).total_seconds())

            # Venue 3 has not had any shows

            url = reverse('lmn:artists_at_venue', kwargs={'venue_pk':3})
            response = self.client.get(url)
            shows = list(response.context['shows'].all())
            self.assertEqual(0, len(shows))



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
