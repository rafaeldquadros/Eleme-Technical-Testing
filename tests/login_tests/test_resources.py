import json


def test_login_with_valid_email_and_password(test_client, seed_db):
    obj = {"email": "rafael@mail.com", "password": "1234"}

    response = test_client.post(
        "/login", data=json.dumps(obj), content_type="application/json"
    )

    assert response.status_code == 200
    assert response.json["access_token"] is not None


def test_login_without_password(test_client):
    obj = {"email": "rafael@mail.com"}

    response = test_client.post(
        "/login", data=json.dumps(obj), content_type="application/json"
    )

    assert response.status_code == 400
    assert response.json["message"]["password"] == "Password is a required field"


def test_login_without_email(test_client):
    obj = {"password": "1234"}

    response = test_client.post(
        "/login", data=json.dumps(obj), content_type="application/json"
    )

    assert response.status_code == 400
    assert response.json["message"]["email"] == "Email is a required field"


def test_login_with_invalid_email(test_client):
    obj = {"email": "error@mail.com", "password": "1234"}

    response = test_client.post(
        "/login", data=json.dumps(obj), content_type="application/json"
    )

    assert response.status_code == 404
    assert response.json["message"] == "Invalid email or password"


def test_login_with_invalid_password(test_client):
    obj = {"email": "rafael@mail.com", "password": "12345"}

    response = test_client.post(
        "/login", data=json.dumps(obj), content_type="application/json"
    )

    assert response.status_code == 404
    assert response.json["message"] == "Invalid email or password"
