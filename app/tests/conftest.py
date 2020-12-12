import json

import pytest
import os
import requests
from app import create_app, db

basedir = os.path.abspath(os.path.dirname(__file__))
baseurl = 'http://127.0.0.1:5000'

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
    db.init_app(app)
    db.create_all()
    yield client
    db.drop_all()
    app_ctx.pop()
