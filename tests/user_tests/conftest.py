import pytest
from db import db
from users.model import UsersModel
from calls.model import CallsModel


@pytest.fixture()
def seed_db():
    user = UsersModel("Rafael", "rafael@mail.com", "1234", False)
    db.session.add(user)
    db.session.commit()

    yield user


@pytest.fixture(scope="function", autouse=True)
def clear_db():
    db.session.query(CallsModel).delete()
    db.session.query(UsersModel).delete()
    db.session.commit()
