from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from utils import get_logger, ensure_dir
import joblib
import json

class ModelTrain():
    def __init__(self, train_cfg, eval_cfg):
        self.train_cfg = train_cfg
        self.eval_cfg  = eval_cfg
        self.logger    = get_logger(self.__class__.__name__)

    def train(self, X_train, y_train):
        hp = self.train_cfg["hyperparameters"]
        self.model = LogisticRegression(
            random_state=self.train_cfg["random_state"],
            solver=hp["solver"],
            max_iter=hp.get("max_iter", 100)
        )
        self.model.fit(X_train, y_train)
        self.logger.info("Model training complete")

        return self.model
    
    def evaluate(self, X_test, y_test):
        y_pred = self.model.predict(X_test)
        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "report": classification_report(y_test, y_pred, target_names=self.eval_cfg["labels"])
        }
        self.logger.info(f"\nModel Accuracy: {metrics['accuracy']:.4f}")
        self.logger.info(f"\nClassification Report:\n{metrics['report']}")

        
        return metrics
    
    def save_model(self):
        path = self.train_cfg["model_output_path"]
        path = "/opt/airflow/models/model.pkl"
        ensure_dir(path)
        joblib.dump(self.model, path)
        self.logger.info(f"Saved model to {path}")

        return 
    
    def save_metrics(self, metrics):
        path = self.train_cfg["metrics_output_path"]
        path = "/opt/airflow/report/metrics.csv"
        ensure_dir(path)
        with open(path, "w") as f:
            json.dump(metrics, f, indent=2)
        self.logger.info(f"Saved metrics to {path}")

        return
# def model_save(model, cfg):

#     logger = get_logger(__name__)
#     model_output_path = cfg['training']['metrics_output_path']
#     joblib.dump(model, model_output_path)
#     logger.info(f"Model saved to: {model_output_path}")
#     return


# def model_evaluation(model, X_test, y_test, target_names):

#     logger = get_logger(__name__)
#     y_pred = model.predict(X_test)
#     accuracy = accuracy_score(y_test, y_pred)
#     report = classification_report(y_test, y_pred, target_names = target_names)

#     logger.info(f"\nModel Accuracy: {accuracy:.4f}")
#     logger.info(f"\nClassification Report:{report}")

#     return 

# def train_model(cfg, X_train, y_train, X_test, y_test, target_names):

#     logger = get_logger(__name__)

#     model = LogisticRegression(
#         random_state=cfg['training']['random_state'],
#         solver=cfg['training']['hyperparameters']['solver'],
#         multi_class='auto',
#         max_iter=cfg['training']['hyperparameters']['max_iter']
#     )

#     model.fit(X_train, y_train)
#     logger.info("Model trained.")

#     model_evaluation(model, X_test, y_test, target_names)
#     model_save(model, cfg)

#     return model


