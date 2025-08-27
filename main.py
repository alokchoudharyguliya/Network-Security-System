from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.components.model_trainer import ModelTrainer
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.entity.config_entity import DataIngestionConfig, DataValidationConfig,DataTransformationConfig, ModelTrainerConfig
from network_security.entity.config_entity import TrainingPipelineConfig

import sys
# def main():
#     print("Hello from network-security-system!")


# if __name__ == "__main__":
#     main()

if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(training_pipeline_config=trainingpipelineconfig)
        datavalidationconfig=DataValidationConfig(training_pipeline_config=trainingpipelineconfig)
        
        dataingestion=DataIngestion(dataingestionconfig)
        logging.info("Initiate the Data Ingestion")
        dataingestionartifact=dataingestion.initiate_data_ingestion()
        logging.info("Data Ingestion Done")
        data_validation=DataValidation(dataingestionartifact,datavalidationconfig)
        logging.info("Initiate the Data Validation")
        datavalidationartifact=data_validation.initiate_data_validation()
        logging.info("Data Validation Done")
        print(datavalidationartifact)
        datatransformationconfig=DataTransformationConfig(training_pipeline_config=trainingpipelineconfig)
        logging.info("Initiate the Data Transformation")
        data_transformation=DataTransformation(datavalidationartifact,datatransformationconfig)
        datatransformationartifact=data_transformation.initiate_data_transformation()
        logging.info("Data Transformation Done")
        print(datatransformationartifact)
        logging.info("Model Training started")
        modeltrainerconfig=ModelTrainerConfig(training_pipeline_config=trainingpipelineconfig)
        model_trainer=ModelTrainer(model_trainer_config=modeltrainerconfig,data_transformer_artifact=datatransformationartifact)
        modeltrainerartifact=model_trainer.initiate_model_trainer()
        logging.info("Model Training Done")
        print(modeltrainerartifact)

        # a=1/0
        # print("This will not be printed")
    except Exception as e:
        raise NetworkSecurityException(e,sys)