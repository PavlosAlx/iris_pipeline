# import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from utils import get_logger
import numpy as np
## Assuming future data might have missing values / need scale, added:
## - fix missing values
## - make sure you scale your numerical features

class DataPreprocessor():

    def __init__(self, preprocess_cfg):
        self.test_size = preprocess_cfg["test_size"]
        self.random_state = preprocess_cfg["random_state"]
        self.logger = get_logger(self.__class__.__name__)
        self.scaler = None

    def clean(self, df):
        # Chose mean value - can either drop / median(better with outliers) /  dedicated regression 
        num_cols = df.select_dtypes(include=np.number).columns
        means = df[num_cols].mean()
        df[num_cols] = df[num_cols].fillna(means)
        self.logger.info("Missing values imputed with mean")
        return df
    
    def scale(self, df, feature_cols):
        # Chose standard scaler - can either MinMaxScaler / RobustScaler(better with outliers)
        self.scaler = StandardScaler()
        df[feature_cols] =self.scaler.fit_transform(df[feature_cols])
        self.logger.info("Features scaled with Standard Scaler")
        return df
    
    def split(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=self.test_size,
        random_state=self.random_state,
        stratify=y
        ) # Stratify to ensure class proportions
        self.logger.info(f"Training set size: {X_train.shape[0]} samples")
        self.logger.info(f"Test set size: {X_test.shape[0]} samples")
        return X_train, X_test, y_train, y_test
    
    def process(self, df, label_col):
        df = self.clean(df)
        features = [c for c in df.columns if c!=label_col]
        df = self.scale(df, features)
        X = df[features]
        y = df[label_col]
        return self.split(X,y)
    