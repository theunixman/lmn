from django.test import TestCase, Client

from django.core.urlresolvers import reverse

from ..models import Venue, Artist, Note, Show
from django.contrib.auth.models import User



class TestEmptyView(TestCase):
    def test_with_no_artists_returns_empty_list(self):
        pass


class TestArtistViews(TestCase):

    fixtures = ['testing_artists']

    def test_with_artists_displays_all_alphabetically(self):
        response = self.client.get(reverse('lmn:artist_list'))
        data = response


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



class TestVenues(TestCase):
    pass

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
