from http import HTTPStatus

import pytest
from django.test.client import Client
from pytest_django.asserts import assertRedirects

from news.forms import BAD_WORDS as RESTRICTED_WORDS
from news.forms import WARNING as REMARK_WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db
test_client = Client()

REMARK_PAYLOAD = {"text": "Новый комментарий"}

RESTRICTED_REMARKS = [
    {"text": f"Много слов... {bad} ...ещё слова"} for bad in RESTRICTED_WORDS
]


def test_non_auth_cant_create_remark(client, post_url):
    initial_comments_count = Comment.objects.count()
    response = client.post(post_url, data=REMARK_PAYLOAD)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == initial_comments_count


def test_auth_user_can_create_remark(
    random_user_client, post_instance, random_user, post_url
):
    initial_comments_count = Comment.objects.count()
    response = random_user_client.post(post_url, data=REMARK_PAYLOAD)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == initial_comments_count + 1
    saved_comment = Comment.objects.latest('created')
    assert saved_comment.text == REMARK_PAYLOAD["text"]
    assert saved_comment.news == post_instance
    assert saved_comment.author == random_user


@pytest.mark.parametrize("bad_data", RESTRICTED_REMARKS)
def test_no_bad_words_in_remarks(random_user_client, post_url, bad_data):
    initial_comments_count = Comment.objects.count()
    response = random_user_client.post(post_url, data=bad_data)
    assert response.status_code == HTTPStatus.OK
    assert Comment.objects.count() == initial_comments_count
    form = response.context["form"]
    assert "text" in form.errors
    assert REMARK_WARNING in form.errors["text"]


def test_owner_can_delete_remark(
    writer_client, post_instance, remark, remark_delete_url
):
    initial_comments_count = Comment.objects.count()
    response = writer_client.post(remark_delete_url)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == initial_comments_count - 1


def test_random_user_cant_delete_remark(
    random_user_client, remark_delete_url, remark
):
    initial_comments_count = Comment.objects.count()
    response = random_user_client.post(remark_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == initial_comments_count
    same_comment = Comment.objects.get(pk=remark.pk)
    assert same_comment.text == remark.text
    assert same_comment.news == remark.news
    assert same_comment.author == remark.author


def test_owner_can_edit_remark(
    writer_client, remark, remark_edit_url, forced_post_comments_redirect
):
    response = writer_client.post(remark_edit_url, data=REMARK_PAYLOAD)
    assert response.status_code == HTTPStatus.FOUND
    assertRedirects(response, forced_post_comments_redirect)
    updated = Comment.objects.get(pk=remark.pk)
    assert updated.text == REMARK_PAYLOAD["text"]
    assert updated.news == remark.news
    assert updated.author == remark.author


def test_random_user_cant_edit_remark(
    random_user_client, remark, remark_edit_url
):
    response = random_user_client.post(remark_edit_url, data=REMARK_PAYLOAD)
    assert response.status_code == HTTPStatus.NOT_FOUND
    unchanged = Comment.objects.get(pk=remark.pk)
    assert unchanged.text == remark.text
    assert unchanged.news == remark.news
    assert unchanged.author == remark.author