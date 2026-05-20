import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient and restore the in-memory `activities` after each test."""
    snapshot = copy.deepcopy(activities)
    client = TestClient(app)
    yield client
    # restore activities to original state to keep tests isolated
    activities.clear()
    activities.update(snapshot)
