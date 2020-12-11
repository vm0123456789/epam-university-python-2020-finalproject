import os
import pytest

from app import create_app


@pytest.fixture
def app_context(scope="class"):
    basedir = os.path.abspath(os.path.dirname(__file__))
    baseurl = 'http://127.0.0.1:5000'

    app = create_app(testing=True)
    with app.app_context():
        yield app

