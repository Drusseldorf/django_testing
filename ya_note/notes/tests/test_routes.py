from http import HTTPStatus

from notes.tests.testing_utils import (FORCED_CREATE_URL, FORCED_DETAIL_URL,
                                       FORCED_LIST_URL, FORCED_REMOVE_URL,
                                       FORCED_SUCCESS_URL, FORCED_UPDATE_URL,
                                       URL_CREATE, URL_DETAIL, URL_LIST,
                                       URL_MAIN, URL_REGISTER, URL_REMOVE,
                                       URL_SIGNIN, URL_SIGNOUT, URL_SUCCESS,
                                       URL_UPDATE, CommonSetupCase)


class TestNoteRoutes(CommonSetupCase):

    def test_pages_availability(self):

        scenarios = [
            (URL_MAIN, self.client, HTTPStatus.OK),
            (URL_SIGNIN, self.client, HTTPStatus.OK),
            (URL_SIGNOUT, self.client, HTTPStatus.OK),
            (URL_REGISTER, self.client, HTTPStatus.OK),
            (URL_LIST, self.guest_client, HTTPStatus.OK),
            (URL_CREATE, self.guest_client, HTTPStatus.OK),
            (URL_SUCCESS, self.guest_client, HTTPStatus.OK),
            (URL_DETAIL, self.owner_client, HTTPStatus.OK),
            (URL_UPDATE, self.owner_client, HTTPStatus.OK),
            (URL_REMOVE, self.owner_client, HTTPStatus.OK),
            (URL_DETAIL, self.guest_client, HTTPStatus.NOT_FOUND),
            (URL_UPDATE, self.guest_client, HTTPStatus.NOT_FOUND),
            (URL_REMOVE, self.guest_client, HTTPStatus.NOT_FOUND),
            (URL_DETAIL, self.client, HTTPStatus.FOUND),
            (URL_UPDATE, self.client, HTTPStatus.FOUND),
            (URL_REMOVE, self.client, HTTPStatus.FOUND),
            (URL_CREATE, self.client, HTTPStatus.FOUND),
            (URL_LIST, self.client, HTTPStatus.FOUND),
            (URL_SUCCESS, self.client, HTTPStatus.FOUND),
        ]
        for url, test_client, expected_status in scenarios:
            with self.subTest(url=url, status=expected_status):
                self.assertEqual(
                    test_client.get(url).status_code, expected_status
                )

    def test_redirect_for_anonymous_client(self):

        redirects = [
            (URL_CREATE, FORCED_CREATE_URL),
            (URL_DETAIL, FORCED_DETAIL_URL),
            (URL_REMOVE, FORCED_REMOVE_URL),
            (URL_UPDATE, FORCED_UPDATE_URL),
            (URL_LIST, FORCED_LIST_URL),
            (URL_SUCCESS, FORCED_SUCCESS_URL),
        ]
        for private_url, forced_redirect in redirects:
            with self.subTest(url=private_url):
                response = self.client.get(private_url)
                self.assertRedirects(response, forced_redirect)
