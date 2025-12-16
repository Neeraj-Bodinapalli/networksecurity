from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.components.model_trainer import ModelTrainer
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
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

        logging.info("model trainer started")
        model_trainer_config=ModelTrainerConfig(trainingpipelineconfig)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_trans_artifact=datatransformationartifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()
        logging.info("model trainer done")
        print(model_trainer_artifact)


    except Exception as e:
        raise NetworkSecurityException(e,sys)