# import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from src.utils import get_logger
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
    










# def missing_values(df):
#     # Chose mean value - can either drop / median(better with outliers) /  dedicated regression 
#     means = df.mean(numeric_only=True)
#     df = df.fillna(means)
#     return df

# def scale_numerical(df, features):
#     # Chose standard scaler - can either MinMaxScaler / RobustScaler(better with outliers)
#     scaler = StandardScaler()
#     df[features] = scaler.fit_transform(df[features])
#     return df, scaler

# def split_dataset(X, y, test_size, random_state):

#     logger = get_logger(__name__)
#     # We use numerical targets for training, but labels for visualization/reporting
#     X_train, X_test, y_train, y_test = train_test_split(
#         X, y, test_size=test_size,
#         random_state=random_state,
#         stratify=y) # Stratify to ensure class proportions

#     logger.info(f"Training set size: {X_train.shape[0]} samples")
#     logger.info(f"Test set size: {X_test.shape[0]} samples")
#     return X_train, X_test, y_train, y_test

# def data_preprocess(iris, X, y, cfg):

#     logger = get_logger(__name__)
#     # map numerical targets to species names for clarity
#     target_names = iris.target_names
#     y_labels = y.map(lambda x: target_names[x])
#     # keep the numerical features of the set
#     features = iris.feature_names

#     df = X.copy()
#     df['species'] = y_labels # Add species labels to the DataFrame
#     logger.info(f"Iris dataset loaded with {df.shape[0]} samples and {df.shape[1]-1} features.")  

#     df = missing_values(df)
#     df, scaler = scale_numerical(df, features)

#     #Break to training / testing
#     test_size = cfg['training']['test_size']
#     random_state = cfg['training']['random_state']
#     X_train, X_test, y_train, y_test = split_dataset(X, y, test_size, random_state)


#     return X_train, X_test, y_train, y_test, target_names,scaler









    
