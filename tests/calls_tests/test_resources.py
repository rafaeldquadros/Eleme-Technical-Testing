import json
from flask_jwt_extended import create_access_token


def test_create_call(test_client, seed_db):
    obj = {
        "priority_level": "MEDIO",
        "setor": "TI",
        "description": "Problema de teste",
    }
    print(seed_db)

    token = create_access_token(identity=seed_db["user_normal"].id)

    response = test_client.post(
        "/calls",
        data=json.dumps(obj),
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 200
    assert response.json["id"] is not None
    assert response.json["priority_level"] == "MEDIO"
    assert response.json["status"] == "Pendente"
    assert response.json["setor"] == "TI"
    assert response.json["description"] == "Problema de teste"
    assert response.json["createdAt"] is not None
    assert response.json["user_id"] == seed_db["user_normal"].id


def test_create_without_priority_level(test_client, seed_db):
    obj = {
        "setor": "TI",
        "description": "Problema de teste",
    }

    token = create_access_token(identity=seed_db["user_normal"].id)

    response = test_client.post(
        "/calls",
        data=json.dumps(obj),
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 400
    assert (
        response.json["message"]["priority_level"]
        == "Enter the priority level 'HIGH/MEDIUM/LOW"
    )


def test_create_without_sector(test_client, seed_db):
    obj = {
        "priority_level": "MEDIO",
        "description": "Problema de teste",
    }

    token = create_access_token(identity=seed_db["user_normal"].id)

    response = test_client.post(
        "/calls",
        data=json.dumps(obj),
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 400
    assert (
        response.json["message"]["setor"]
        == "Inform the sector you want to send the call"
    )


def test_create_without_description(test_client, seed_db):
    obj = {
        "priority_level": "MEDIO",
        "setor": "TI",
    }

    token = create_access_token(identity=seed_db["user_normal"].id)

    response = test_client.post(
        "/calls",
        data=json.dumps(obj),
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 400
    assert (
        response.json["message"]["description"]
        == "Please provide a description of your problem!"
    )


def test_create_call_without_authorization(test_client):
    obj = {
        "priority_level": "MEDIO",
        "setor": "TI",
        "description": "Problema de teste",
    }

    response = test_client.post(
        "/calls",
        data=json.dumps(obj),
        content_type="application/json",
    )

    assert response.status_code == 401
    assert response.json["msg"] == "Missing Authorization Header"


def test_get_all_calls(test_client, seed_db):
    token = create_access_token(
        identity=seed_db["user_normal"].id, additional_claims={"is_admin": True}
    )

    response = test_client.get(
        "/calls",
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["id"] is not None
    assert response.json[0]["priority_level"] == "ALTO"
    assert response.json[0]["status"] == "Pendente"
    assert response.json[0]["setor"] == "TI"
    assert response.json[0]["description"] == "teste"
    assert response.json[0]["user_id"] == seed_db["user_normal"].id


def test_get_all_calls_if_not_admin(test_client, seed_db):
    token = create_access_token(identity=seed_db["user_normal"].id)

    response = test_client.get(
        "/calls",
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 401
    assert response.json["message"] == "Your account is not an administrator"


def test_get_call_by_id_admin(test_client, seed_db):
    token = create_access_token(
        identity=seed_db["user_normal"].id, additional_claims={"is_admin": True}
    )

    response = test_client.get(
        "/calls/{}".format(seed_db["call"].id),
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 200
    assert response.json["id"] is not None
    assert response.json["priority_level"] == "ALTO"
    assert response.json["status"] == "Pendente"
    assert response.json["setor"] == "TI"
    assert response.json["description"] == "teste"
    assert response.json["user_id"] == seed_db["user_normal"].id


def test_get_call_by_id_if_is_owner(test_client, seed_db):
    token = create_access_token(identity=seed_db["user_normal"].id)

    response = test_client.get(
        "/calls/{}".format(seed_db["call"].id),
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 200
    assert response.json["id"] is not None
    assert response.json["priority_level"] == "ALTO"
    assert response.json["status"] == "Pendente"
    assert response.json["setor"] == "TI"
    assert response.json["description"] == "teste"
    assert response.json["user_id"] == seed_db["user_normal"].id


def test_get_call_by_id_if_not_admin(test_client, seed_db):
    token = create_access_token(identity=seed_db["user_normal_2"].id)

    response = test_client.get(
        "/calls/{}".format(seed_db["call"].id),
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 401
    assert (
        response.json["message"]
        == "You need to be a ticket owner or administrator to do this."
    )


def test_get_call_by_id_if_not_owner(test_client, seed_db):
    token = create_access_token(identity=seed_db["user_normal_2"].id)

    response = test_client.get(
        "/calls/{}".format(seed_db["call"].id),
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 401
    assert (
        response.json["message"]
        == "You need to be a ticket owner or administrator to do this."
    )


def test_update_call_description_if_admin(test_client, seed_db):
    token = create_access_token(
        identity=seed_db["user_admin"].id, additional_claims={"is_admin": True}
    )
    obj = {"description": "New description"}

    response = test_client.patch(
        "/calls/{}".format(seed_db["call"].id),
        data=json.dumps(obj),
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 200
    assert response.json["id"] is not None
    assert response.json["priority_level"] == "ALTO"
    assert response.json["status"] == "Pendente"
    assert response.json["setor"] == "TI"
    assert response.json["description"] == "New description"
    assert response.json["user_id"] == seed_db["user_normal"].id


def test_update_call_setor_if_admin(test_client, seed_db):
    token = create_access_token(identity=seed_db["user_normal"].id)
    obj = {"setor": "Administração"}

    response = test_client.patch(
        "/calls/{}".format(seed_db["call"].id),
        data=json.dumps(obj),
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 200
    assert response.json["id"] is not None
    assert response.json["priority_level"] == "ALTO"
    assert response.json["status"] == "Pendente"
    assert response.json["setor"] == "Administração"
    assert response.json["description"] == "teste"
    assert response.json["user_id"] == seed_db["user_normal"].id


def test_update_call_priority_level_if_admin(test_client, seed_db):
    token = create_access_token(
        identity=seed_db["user_admin"].id, additional_claims={"is_admin": True}
    )
    obj = {"priority_level": "BAIXO"}

    response = test_client.patch(
        "/calls/{}".format(seed_db["call"].id),
        data=json.dumps(obj),
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 200
    assert response.json["id"] is not None
    assert response.json["priority_level"] == "BAIXO"
    assert response.json["status"] == "Pendente"
    assert response.json["setor"] == "TI"
    assert response.json["description"] == "teste"
    assert response.json["user_id"] == seed_db["user_normal"].id


def test_update_call_description_if_owner(test_client, seed_db):
    token = create_access_token(
        identity=seed_db["user_admin"].id, additional_claims={"is_admin": True}
    )
    obj = {"description": "New description"}

    response = test_client.patch(
        "/calls/{}".format(seed_db["call"].id),
        data=json.dumps(obj),
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 200
    assert response.json["id"] is not None
    assert response.json["priority_level"] == "ALTO"
    assert response.json["status"] == "Pendente"
    assert response.json["setor"] == "TI"
    assert response.json["description"] == "New description"
    assert response.json["user_id"] == seed_db["user_normal"].id


def test_update_call_setor_if_owner(test_client, seed_db):
    token = create_access_token(identity=seed_db["user_normal"].id)
    obj = {"setor": "Administração"}

    response = test_client.patch(
        "/calls/{}".format(seed_db["call"].id),
        data=json.dumps(obj),
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 200
    assert response.json["id"] is not None
    assert response.json["priority_level"] == "ALTO"
    assert response.json["status"] == "Pendente"
    assert response.json["setor"] == "Administração"
    assert response.json["description"] == "teste"
    assert response.json["user_id"] == seed_db["user_normal"].id


def test_update_call_priority_level_if_owner(test_client, seed_db):
    token = create_access_token(identity=seed_db["user_normal"].id)
    obj = {"priority_level": "BAIXO"}

    response = test_client.patch(
        "/calls/{}".format(seed_db["call"].id),
        data=json.dumps(obj),
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 200
    assert response.json["id"] is not None
    assert response.json["priority_level"] == "BAIXO"
    assert response.json["status"] == "Pendente"
    assert response.json["setor"] == "TI"
    assert response.json["description"] == "teste"
    assert response.json["user_id"] == seed_db["user_normal"].id


def test_update_call_description_if_not_owner(test_client, seed_db):
    token = create_access_token(identity=seed_db["user_normal_2"].id)
    obj = {"description": "New description"}

    response = test_client.patch(
        "/calls/{}".format(seed_db["call"].id),
        data=json.dumps(obj),
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 401
    assert (
        response.json["message"]
        == "You need to be a ticket owner or administrator to do this."
    )


def test_update_call_setor_if_not_owner(test_client, seed_db):
    token = create_access_token(identity=seed_db["user_normal_2"].id)
    obj = {"setor": "Administração"}

    response = test_client.patch(
        "/calls/{}".format(seed_db["call"].id),
        data=json.dumps(obj),
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 401
    assert (
        response.json["message"]
        == "You need to be a ticket owner or administrator to do this."
    )


def test_update_call_priority_level_if_not_owner(test_client, seed_db):
    token = create_access_token(identity=seed_db["user_normal_2"].id)
    obj = {"priority_level": "BAIXO"}

    response = test_client.patch(
        "/calls/{}".format(seed_db["call"].id),
        data=json.dumps(obj),
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 401
    assert (
        response.json["message"]
        == "You need to be a ticket owner or administrator to do this."
    )


def test_update_call_with_a_invalid_id(test_client, seed_db):
    token = create_access_token(identity=seed_db["user_normal_2"].id)
    obj = {"priority_level": "BAIXO"}

    response = test_client.patch(
        "/calls/{}".format(98394),
        data=json.dumps(obj),
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 404
    assert response.json["message"] == "Call not found"


def test_delete_call_if_admin(test_client, seed_db):
    token = create_access_token(
        identity=seed_db["user_admin"].id, additional_claims={"is_admin": True}
    )

    response = test_client.delete(
        "/calls/{}".format(seed_db["call"].id),
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 200
    assert response.json["message"] == "Call deleted successfully"


def test_delete_call_if_owner(test_client, seed_db):
    token = create_access_token(identity=seed_db["user_normal"].id)

    response = test_client.delete(
        "/calls/{}".format(seed_db["call"].id),
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 200
    assert response.json["message"] == "Call deleted successfully"


def test_delete_call_if_not_owner_or_admin(test_client, seed_db):
    token = create_access_token(identity=seed_db["user_normal_2"].id)

    response = test_client.delete(
        "/calls/{}".format(seed_db["call"].id),
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 401
    assert (
        response.json["message"]
        == "You need to be a ticket owner or administrator to do this."
    )


def test_delete_call_with_invalid_id(test_client, seed_db):
    token = create_access_token(identity=seed_db["user_admin"].id)

    response = test_client.delete(
        "/calls/{}".format(8748374),
        content_type="application/json",
        headers={"Authorization": "Bearer {}".format(token)},
    )

    assert response.status_code == 404
    assert response.json["message"] == "Call not found"
