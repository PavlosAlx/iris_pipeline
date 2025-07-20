# 

import sys
from pathlib import Path
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Make sure Python can import your src/ modules
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from pipeline import load_data, preprocess_data, train_model, evaluate_model

default_args = {
    "owner": "Pavlos Alexias",
    "depends_on_past": False,
    "start_date": datetime(2025, 7, 20),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="iris_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    max_active_runs=1,
    tags=["iris", "ml"],
) as dag:

    load = PythonOperator(
        task_id="load_data",
        python_callable=load_data,
        op_kwargs={"config_path": str(PROJECT_ROOT / "config.yml")},
    )

    preprocess = PythonOperator(
        task_id="preprocess_data",
        python_callable=preprocess_data,
        op_kwargs={
            "config_path": str(PROJECT_ROOT / "config.yml"),
            "df": "{{ ti.xcom_pull(task_ids='load_data') }}",
        },
    )

    train = PythonOperator(
        task_id="train_model",
        python_callable=train_model,
        op_kwargs={
            "config_path": str(PROJECT_ROOT / "config.yml"),
            "X_train": "{{ ti.xcom_pull(task_ids='preprocess_data')[0] }}",
            "y_train": "{{ ti.xcom_pull(task_ids='preprocess_data')[2] }}",
        },
    )

    evaluate = PythonOperator(
        task_id="evaluate_model",
        python_callable=evaluate_model,
        op_kwargs={
            "config_path": str(PROJECT_ROOT / "config.yml"),
            "model": "{{ ti.xcom_pull(task_ids='train_model')[0] }}",
            "trainer": "{{ ti.xcom_pull(task_ids='train_model')[1] }}",
            "X_test": "{{ ti.xcom_pull(task_ids='preprocess_data')[1] }}",
            "y_test": "{{ ti.xcom_pull(task_ids='preprocess_data')[3] }}",
        },
    )

    # Define execution order
    load >> preprocess >> train >> evaluate