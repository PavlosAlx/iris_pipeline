# from sklearn.datasets import load_iris
import pandas as pd
import os
import boto3
from utils import get_logger

class DataLoader():

    def __init__(self, data_cfg):
        self.cfg = data_cfg
        self.logger = get_logger(self.__class__.__name__)

    def load(self):
        t = self.cfg["type"]
        if t=="local":
            return self.load_local(self.cfg["path"])
        elif t=="s3":
            return self.load_s3(
                bucket=self.cfg["bucket"],
                key=self.cfg["key"],
                profile=self.cfg.get("profile")
            )
        else:
            self.logger.error(f"Couldn't load the data from {t}")
            raise ValueError(f"Couldn't load the data from {t}")

    def load_local(self, path):
        self.logger.info(f"Loading the data from {path}")
        df = pd.read_csv(path)
        self.logger.info(f"Loaded {len(df)} rows")
        return df
    
    def load_s3(self, bucket, key, profile):
        self.logger.info(f"Downloading s3://{bucket}/{key}")
        session = boto3.Session(profile_name=profile) if profile else boto3.Session()
        body = session.client("s3").get_object(Bucket=bucket, Key=key)["Body"]
        df = pd.read_csv(body)
        self.logger.info(f"Loaded {len(df)} rows from S3")
        return df
