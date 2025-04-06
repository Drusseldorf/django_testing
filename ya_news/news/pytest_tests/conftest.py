from datetime import datetime, timedelta

import pytest
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.fixture
def post_instance(db):
    return News.objects.create(title="Заголовок поста", text="Текст поста")


@pytest.fixture
def writer(django_user_model):
    return django_user_model.objects.create(username="WriterUser")


@pytest.fixture
def writer_client(writer):
    auth_client = Client()
    auth_client.force_login(writer)
    return auth_client


@pytest.fixture
def random_user(django_user_model):
    return django_user_model.objects.create(username="RandomUser")


@pytest.fixture
def random_user_client(random_user):
    auth_client = Client()
    auth_client.force_login(random_user)
    return auth_client


@pytest.fixture
def remark(writer, post_instance, db):
    return Comment.objects.create(
        news=post_instance, author=writer, text="Текст комментария"
    )


@pytest.fixture
def sample_posts(db):
    News.objects.bulk_create(
        News(
            title=f"Заголовок {idx + 1}",
            text=f"Содержимое поста {idx + 1}",
            date=datetime.today() - timedelta(days=idx),
        )
        for idx in range(NEWS_COUNT_ON_HOME_PAGE)
    )


@pytest.fixture
def sample_remarks(writer, post_instance, db):
    for idx in range(15):
        new_comment = Comment.objects.create(
            news=post_instance, author=writer, text=f"Комментарий №{idx}"
        )
        new_comment.created = timezone.now() + timedelta(days=idx)
        new_comment.save()


@pytest.fixture
def main_page_url():
    return reverse("news:home")


@pytest.fixture
def user_login_url():
    return reverse("users:login")


@pytest.fixture
def user_logout_url():
    return reverse("users:logout")


@pytest.fixture
def user_signup_url():
    return reverse("users:signup")


@pytest.fixture
def post_url(post_instance):
    return reverse("news:detail", args=(post_instance.id,))


@pytest.fixture
def remark_edit_url(remark):
    return reverse("news:edit", args=(remark.id,))


@pytest.fixture
def remark_delete_url(remark):
    return reverse("news:delete", args=(remark.id,))


@pytest.fixture
def forced_remark_edit_url(user_login_url, remark_edit_url):
    return f"{user_login_url}?next={remark_edit_url}"


@pytest.fixture
def forced_remark_delete_url(user_login_url, remark_delete_url):
    return f"{user_login_url}?next={remark_delete_url}"


@pytest.fixture
def forced_post_comments_redirect(post_url):
    return f"{post_url}#comments"
