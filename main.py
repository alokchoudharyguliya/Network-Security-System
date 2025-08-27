from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.entity.config_entity import DataIngestionConfig, DataValidationConfig
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
        logging.info("Data Ingestion Done")
        print(datavalidationartifact)
        # a=1/0
        # print("This will not be printed")
    except Exception as e:
        raise NetworkSecurityException(e,sys)