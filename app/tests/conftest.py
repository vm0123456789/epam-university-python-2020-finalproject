import pytest

from app import create_app


@pytest.fixture
def app_context(scope="session"):
    app = create_app(testing=True)
    with app.app_context():
        return app


@pytest.fixture
def client(app_context):
    app = create_app(testing=True)
    app_ctx = app.app_context()
    app_ctx.push()
    client = app.test_client(use_cookies=True)
    yield client


