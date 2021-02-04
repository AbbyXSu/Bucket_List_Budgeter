import pytest
from src.data_access import app
WTF_CSRF_ENABLED = False
@pytest.fixture(scope='module')
def test_client():
    flask_app = app
    app.testing = True
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client
