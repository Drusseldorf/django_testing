from http import client

import pytest
from django.test.client import Client

from news.forms import CommentForm
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE

pytestmark = pytest.mark.django_db
test_client = Client()


def test_posts_on_main_page(sample_posts, main_page_url):
    response = test_client.get(main_page_url)
    content_objects = response.context["object_list"]
    assert content_objects.count() == NEWS_COUNT_ON_HOME_PAGE


def test_order_of_posts(sample_posts, client, main_page_url):
    response = client.get(main_page_url)
    posts_dates = [post.date for post in response.context["object_list"]]
    assert posts_dates == sorted(posts_dates, reverse=True)


def test_order_of_remarks(sample_remarks, client, post_instance, post_url):
    response = client.get(post_url)
    assert "news" in response.context
    remark_timestamps = [
        c.created for c in response.context["news"].comment_set.all()
    ]
    assert remark_timestamps == sorted(remark_timestamps)


def test_non_auth_client_no_form(client, post_instance, post_url):
    response = client.get(post_url)
    assert "form" not in response.context


def test_auth_user_has_comment_form(
    random_user_client, post_instance, post_url
):
    response = random_user_client.get(post_url)
    form_in_context = response.context.get("form")
    assert isinstance(form_in_context, CommentForm)
