import os, sys, numpy, pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from network_security.constants.training_pipeline import TARGET_COLUMN
from network_security.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from network_security.entity.artifact_entity import (DataTransformationArtifact,DataValidationArtifact)
from network_security.entity.config_entity import DataTransformationConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

from network_security.utils.main_utils.utils import save_numpy_array_data,save_object
class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
            
    def get_data_transformer_object(cls)->Pipeline:
        """
        It initializes a KNNImputer object with the parameters specified in the training_pipeline.py file and reutrns a Pipeline object with the KNNImputer object as the first step.
        Args:
            cls: DataTransformation
        Returns:
            A Pipeline object
        """
        logging.info("Entered get_data_transformer_object method of Transformation class")
        try:
            KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS) # ** stands for whatever parameters we are giving here will be considered as key value pairs
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("Entered initiate_data_transformation method of DataTransformation class")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN])
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_train_df=target_feature_train_df.replace(-1,0)
        except Exception as e:
            raise NetworkSecurityException(e,sys)