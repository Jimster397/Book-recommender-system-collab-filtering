import os 
import sys
import logging
from books_recommender.logger import log
from books_recommender.constant import *
from books_recommender.utils.util import read_yaml_file
from books_recommender.exception.exception_handler import AppException
from books_recommender.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig



class AppConfiguration:
    def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
        try:
            self.configs_info = read_yaml_file(file_path = config_file_path)
        except Exception as e:
            raise AppException(e, sys) from e
        

    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            config = self.configs_info['data_ingestion_config']
        
            response = DataIngestionConfig(
                source_urls=config['source_urls'],
                raw_data_dir=config['raw_data_dir']
            )

            logging.info(f"Data Ingestion Config: {response}")
            return response
            
        except Exception as e:
            raise AppException(e, sys) from e
        

    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            config = self.configs_info['data_validation_config']
            raw_data_dir = self.configs_info['data_ingestion_config']['raw_data_dir']
            
            books_csv_path = os.path.join(raw_data_dir, config['books_csv_file'])
            ratings_csv_path = os.path.join(raw_data_dir, config['ratings_csv_file'])
            users_csv_path = os.path.join(raw_data_dir, config['users_csv_file'])
            
            clean_data_dir = os.path.join('artifacts/data_ingestion', config['clean_data_dir'])
            serialized_objects_dir = os.path.join('artifacts/data_ingestion', config['serialized_objects_dir'])
            
            response = DataValidationConfig(
                clean_data_dir = clean_data_dir,
                serialized_objects_dir = serialized_objects_dir,
                books_csv_file = books_csv_path,
                ratings_csv_file = ratings_csv_path,
                users_csv_file = users_csv_path
            )

            logging.info(f"Data Validation Config: {response}")
            return response
            
        except Exception as e:
            raise AppException(e, sys) from e
        
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        try:
            config = self.configs_info['data_transformation_config']
            validation_config = self.configs_info['data_validation_config']
            
            clean_data_file_path = os.path.join(
                'artifacts/data_ingestion',
                validation_config['clean_data_dir'],
                'clean_data.csv'
            )
            
            transformed_data_dir = os.path.join(
                'artifacts/data_ingestion',
                config['transformed_data_dir']
            )
            
            response = DataTransformationConfig(
                clean_data_file_path = clean_data_file_path,
                transformed_data_dir = transformed_data_dir
            )

            logging.info(f"Data Transformation Config: {response}")
            return response
            
        except Exception as e:
            raise AppException(e, sys) from e


    def get_model_trainer_config(self) -> ModelTrainerConfig:
        try:
            config = self.configs_info['model_trainer_config']
            validation_config = self.configs_info['data_validation_config']
            
            # Build full path to book_pivot.pkl
            transformed_data_file_dir = os.path.join(
                'artifacts/data_ingestion',
                validation_config['serialized_objects_dir'],
                'book_pivot.pkl'
            )
            
            # Directory to save trained model
            trained_model_dir = os.path.join(
                'artifacts/data_ingestion',
                config['trained_model_dir']
            )
            
            trained_model_name = config['trained_model_name']
            
            response = ModelTrainerConfig(
                transformed_data_file_dir=transformed_data_file_dir,
                trained_model_dir=trained_model_dir,
                trained_model_name=trained_model_name
            )
            
            logging.info(f"Model Trainer Config: {response}")
            return response
            
        except Exception as e:
            raise AppException(e, sys) from e