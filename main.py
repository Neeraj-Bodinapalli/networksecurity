from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig 
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

        logging.info("Initiate data transformation")
        datatransformationconfig=DataTransformationConfig(trainingpipelineconfig)
        datatransformation=DataTransformation(datavalidationartifact,datatransformationconfig)
        datatransformationartifact=datatransformation.initiate_data_transformation()
        logging.info(" data transformation done")
        print(datatransformationartifact)


    except Exception as e:
        raise NetworkSecurityException(e,sys)