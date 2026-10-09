import pytest
from logging import getLogger

from src.config import Config


def test_env_overrides(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("TG_API_ID", "42")
    monkeypatch.setenv("TG_API_HASH", "h")
    monkeypatch.setenv("TG_BOT_TOKEN", "1:t")
    config = Config(getLogger())
    config.load_config("config.yaml")
    assert config.data["tech"] == {"api_id": 42, "api_hash": "h", "bot_token": "1:t"}


def test_missing_file_creates_template(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    for name in ("TG_API_ID", "TG_API_HASH", "TG_BOT_TOKEN"):
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(Exception):
        Config(getLogger()).load_config("config.yaml")
    assert (tmp_path / "config.yaml").exists()
