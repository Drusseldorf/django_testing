from notes.forms import NoteForm
from notes.tests.testing_utils import (URL_CREATE, URL_LIST, URL_UPDATE,
                                       CommonSetupCase)


class TestContentPages(CommonSetupCase):

    def test_item_presence_in_list(self):
        response = self.owner_client.get(URL_LIST)
        notes_list = response.context["object_list"]
        self.assertIn(self.current_note, notes_list)
        found_note = notes_list.get(pk=self.current_note.id)
        self.assertEqual(found_note.title, self.current_note.title)
        self.assertEqual(found_note.text, self.current_note.text)
        self.assertEqual(found_note.slug, self.current_note.slug)
        self.assertEqual(found_note.author, self.current_note.author)

    def test_absence_for_non_author(self):
        response = self.guest_client.get(URL_LIST)
        notes_list = response.context["object_list"]
        self.assertNotIn(self.current_note, notes_list)

    def test_form_on_relevant_pages(self):
        pages = (URL_CREATE, URL_UPDATE)
        for page in pages:
            with self.subTest(page=page):
                response = self.owner_client.get(page)
                self.assertIsInstance(response.context.get("form"), NoteForm)
