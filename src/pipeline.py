# src/pipeline.py

import pandas as pd
# Only import Airflow’s helper when running under Airflow
try:
    from airflow.operators.python import get_current_context
except ImportError:
    get_current_context = None

from data_loader import DataLoader
from data_preprocess import DataPreprocessor
from train import ModelTrain
from config import Config
from utils import setup_logging, get_logger

def load_data(config_path: str):
    """Load data using DataLoader and push real DataFrame to XCom."""
    setup_logging(
        log_file="logs/app.log",
        max_bytes=5_000_000,
        backup_count=3,
        level="DEBUG"
    )
    logger = get_logger(__name__)
    logger.info("Loading data...")
    cfg = Config(config_path)
    loader = DataLoader(cfg["data_source"])
    df = loader.load()
    return df  # real pd.DataFrame will be XCom‑pushed

def preprocess_data(config_path: str, df, **kwargs):
    """
    Preprocess data using DataPreprocessor.
    If `df` is a string (Jinja template), pull the real DataFrame from XCom.
    """
    # grab TaskInstance to fetch real objects
    ti = get_current_context()["ti"]

    # if df came in as templated string, replace with real DataFrame
    if isinstance(df, str):
        df = ti.xcom_pull(task_ids="load_data")

    logger = get_logger(__name__)
    logger.info("Preprocessing data...")

    cfg = Config(config_path)
    dp = DataPreprocessor(cfg["training"])
    X_train, X_test, y_train, y_test = dp.process(df, label_col="species")

    # return real numpy/pandas splits
    return X_train, X_test, y_train, y_test

def train_model(config_path: str, X_train, y_train, **kwargs):
    """
    Train model using ModelTrain.
    If X_train is a string, pull the real splits from XCom.
    """
    ti = get_current_context()["ti"]

    # if X_train is templated string, pull all splits
    if isinstance(X_train, str):
        splits = ti.xcom_pull(task_ids="preprocess_data")
        X_train, X_test, y_train, y_test = splits

    logger = get_logger(__name__)
    logger.info("Training model...")

    cfg = Config(config_path)
    trainer = ModelTrain(cfg["training"], cfg["evaluation"])
    model = trainer.train(X_train, y_train)

    # return both model and trainer so evaluate can reuse
    return model, trainer

def evaluate_model(config_path: str, model, trainer, X_test, y_test, **kwargs):
    """
    Evaluate model using ModelTrain.
    If X_test is a string, pull the real splits from XCom.
    """
    ti = get_current_context()["ti"]

    # If we got trainer as a string, pull the real (model, trainer) tuple
    if isinstance(trainer, str):
        model_trainer = ti.xcom_pull(task_ids="train_model")
        # train_model returned (model, trainer)
        _, trainer = model_trainer
    # if X_test is templated string, pull all splits
    if isinstance(X_test, str):
        splits = ti.xcom_pull(task_ids="preprocess_data")
        _, X_test, _, y_test = splits

    logger = get_logger(__name__)
    logger.info("Evaluating model...")

    # reuse the same trainer instance to evaluate & save
    metrics = trainer.evaluate(X_test, y_test)
    trainer.save_model()
    trainer.save_metrics(metrics)

    return metrics

def main(config_path: str):
    """Main pipeline function for standalone execution."""
    setup_logging(
        log_file="logs/app.log",
        max_bytes=5_000_000,
        backup_count=3,
        level="DEBUG"
    )
    logger = get_logger(__name__)
    logger.info("Pipeline starting...")

    # 1) Load
    df = load_data(config_path)

    # 2) Preprocess & split
    X_train, X_test, y_train, y_test = preprocess_data(config_path, df)

    # 3) Train
    model, trainer = train_model(config_path, X_train, y_train)

    # 4) Evaluate
    metrics = evaluate_model(config_path, model, trainer, X_test, y_test)

    logger.info("Pipeline completed successfully")

if __name__ == "__main__":
    # when running inside Docker/Airflow
    main("/opt/airflow/config.yml")
