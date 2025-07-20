# tests/test_integration.py

import os
import yaml
import json
import pandas as pd
import pytest

from pipeline import main as pipeline_main

def test_end_to_end_pipeline(tmp_path, monkeypatch):
    # 1) Build a tiny CSV
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    csv_path = data_dir / "iris.csv"
    df = pd.DataFrame({
        "feat":  [0, 1, 0, 1],
        "label": [0, 0, 1, 1]
    })
    df.to_csv(csv_path, index=False)
    # print(df.head())
    # 2) Write a one‑off config.yml pointing at tmp data + outputs
    config = {
        "data_source": {
            "type": "local",
            "path": str(csv_path)
        },
        "training": {
            "test_size": 0.5,
            "random_state": 42,
            "hyperparameters": {"solver": "lbfgs"},
            "model_output_path": str(tmp_path / "model.joblib"),
            "metrics_output_path": str(tmp_path / "metrics.json")
        },
        "evaluation": {
            "labels": ["class0", "class1"],
            "plot_confusion": False
        }
    }
    cfg_file = tmp_path / "config.yml"
    cfg_file.write_text(yaml.dump(config))

    # 3) Ensure relative paths inside your pipeline resolve to tmp_path
    monkeypatch.chdir(tmp_path)

    # 4) Kick off the pipeline
    pipeline_main(str(cfg_file))

    # 5) Verify artifacts exist
    model_file   = tmp_path / "model.joblib"
    metrics_file = tmp_path / "metrics.json"
    assert model_file.exists(), "Expected the trained model to be saved"
    assert metrics_file.exists(), "Expected the metrics JSON to be saved"

    # 6) Load and sanity‑check metrics
    metrics = json.loads(metrics_file.read_text())
    assert "accuracy" in metrics
    # accuracy must be a float between 0 and 1
    acc = metrics["accuracy"]
    assert isinstance(acc, float)
    assert 0.0 <= acc <= 1.0
