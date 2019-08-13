# conftest.py - This is used to configure pytest to have a fixture for the Flask App
import pytest

from conda_parser import create_app


@pytest.fixture
def app():
    app = create_app()
    app.debug = True
    return app
