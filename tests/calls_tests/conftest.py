from db import db
from users.model import UsersModel
from calls.model import CallsModel

import pytest


@pytest.fixture()
def seed_db():
    user_admin = UsersModel("Admin", "admin@mail.com", "1234", True)
    db.session.add(user_admin)
    db.session.commit()

    user_normal = UsersModel("Rafael", "rafael@mail.com", "1234", False)
    db.session.add(user_normal)
    db.session.commit()

    user_normal_2 = UsersModel("Rafael", "rafael2@mail.com", "1234", False)
    db.session.add(user_normal)
    db.session.commit()

    call = CallsModel(
        description="teste",
        priority_level="ALTO",
        setor="TI",
        user_id=user_normal.id,
        status="Pendente",
    )
    db.session.add(call)
    db.session.commit()

    yield {
        "user_admin": user_admin,
        "user_normal": user_normal,
        "call": call,
        "user_normal_2": user_normal_2,
    }


@pytest.fixture(scope="function", autouse=True)
def clear_db():
    db.session.query(CallsModel).delete()
    db.session.query(UsersModel).delete()
    db.session.commit()
