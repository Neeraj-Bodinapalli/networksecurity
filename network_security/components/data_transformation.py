import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from network_security.constant.training_pipeline import TARGET_COLUMN
from network_security.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from network_security.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)

from network_security.entity.config_entity import DataTransformationConfig
from network_security.exception.exception import NetworkSecurityException 
from network_security.logging.logger import logging
from network_security.utils.main_utils.utils import save_numpy_array_data,save_object

class DataTransformation:
    def __init__(self,datavalidationartifact:DataValidationArtifact,datatransformationconfig:DataTransformationConfig):
        try:
            self.datavalidationartifact=datavalidationartifact
            self.datatransformationconfig=datatransformationconfig
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def get_data_transformer_object(cls)->Pipeline:
        """
        It initialises a KNNImputer object with the parameters specified in the training_pipeline.py file
        and returns a Pipeline object with the KNNImputer object as the first step.

        Args:
          cls: DataTransformation

        Returns:
          A Pipeline object
        """
        logging.info(
            "Entered get_data_transformer_object method of Trnasformation class"
        )
        try:
           imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
           logging.info(
                f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}" 
            )
           processor:Pipeline=Pipeline([("imputer",imputer)])
           return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    
    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("entered initiate data transformation fucntion")
        try:
            logging.info("starting data transformation")
            train_df=DataTransformation.read_data(self.datavalidationartifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.datavalidationartifact.valid_test_file_path)

            # training data frame removing target
            input_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_train_df=train_df[TARGET_COLUMN]
            target_train_df=target_train_df.replace(-1,0)  # replacing -1 with 0 as it is classification problem 
            
            # training data frame removing target
            input_test_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_test_df=train_df[TARGET_COLUMN]
            target_test_df=target_test_df.replace(-1,0)

            preprocessor=self.get_data_transformer_object()

            preprocessor_object=preprocessor.fit(input_train_df)
            transformed_input_train_feature=preprocessor_object.transform(input_train_df)
            transformed_input_test_feature =preprocessor_object.transform(input_test_df)

            train_arr = np.c_[transformed_input_train_feature, np.array(target_train_df) ]
            test_arr = np.c_[ transformed_input_test_feature, np.array(target_test_df) ]

            #save numpy array data
            save_numpy_array_data( self.datatransformationconfig.transformed_train_file_path, array=train_arr, )
            save_numpy_array_data( self.datatransformationconfig.transformed_test_file_path,array=test_arr,)
            save_object( self.datatransformationconfig.transformed_object_file_path, preprocessor_object,)

            save_object( "final_model/preprocessor.pkl", preprocessor_object,)


            #preparing artifacts

            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.datatransformationconfig.transformed_object_file_path,
                transformed_train_file_path=self.datatransformationconfig.transformed_train_file_path,
                transformed_test_file_path=self.datatransformationconfig.transformed_test_file_path
            )
            return data_transformation_artifact

           

        except Exception as e:
            raise NetworkSecurityException(e,sys)

