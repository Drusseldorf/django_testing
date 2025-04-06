from http import HTTPStatus

from pytils.translit import slugify

from notes.models import Note
from notes.tests.testing_utils import (URL_CREATE, URL_REMOVE, URL_SUCCESS,
                                       URL_UPDATE, CommonSetupCase)


class TestNoteBehavior(CommonSetupCase):

    def test_anonymous_cannot_create(self):

        before = set(Note.objects.all())
        self.client.post(URL_CREATE, data=self.test_payload)
        after = set(Note.objects.all())
        self.assertEqual(before, after)

    def test_reject_not_unique_slug(self):

        self.test_payload["slug"] = self.current_note.slug
        existing = set(Note.objects.all())
        self.guest_client.post(URL_CREATE, data=self.test_payload)
        self.assertEqual(set(Note.objects.all()), existing)

    def _create_note_assertions(self, expected_slug):

        old_notes = set(Note.objects.all())
        self.guest_client.post(URL_CREATE, data=self.test_payload)
        new_notes = set(Note.objects.all()) - old_notes

        self.assertEqual(len(new_notes), 1)
        new_note = new_notes.pop()
        self.assertEqual(new_note.title, self.test_payload["title"])
        self.assertEqual(new_note.text, self.test_payload["text"])
        self.assertEqual(new_note.slug, expected_slug)
        self.assertEqual(new_note.author, self.guest_user)

    def test_empty_slug_autofilled(self):

        self.test_payload["slug"] = ""
        self._create_note_assertions(slugify(self.test_payload["title"]))

    def test_auth_user_creates_note(self):

        self._create_note_assertions(self.test_payload["slug"])

    def test_owner_edits_item(self):

        response = self.owner_client.post(URL_UPDATE, data=self.test_payload)
        self.assertRedirects(response, URL_SUCCESS)
        updated = Note.objects.get(id=self.current_note.id)
        self.assertEqual(updated.text, self.test_payload["text"])
        self.assertEqual(updated.title, self.test_payload["title"])
        self.assertEqual(updated.slug, self.test_payload["slug"])
        self.assertEqual(updated.author, self.current_note.author)

    def test_owner_removes_item(self):

        count_before = Note.objects.count()
        response = self.owner_client.post(URL_REMOVE)
        self.assertRedirects(response, URL_SUCCESS)
        self.assertEqual(Note.objects.count(), count_before - 1)
        self.assertFalse(Note.objects.filter(pk=self.current_note.pk).exists())

    def test_guest_cant_edit_item(self):

        response = self.guest_client.post(URL_UPDATE, data=self.test_payload)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_unchanged = Note.objects.get(id=self.current_note.id)
        self.assertEqual(note_unchanged.title, self.current_note.title)
        self.assertEqual(note_unchanged.text, self.current_note.text)
        self.assertEqual(note_unchanged.slug, self.current_note.slug)
        self.assertEqual(note_unchanged.author, self.current_note.author)

    def test_guest_cant_remove_item(self):

        notes_before = set(Note.objects.all())
        response = self.guest_client.post(URL_REMOVE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(notes_before, set(Note.objects.all()))

        note_unchanged = Note.objects.get(id=self.current_note.id)
        self.assertEqual(note_unchanged.title, self.current_note.title)
        self.assertEqual(note_unchanged.text, self.current_note.text)
        self.assertEqual(note_unchanged.slug, self.current_note.slug)
        self.assertEqual(note_unchanged.author, self.current_note.author)
