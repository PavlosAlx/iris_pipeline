# tests/test_train.py

import pandas as pd
import pytest
import json
from src.train import ModelTrain

@pytest.fixture
def small_data():
    """
    Minimal perfectly separable dataset:
    - One feature 'x'
    - Two classes 0 and 1
    """
    X = pd.DataFrame({"x": [0, 1]})
    y = pd.Series([0, 1])
    return X, y

def test_train_and_evaluate(tmp_path, small_data):
    X, y = small_data

    # Initialize trainer with tiny synthetic data config
    trainer = ModelTrain(
        train_cfg={
            "random_state": 0,
            "hyperparameters": {"solver": "lbfgs"},
            "model_output_path": str(tmp_path / "model.joblib"),
            "metrics_output_path": str(tmp_path / "metrics.json")
        },
        eval_cfg={"labels": ["class0", "class1"]}
    )

    # Train & evaluate on the same data (should yield perfect accuracy)
    model = trainer.train(X, y)
    metrics = trainer.evaluate(X, y)
    assert metrics["accuracy"] == pytest.approx(1.0)

    # Persist artifacts
    trainer.save_model()
    trainer.save_metrics(metrics)

    # Verify files were created
    model_file = tmp_path / "model.joblib"
    metrics_file = tmp_path / "metrics.json"
    assert model_file.exists(), "Expected the model.joblib file to be saved"
    assert metrics_file.exists(), "Expected the metrics.json file to be saved"

    # Reload metrics and double‑check accuracy
    saved = json.loads(metrics_file.read_text())
    assert saved["accuracy"] == pytest.approx(1.0)
