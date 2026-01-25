import os
import sys
import urllib.request
from books_recommender.logger import log
import logging
from books_recommender.exception.exception_handler import AppException
from books_recommender.config.configuration import AppConfiguration


class DataIngestion:
    def __init__(self, app_config = AppConfiguration()):
        """
        Data Ingestion Initialization
        data_ingestion_config: DataIngestionConfig
        """
        try:
            logging.info(f"{'='*20}Data ingestion log started.{'='*20}")
            self.data_ingestion_config = app_config.get_data_ingestion_config()
        except Exception as e:
            raise AppException(e, sys) from e
    


    def download_data(self):
        """
        Download all data files (books, ratings, users) from GitHub
        """
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            os.makedirs(raw_data_dir, exist_ok=True)
            
            downloaded_files = {}
            
            # Download each CSV file
            for file_type, url in self.data_ingestion_config.source_urls.items():
                file_name = url.split('/')[-1]
                file_path = os.path.join(raw_data_dir, file_name)
                
                logging.info(f"Downloading {file_type} data from {url}")
                urllib.request.urlretrieve(url, file_path)
                logging.info(f"Downloaded {file_type} data to {file_path}")
                
                downloaded_files[file_type] = file_path
            
            logging.info(f"All data files downloaded successfully")
            return downloaded_files
            
        except Exception as e:
            raise AppException(e, sys) from e
        

    def initiate_data_ingestion(self):
        try:
            downloaded_files = self.download_data()
            logging.info(f"{'='*20}Data Ingestion log completed.{'='*20} \n\n")
            return downloaded_files
        except Exception as e:
            raise AppException(e, sys) from e