import os
import yaml
import tempfile
from config import Config

def test_config_loads(tmp_path, monkeypatch):
    # Create a temp YAML
    cfg_file = tmp_path / "cfg.yml"
    data = {"foo": {"bar": 123}}
    cfg_file.write_text(yaml.dump(data))

    cfg = Config(str(cfg_file))
    assert cfg["foo"]["bar"] == 123
    assert cfg.get("nonexistent", "default") == "default"