from src.utils import setup_logging, get_logger
from src.data_loader import DataLoader
from src.data_preprocess import DataPreprocessor
from src.train import ModelTrain
from src.config import Config

def main(config_path):
    # logger & config
    setup_logging(
        log_file="logs/app.log",
        max_bytes=5_000_000,
        backup_count=3,
        level="DEBUG" 
    )

    logger = get_logger(__name__)
    logger.info("Pipeline starting...")
    cfg    = Config(config_path)

    # load data
    loader = DataLoader(cfg["data_source"])
    df     = loader.load()

    # preprocess & split
    preprocess    = DataPreprocessor(cfg["training"])
    X_train, X_test, y_train, y_test = preprocess.process(df, label_col="label")

    # train & eval
    trainer = ModelTrain(cfg["training"], cfg["evaluation"])
    model    = trainer.train(X_train, y_train)
    metrics  = trainer.evaluate(X_test, y_test)
    trainer.save_model()
    trainer.save_metrics(metrics)

    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    main()








# def load_config(config_path):

#     with open(config_path) as f:
#         cfg = yaml.safe_load(f)
    
#     return cfg

# def run(config_path):
    
#     #load config
#     cfg = load_config(config_path)
#     raw, X, y = data_load_sklearn()
#     X_train, X_test, y_train, y_test, target_names, scaler = data_preprocess(raw, X, y, cfg)
#     model = train_model(cfg, X_train, y_train, X_test, y_test, target_names)

#     return 

# if __name__=="__main__":

#     setup_logging(
#         log_file="logs/app.log",
#         max_bytes=5_000_000,
#         backup_count=3,
#         level="DEBUG" 
#     )

#     logger = get_logger(__name__)
#     logger.info("Pipeline starting...")

#     this_dir = os.path.dirname(__file__)
#     project_root = os.path.dirname(this_dir)
#     config_path = os.path.join(project_root, "config.yml")

#     try:
#         run(config_path)
#         logger.info("Pipeline finished successfully")
#     except Exception:
#         logger.exception("Pipeline failed with exception")
