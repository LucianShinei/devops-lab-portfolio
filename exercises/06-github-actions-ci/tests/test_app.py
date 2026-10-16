import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

APP_DIR = Path(__file__).resolve().parents[3] / "exercises" / "05-docker-compose-flask"
sys.path.insert(0, str(APP_DIR))

import app as flask_app

@pytest.fixture
def client():
    flask_app.app.config.update(TESTING=True)
    with flask_app.app.test_client() as test_client:
        yield test_client


def test_health_returns_healthy(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_home_records_visit_and_returns_counts(client):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_connection.is_connected.return_value = True

    with patch.object(flask_app.redis_client, "incr", return_value=1) as mock_incr:
        with patch.object(flask_app, "get_mysql_connection", return_value=mock_connection):
            response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {
        "message": "Flask + Redis + MySQL are working!",
        "redis_visit_count": 1,
        "mysql_total_visits": 1
    }
    mock_incr.assert_called_once_with("page_visits")
    mock_connection.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()


def test_home_returns_503_when_mysql_is_unavailable(client):
    with patch.object(flask_app.redis_client, "incr", return_value=3):
        with patch.object(flask_app, "get_mysql_connection", side_effect=RuntimeError("database unavailable")):
            response = client.get("/")

    assert response.status_code == 503
    assert response.get_json() == {
        "error": "Unable to connect to the backing services"
    }
