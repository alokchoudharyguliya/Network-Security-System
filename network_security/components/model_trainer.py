import os, sys

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

from network_security.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from network_security.entity.config_entity import ModelTrainerConfig

from network_security.utils.main_utils.utils import NetworkModel
from network_security.utils.main_utils.utils import save_object,load_object
from network_security.utils.main_utils.utils import load_numpy_array_data,evaluate_models
from network_security.utils.ml_utils.metric.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (AdaBoostClassifier,GradientBoostingClassifier,RandomForestClassifier)
import mlflow
from urllib.parse import urlparse
import dagshub

os.environ["MLFLOW_TRACKING_URI"]=""
os.environ["MLFLOW_TRACKING_USERNAME"]=""
os.environ["MLFLOW_TRACKING_PASSWORD"]=""


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,
                 data_transformer_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def track_mlflow(self):
        pass