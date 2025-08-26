# Data Drifting should not be there so we need to ensure data validation
from network_security.entity.config_entity import DataValidationConfig
from network_security.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.constants.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import yaml
from network_security.utils.main_utils.utils  import  read_yaml_file
import pandas as pd, os, sys
class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path
            ## read the dat from train and test
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)