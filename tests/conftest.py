from app import create_app
import pytest


@pytest.fixture(scope="module")
def test_client():
    client = create_app()

    with client.test_client() as testing_client:
        with client.app_context():
            yield testing_client
