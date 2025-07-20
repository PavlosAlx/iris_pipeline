import pandas as pd
import numpy as np
import pytest
from data_preprocess import DataPreprocessor

@pytest.fixture
def raw_df():
    return pd.DataFrame({
        "feat1": [1.0, np.nan, 3.0],
        "feat2": [4.0, 5.0, np.nan],
        "label": [0, 1, 0]
    })

def test_clean_imputes_mean(raw_df):
    dp = DataPreprocessor({"test_size": 0.2, "random_state": 42})
    cleaned = dp.clean(raw_df.copy())
    assert cleaned.loc[1, "feat1"] == pytest.approx(2.0)
    assert cleaned.loc[2, "feat2"] == pytest.approx(4.5)

def test_scale_zero_mean_unit_var(raw_df):
    dp = DataPreprocessor({"test_size": 0.2, "random_state": 42})
    cleaned = dp.clean(raw_df.copy())
    scaled = dp.scale(cleaned, ["feat1", "feat2"])
    # After scaling, mean≈0
    assert abs(scaled["feat1"].mean()) < 1e-6
    # And population std (ddof=0) ≈ 1
    assert pytest.approx(scaled["feat2"].std(ddof=0), rel=1e-2) == 1.0

def test_process_splits_correctly(raw_df):
    # Duplicate so stratify works
    df = pd.concat([raw_df, raw_df], ignore_index=True)
    dp = DataPreprocessor({"test_size": 0.5, "random_state": 0})
    X_tr, X_te, y_tr, y_te = dp.process(df, label_col="label")
    assert len(X_tr) == 3
    assert len(X_te) == 3
    assert set(y_tr.unique()) <= set(df["label"].unique())
    assert set(y_te.unique()) <= set(df["label"].unique())
