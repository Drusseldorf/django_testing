from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

MAIN_PAGE_URL = pytest.lazy_fixture("main_page_url")
LOGIN_PAGE_URL = pytest.lazy_fixture("user_login_url")
LOGOUT_PAGE_URL = pytest.lazy_fixture("user_logout_url")
SIGNUP_PAGE_URL = pytest.lazy_fixture("user_signup_url")
POST_DETAIL_URL = pytest.lazy_fixture("post_url")
REMOVAL_URL = pytest.lazy_fixture("remark_delete_url")
UPDATE_URL = pytest.lazy_fixture("remark_edit_url")

REMOVAL_REDIRECT_URL = pytest.lazy_fixture("forced_remark_delete_url")
UPDATE_REDIRECT_URL = pytest.lazy_fixture("forced_remark_edit_url")

DEFAULT_CLIENT = pytest.lazy_fixture("client")
AUTHORING_CLIENT = pytest.lazy_fixture("writer_client")
ALT_USER_CLIENT = pytest.lazy_fixture("random_user_client")

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "page_url, client_fixture, expected_status",
    [
        (MAIN_PAGE_URL, DEFAULT_CLIENT, HTTPStatus.OK),
        (LOGIN_PAGE_URL, DEFAULT_CLIENT, HTTPStatus.OK),
        (LOGOUT_PAGE_URL, DEFAULT_CLIENT, HTTPStatus.OK),
        (SIGNUP_PAGE_URL, DEFAULT_CLIENT, HTTPStatus.OK),
        (POST_DETAIL_URL, DEFAULT_CLIENT, HTTPStatus.OK),
        (REMOVAL_URL, AUTHORING_CLIENT, HTTPStatus.OK),
        (REMOVAL_URL, ALT_USER_CLIENT, HTTPStatus.NOT_FOUND),
        (REMOVAL_URL, DEFAULT_CLIENT, HTTPStatus.FOUND),
        (UPDATE_URL, AUTHORING_CLIENT, HTTPStatus.OK),
        (UPDATE_URL, ALT_USER_CLIENT, HTTPStatus.NOT_FOUND),
        (UPDATE_URL, DEFAULT_CLIENT, HTTPStatus.FOUND),
    ],
)
def test_public_private_routes(client_fixture, page_url, expected_status):
    response = client_fixture.get(page_url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "target_url, forced_redirect",
    [
        (REMOVAL_URL, REMOVAL_REDIRECT_URL),
        (UPDATE_URL, UPDATE_REDIRECT_URL),
    ],
)
def test_redirect_for_remark_edit_delete(target_url, forced_redirect, client):
    response = client.get(target_url)
    assertRedirects(response, forced_redirect)
