import pytest
from django.contrib.auth.models import User
from django.test.client import HTTPStatus, Client

from postladneem_beats.models import Beat, Genre, Key


@pytest.fixture
def client():
    return Client()


def test_login_page__loads_successfully(client):
    response = client.get("/login/")
    assert response.status_code == HTTPStatus.OK


def test_registration_page__loads_successfully(client):
    response = client.get("/registration/")
    assert response.status_code == HTTPStatus.OK


def test_feed_page__loads_successfully(db, client):
    response = client.get("/feed/")
    assert response.status_code == HTTPStatus.OK


def test_creation_page__loads_successfully(db, client):
    response = client.get("/creation/")
    assert response.status_code == HTTPStatus.OK


def test_root_page__on_unauthorized__redirects_to_login(db):
    client = Client()
    client.logout()
    response = client.get("/")
    assert response.status_code == HTTPStatus.MOVED_PERMANENTLY


def test_root_page__on_authorized__redirects_to_feed(db):
    User.objects.create_user(username="test", password="1")
    client = Client()
    client.login(username="test", password="1")
    response = client.get("/")
    assert response.status_code == HTTPStatus.MOVED_PERMANENTLY
    assert response.url == "/feed/"


def test_feed_page__on_unauthorized__should_redirect_to_login(db):
    client = Client()
    client.logout()
    response = client.get("/feed/")
    assert response.status_code == HTTPStatus.OK


def test_edit_page__without_id_provided__should_400(db):
    client = Client()
    client.logout()

    response = client.get("/edit/")
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_edit_page__on_unauthorized__should_redirect_to_login(db):
    client = Client()
    client.logout()
    Beat.objects.create(pk=1, name="test", bpm=120, genre=Genre.objects.create(), key=Key.objects.create(is_minor=True))
    response = client.get("/edit/?id=1")
    assert response.status_code == HTTPStatus.OK


def test_creation_page__on_unauthorized__should_redirect_to_login(db):
    client = Client()
    client.logout()
    response = client.get("/creation/")
    assert response.status_code == HTTPStatus.OK
