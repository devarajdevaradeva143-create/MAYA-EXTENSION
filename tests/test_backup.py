import json

from maya_theme.core import backup


def test_export_import_roundtrip(tmp_path, monkeypatch):
    import maya_theme.core.config as c

    home = tmp_path
    monkeypatch.setattr(c, "MAYA_HOME", home / ".local/share/maya-theme")
    monkeypatch.setattr(c, "CONFIG_FILE", home / ".local/share/maya-theme/config.json")
    monkeypatch.setattr(c, "STATE_DIR", home / ".local/state/maya-theme")
    monkeypatch.setattr(c, "BACKUP_DIR", home / ".local/share/maya-theme/backups")
    (home / ".local/share/maya-theme").mkdir(parents=True)
    c.save_config(c.DEFAULT_CONFIG)

    out = tmp_path / "bundle.json"
    backup.export_bundle(out)
    assert out.exists()
    data = json.loads(out.read_text())
    assert data["version"] == c.DEFAULT_CONFIG["version"]

    # modify then import
    data["glass"] = {"enabled": False, "blur": 5}
    out2 = tmp_path / "bundle2.json"
    out2.write_text(json.dumps(data))
    # import validates version present
    cfg = backup.import_bundle(out2)
    assert cfg["glass"]["blur"] == 5


def test_backup_create_and_list(tmp_path, monkeypatch):
    import maya_theme.core.config as c

    monkeypatch.setattr(c, "MAYA_HOME", tmp_path / "maya")
    monkeypatch.setattr(c, "CONFIG_FILE", tmp_path / "maya/config.json")
    monkeypatch.setattr(c, "STATE_DIR", tmp_path / "state")
    monkeypatch.setattr(c, "BACKUP_DIR", tmp_path / "backups")
    (tmp_path / "maya").mkdir()
    c.save_config(c.DEFAULT_CONFIG)
    monkeypatch.setattr(backup, "BACKUP_DIR", tmp_path / "backups")
    monkeypatch.setattr(backup, "MAYA_HOME", tmp_path / "maya")
    p = backup.create_backup("test")
    assert p.exists()
    assert (p / "meta.json").exists()
    assert len(backup.list_backups()) >= 1