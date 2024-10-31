import pytest
from app import create_app
from config import Config

class TestConfig(Config):
    TESTING = True
    POSTGRES_URI = 'postgresql://localhost/criminalcode_test'

@pytest.fixture
def app():
    app = create_app(TestConfig)
    return app

@pytest.fixture
def client(app):
    return app.test_client() 