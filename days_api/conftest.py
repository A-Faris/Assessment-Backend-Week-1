"""This file contains fixtures for testing the API."""

# pylint: skip-file

import pytest

from app import app, app_history


@pytest.fixture
def test_app():
    """Returns a test version of the API."""
    return app.test_client()


@pytest.fixture(autouse=True)
def run_around_tests():
    """Resets history in between tests."""
    app_history.clear()
    yield
    app_history.clear()
