from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

from network_security.entity.config_entity import DataIngestionConfig
import os,sys, pymongo,numpy as np
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv 
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URI")
class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            pass
        except Exception as e:
            raise e