# import yaml
# import tempfile
# import os
# import pytest
# from src.config import Config

import os
import yaml
import tempfile
from src.config import Config

def test_config_loads(tmp_path, monkeypatch):
    # Create a temp YAML
    cfg_file = tmp_path / "cfg.yml"
    data = {"foo": {"bar": 123}}
    cfg_file.write_text(yaml.dump(data))

    cfg = Config(str(cfg_file))
    assert cfg["foo"]["bar"] == 123
    assert cfg.get("nonexistent", "default") == "default"


# def test_load_config_from_path(tmp_path):
#     sample = {"alpha": {"beta": 42}}
#     cfg_file = tmp_path / "custom.yml"
#     cfg_file.write_text(yaml.dump(sample))

#     cfg = Config(str(cfg_file))
#     assert cfg["alpha"]["beta"] == 42
#     assert cfg.get("nope", "def") == "def"

# def test_default_path(tmp_path, monkeypatch):
#     # Create a fake project structure: <tmp>/proj/src/config.py + <tmp>/proj/config.yml
#     proj = tmp_path / "proj"
#     srcdir = proj / "src"
#     srcdir.mkdir(parents=True)
#     # Write a config.yml in the project root
#     cfg_file = proj / "config.yml"
#     sample = {"x": 7}
#     cfg_file.write_text(yaml.dump(sample))
#     # Monkey‑patch __file__ inside src/config.py to live under srcdir
#     fake_file = srcdir / "config.py"
#     fake_file.write_text("# dummy")
#     monkeypatch.setenv("PYTHONPATH", str(proj))  # ensure project is on path
#     # Now Config() with no args should pick up <proj>/config.yml
#     cfg = Config()
#     assert cfg["x"] == 7

# def test_missing_file_raises():
#     with pytest.raises(FileNotFoundError):
#         Config("/this/path/does_not_exist.yml")
