import pytest
from unittest.mock import patch
from config import get_db_url, get_auth_data, get_db_asterisk_url, get_pass, get_filter_minus_days_from  # Импортируем тестируемую функцию

@pytest.fixture
def mock_settings(monkeypatch):
    # Альтернатива: мокаем через monkeypatch
    monkeypatch.setattr('config.settings.SECRET_KEY', 'fixture_secret')
    monkeypatch.setattr('config.settings.ALGORITHM', 'fixture_HS512')
    monkeypatch.setattr('config.settings.ADMIN_LOGIN', 'login')
    monkeypatch.setattr('config.settings.START_PASS', 'password')
    monkeypatch.setattr('config.settings.CONN_STR', 'conn_str')
    monkeypatch.setattr('config.settings.CONN_STR_ASTERISK', 'conn_str_asterisk')
    monkeypatch.setattr('config.settings.AUDIO_PATH', 'audio_path')
    monkeypatch.setattr('config.settings.FILTER_MINUS_DAYS_FROM', 5)

def test_config_get_db_url(mock_settings):
    result = get_db_url()
    assert result == "conn_str"

def test_config_get_db_asterisk_url(mock_settings):
    result = get_db_asterisk_url()
    assert result == "conn_str_asterisk"

def test_config_get_auth_data(mock_settings):
    result = get_auth_data()
    assert result == {
        "secret_key": "fixture_secret",
        "algorithm": "fixture_HS512"
    }

def test_config_get_pass(mock_settings):
    result = get_pass()
    assert result == {
        "login": "login",
        "pass": "password"
    }

def test_config_get_filter_minus_days_from(mock_settings):
    result = get_filter_minus_days_from()
    assert isinstance(result, int)
    assert result == 5

