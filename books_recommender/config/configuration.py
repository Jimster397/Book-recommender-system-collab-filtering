import os 
import sys
import logging

from numpy import e
from books_recommender.logger import log
from books_recommender.utils.util import read_yaml_file
from books_recommender.exception.exception_handler import AppException
from books_recommender.constant import *



class AppConfiguration:
    def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
        try:
            self.configs_info = read_yaml_file(file_path = config_file_path)
        except Exception as e:
            raise AppException(e, sys) from e
        

    
def get_data_ingestion_config(self) -> DataIngestionConfig:
    try:
        # Get the data ingestion section from config
        config = self.configs_info['data_ingestion_config']
    
        # Create the config object directly from the YAML values
        response = DataIngestionConfig(
            source_urls=config['source_urls'],
            root_dir=config['root_dir'],
            local_data_dir=config['local_data_dir'],
            raw_data_dir=config['raw_data_dir'],
            ingested_dir=config['ingested_dir']
        )

        logging.info(f"Data Ingestion Config: {response}")
        return response
        
    except Exception as e:
        raise AppException(e, sys) from e