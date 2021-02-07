from src import BLBDB_APP_URI
from flask_testing import TestCase

from ..data_access import app

class TestBase(TestCase):
    def create_app(self):
        app.config.update(SQLALCHEMY_DATABASE_URI=BLBDB_APP_URI,
                SECRET_KEY='TEST_SECRET_KEY',
                DEBUG=True
                )
        return app

