from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

from network_security.entity.config_entity import DataIngestionConfig
import os,sys, pymongo,numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv 
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URI")
class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_collection_as_dataframe(self):
        try:
            database_name=self.data_ingestion_config.database_name
            colleciton_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            colleciton=self.mongo_client[database_name][colleciton_name]
            df=pd.DataFrame(list(colleciton.find()))
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException()
    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe()

        except Exception as e:
            raise NetworkSecurityException