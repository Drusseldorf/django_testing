from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()

TEST_NOTE_SLUG = "note_slug"

URL_CREATE = reverse("notes:add")
URL_MAIN = reverse("notes:home")
URL_LIST = reverse("notes:list")
URL_SUCCESS = reverse("notes:success")

URL_SIGNIN = reverse("users:login")
URL_SIGNOUT = reverse("users:logout")
URL_REGISTER = reverse("users:signup")

URL_UPDATE = reverse("notes:edit", args=(TEST_NOTE_SLUG,))
URL_DETAIL = reverse("notes:detail", args=(TEST_NOTE_SLUG,))
URL_REMOVE = reverse("notes:delete", args=(TEST_NOTE_SLUG,))

FORCED_CREATE_URL = f"{URL_SIGNIN}?next={URL_CREATE}"
FORCED_REMOVE_URL = f"{URL_SIGNIN}?next={URL_REMOVE}"
FORCED_DETAIL_URL = f"{URL_SIGNIN}?next={URL_DETAIL}"
FORCED_UPDATE_URL = f"{URL_SIGNIN}?next={URL_UPDATE}"
FORCED_LIST_URL = f"{URL_SIGNIN}?next={URL_LIST}"
FORCED_SUCCESS_URL = f"{URL_SIGNIN}?next={URL_SUCCESS}"


class CommonSetupCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.guest_user = User.objects.create(username="RandomUser")
        cls.guest_client = Client()
        cls.guest_client.force_login(cls.guest_user)

        cls.owner_user = User.objects.create(username="AuthorUser")
        cls.owner_client = Client()
        cls.owner_client.force_login(cls.owner_user)

        cls.current_note = Note.objects.create(
            title="Начальный заголовок",
            text="Начальный текст",
            slug=TEST_NOTE_SLUG,
            author=cls.owner_user,
        )

        cls.test_payload = {
            "title": "Новый заголовок",
            "text": "Новый текст",
            "slug": "second-slug",
        }
