"""Tests for auto-update: check, version compare, signature, apply."""

import json
from unittest.mock import MagicMock, patch

import pytest

from maya_theme.core import update


@pytest.fixture(autouse=True)
def _config(tmp_path, monkeypatch):
    import maya_theme.core.config as c

    monkeypatch.setattr(c, "MAYA_HOME", tmp_path / "maya")
    monkeypatch.setattr(c, "CONFIG_FILE", tmp_path / "maya/config.json")
    monkeypatch.setattr(c, "STATE_DIR", tmp_path / "state")
    monkeypatch.setattr(c, "BACKUP_DIR", tmp_path / "backups")
    (tmp_path / "maya").mkdir(parents=True)
    c.save_config(c.DEFAULT_CONFIG)


def test_version_gt():
    assert update._version_gt("0.2.0", "0.1.0") is True
    assert update._version_gt("0.1.0", "0.1.0") is False
    assert update._version_gt("0.1.0", "0.2.0") is False
    assert update._version_gt("1.0.0", "0.9.9") is True


def test_check_update_no_source():
    r = update.check_update()
    assert r["available"] is False
    assert "no update source" in r.get("reason", "")


def test_check_update_disabled():
    # configure a source but disable checks
    import maya_theme.core.config as c

    cfg = c.load_config()
    cfg["privacy"]["update_url"] = "https://example.com/manifest.json"
    cfg["privacy"]["update_checks"] = False
    c.save_config(cfg)
    r = update.check_update()
    assert r["available"] is False
    assert "disabled" in r.get("reason", "")


def test_check_update_available():
    import maya_theme.core.config as c

    cfg = c.load_config()
    cfg["privacy"]["update_url"] = "https://example.com/manifest.json"
    cfg["privacy"]["update_checks"] = True
    c.save_config(cfg)

    manifest = {"version": "0.2.0", "changelog": "new stuff", "url": "https://example.com/update.zip", "checksum": "abc"}
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps(manifest).encode()
    mock_response.__enter__ = lambda self: self
    mock_response.__exit__ = lambda *a: None

    with patch("urllib.request.urlopen", return_value=mock_response):
        r = update.check_update()
    assert r["available"] is True
    assert r["version"] == "0.2.0"


def test_apply_update_no_source():
    r = update.apply_update()
    assert r["success"] is False


def test_apply_update_checksum_mismatch():
    import maya_theme.core.config as c

    cfg = c.load_config()
    cfg["privacy"]["update_url"] = "https://example.com/manifest.json"
    cfg["privacy"]["update_checks"] = True
    c.save_config(cfg)

    manifest = {"version": "0.2.0", "url": "https://example.com/update.zip", "checksum": "wronghash"}
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps(manifest).encode()
    mock_response.__enter__ = lambda self: self
    mock_response.__exit__ = lambda *a: None

    # mock download to return different data
    with patch("urllib.request.urlopen", return_value=mock_response):
        with patch.object(update, "_download", return_value=b"different data"):
            r = update.apply_update()
    assert r["success"] is False
    assert "checksum" in r.get("error", "").lower()


def test_verify_signature_no_sig():
    assert update._verify_signature(b"data", "") is True


def test_verify_signature_no_gpg():
    with patch("shutil.which", return_value=None):
        assert update._verify_signature(b"data", "sig123") is False