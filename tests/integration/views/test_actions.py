import pytest
from django.contrib.auth.models import User
from django.test.client import HTTPStatus, Client

from postladneem_beats.models import Genre, Key


@pytest.fixture
def client():
    return Client()


def test_login_action__on_correct_credentials__should_pass(db, client):
    User.objects.create_user(username="test", password="1")
    client.logout()
    response = client.post("/login_action/", {"username": "test", "password": "1"})
    assert response.status_code == 302


def test_login_action__on_bad_credentials__should_fail(db, client):
    client.logout()
    response = client.post("/login_action/", {"username": "test", "password": "2"})
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_edit_action__on_id_lack_should_400(client):
    response = client.post("/edit_action/")
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_creation_action__on_get__should_405(db, client):
    response = client.get("/beats/")
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_creation_action__on_correct_body__should_pass(db, client):
    Genre.objects.create(name="Reggaeton")
    Key.objects.create(tonica="A", is_minor=True)
    client.post(
        "/beats/",
        {"name": "wug", "description": "E", "genre": "Reggaeton", "bpm": 120, "key": "Am", "file": "dsd.mp3"},
    )

    assert HTTPStatus.OK


def test_creation_action__on_empty_body__should_400(db, client):
    response = client.post("/beats/")
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_logout_action__on_authorized__should_clean_session(db, client):
    response = client.post("/logout/")
    assert response.status_code == 302


def test_logout_action__on_unauthorized__should_redirect(db, client):
    client.logout()
    response = client.post("/logout/")
    assert response.status_code == 302


def test_registration_action__on_authorized__should_replace_session(db, client):
    c = User.objects.count()
    client.post("/registration_action/", {"username": "test", "password": "2", "approval": "2"})
    assert User.objects.count() == c + 1


def test_registration_action__should_create_user(db, client):
    c = User.objects.count()
    client.post("/registration_action/", {"username": "test", "password": "2", "approval": "2"})
    assert User.objects.count() == c + 1


def test_registration_action__on_password_not_equals_approval__should_400(db, client):
    response = client.post("/registration_action/", {"username": "test", "password": "2", "approval": "3"})
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_registration_action__on_existent_user__should_login(db, client):
    User.objects.create_user(username="test", password="1")
    response = client.post("/registration_action/", {"username": "test", "password": "1", "approval": "1"})
    assert response.status_code == 302
