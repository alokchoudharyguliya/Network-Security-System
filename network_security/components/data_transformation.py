import os, sys, pandas as pd, numpy as np
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
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS) # ** stands for whatever parameters we are giving here will be considered as key value pairs
            processor:Pipeline=Pipeline([("imputer",imputer)])
            return processor
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
            
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df=target_feature_test_df.replace(-1,0)
            preprocessor=self.get_data_transformer_object()
            preprocessor_object=preprocessor.fit(input_feature_train_df)
            transformed_input_train_features=preprocessor_object.transform(input_feature_train_df)
            transfoemed_input_test_features=preprocessor_object.transform(input_feature_test_df)
            train_arr=np.c_[transformed_input_train_features,np.array(target_feature_train_df)]
            test_arr=np.c_[transfoemed_input_test_features,np.array(target_feature_test_df)]
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr,)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr,)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object,)
            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path

            )
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)