import json


def test_create_user_admin(test_client):
    obj = {
        "name": "Rafael",
        "email": "rafael@mail.com",
        "password": "1234",
        "isAdmin": True,
    }

    response = test_client.post(
        "/users", data=json.dumps(obj), content_type="application/json"
    )

    assert response.status_code == 200
    assert response.json["id"] is not None
    assert response.json["name"] == "Rafael"
    assert response.json["isAdmin"] == True
    assert "password" not in response.json


def test_create_user(test_client):
    obj = {
        "name": "Rafael",
        "email": "rafael@mail.com",
        "password": "1234",
    }

    response = test_client.post(
        "/users", data=json.dumps(obj), content_type="application/json"
    )

    assert response.status_code == 200
    assert response.json["id"] is not None
    assert response.json["name"] == "Rafael"
    assert "password" not in response.json


def test_create_user_without_name(test_client):
    obj = {
        "email": "rafael@mail.com",
        "password": "1234",
    }

    response = test_client.post(
        "/users", data=json.dumps(obj), content_type="application/json"
    )

    assert response.status_code == 400
    assert response.json["message"]["name"] == "Name is a required field"


def test_create_user_without_password(test_client):
    obj = {
        "name": "Rafael",
        "email": "rafael@mail.com",
    }

    response = test_client.post(
        "/users", data=json.dumps(obj), content_type="application/json"
    )

    assert response.status_code == 400
    assert response.json["message"]["password"] == "Password is a required field"


def test_create_user_without_email(test_client):
    obj = {
        "name": "Rafael",
        "password": "1234",
    }

    response = test_client.post(
        "/users", data=json.dumps(obj), content_type="application/json"
    )

    assert response.status_code == 400
    assert response.json["message"]["email"] == "Email is a required field"


def test_create_user_with_existing_email(test_client, seed_db):
    obj = {
        "name": "Rafael",
        "email": "rafael@mail.com",
        "password": "1234",
        "isAdmin": True,
    }
    print(seed_db)

    response = test_client.post(
        "/users", data=json.dumps(obj), content_type="application/json"
    )

    assert response.status_code == 400
    assert response.json[
        "message"
    ] == "There is already a user registered with this email: {}".format(seed_db.email)
