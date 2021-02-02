from flask_testing import TestCase

from ..data_access import app

class TestBase(TestCase):
    def create_app(self):
        app.config.update(SQLALCHEMY_DATABASE_URI="mssql+pyodbc://BLBAPP:abby@DESKTOP-4K1BGVB/BLB_DB?driver=SQL+Server",
                SECRET_KEY='TEST_SECRET_KEY',
                DEBUG=True
                )
        return app

