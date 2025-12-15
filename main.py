from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.entity.config_entity import DataIngestionConfig,DataValidationConfig
from network_security.entity.config_entity import TrainingPipelineConfig
import sys

if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        dataingestion=DataIngestion(dataingestionconfig)
        dataingestionartifact=dataingestion.initiate_data_ingestion()
        logging.info("Initiate data ingestion")
        print(dataingestionartifact)
        datavalidationconfig=DataValidationConfig(trainingpipelineconfig)
        datavalidation=DataValidation(dataingestionartifact,datavalidationconfig)
        logging.info("Initiate data validation")
        datavalidationartifact=datavalidation.initiate_data_validation()
        logging.info(" data validation done")
        print(datavalidationartifact)


    except Exception as e:
        raise NetworkSecurityException(e,sys)