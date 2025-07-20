# Iris Classification Pipeline

A modular, production‑ready machine‑learning pipeline for the Iris dataset, fully tested and orchestrated with Apache Airflow in Docker.  This README documents the steps and design decisions taken from project inception through to Dockerized scheduling—so you can see how it all fits together.

---

## Complete PoC Airflow 

![alt text](/images/image.png)
![alt text](/images/image1.png)
![alt text](/images/image2.png)

## Unit tests 

![alt text](/images/image3.png)



## 🚀 Overview & Motivation

1. **Modular design**  
   - Each concern lives in its own class:  
     - `DataLoader` (local/S3 data access)  
     - `DataPreprocessor` (imputation, scaling, stratified split)  
     - `ModelTrain` (train, evaluate, save model & metrics)  

2. **Configuration‑driven**  
   - All paths and hyperparameters live in `config.yml`  
   - Single entrypoint reads YAML, instantiates each module  

3. **Robust logging**  
   - `utils.setup_logging()` configures rotating‐file + console handlers  (at the moment commented out)
   - Each class gets its own logger via `get_logger(__name__)`  

4. **Automated testing**  
   - **Unit tests** for config, loader, preprocessor, trainer  
   - **Integration test** exercises the full pipeline on a toy CSV  

5. **Orchestration**  
   - Apache Airflow DAG splits load→preprocess→train→evaluate  
   - Docker Compose + `airflow standalone` spins up Postgres + scheduler + webserver  

6. **Artifact persistence**  
   - `ensure_dir()` guarantees output directories exist  
   - Host mount of `./models` & `./reports` surfaces trained `.joblib` and `metrics.csv`  

7. **Next step: DVC**  
   - Data Version Control to track raw & processed data alongside code  

---

## 📁 Testing

1. **Activate the virtual env and install dependencies**
    - python -m venv .venv
    - ./venv/Source/activate
    - pip install -r requirements.txt

2. **Run unit tests & integration test**
    - pytest -v tests/test_*.py
    - pytest -v tests/test_integration.py

## 🐳 Docker and Airflow

1. **Build and launch**
    - docker-compose down --volumes --remove-orphans
    - docker-compose build
    - docker-compose up

2. **Access UI**
    - Browse to https://localhost:8080
    - username: admin
    - pass:     admin
    - triger iris_pipeline

3. **Inspect artifacts**
    - models/model.joblib
    - reports/metrics.csv

