import pytest
from webapp.main.app import app


@pytest.fixture()
def app_fixture():
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(app_fixture):
    return app_fixture.test_client()


@pytest.fixture()
def runner(app_fixture):
    return app_fixture.test_cli_runner()