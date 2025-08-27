import os, sys
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.components.model_trainer import ModelTrainer

from network_security.entity.config_entity import (
    DataValidationConfig,DataIngestionConfig, DataTransformationConfig, ModelTrainerConfig, TrainingPipelineConfig
)

from network_security.entity.artifact_entity import(
    DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact
)

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()
        