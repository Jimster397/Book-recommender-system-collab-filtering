import os
import sys
import pickle
import pandas as pd
import logging
from books_recommender.logger import log
from books_recommender.config.configuration import AppConfiguration
from books_recommender.exception.exception_handler import AppException


class DataTransformation:
    def __init__(self, app_config=AppConfiguration()):
        try:
            self.data_transformation_config = app_config.get_data_transformation_config()  # ← Fixed typo
            self.data_validation_config = app_config.get_data_validation_config()  # ← Different variable
        except Exception as e:
            raise AppException(e, sys) from e
    
    def get_data_transformer(self):
        try:
            # Load cleaned data
            df = pd.read_csv(self.data_transformation_config.clean_data_file_path)
            
            # Create pivot table
            book_pivot = df.pivot_table(columns='user_id', index='title', values='rating')
            logging.info(f"Shape of book pivot table: {book_pivot.shape}")
            book_pivot.fillna(0, inplace=True)

            # Get book names
            book_names = book_pivot.index

            # Save all serialized objects to one location
            os.makedirs(self.data_validation_config.serialized_objects_dir, exist_ok=True)
            
            # Save book_pivot
            pickle.dump(book_pivot, open(os.path.join(self.data_validation_config.serialized_objects_dir, "book_pivot.pkl"), 'wb'))
            logging.info(f"Saved book_pivot serialization object to {self.data_validation_config.serialized_objects_dir}")
            
            # Save book_names
            pickle.dump(book_names, open(os.path.join(self.data_validation_config.serialized_objects_dir, "book_names.pkl"), 'wb'))
            logging.info(f"Saved book_names serialization object to {self.data_validation_config.serialized_objects_dir}")

        except Exception as e:
            raise AppException(e, sys) from e
    
    def initiate_data_transformation(self):
        try:
            logging.info(f"{'='*20}Data Transformation log started.{'='*20}")
            self.get_data_transformer()
            logging.info(f"{'='*20}Data Transformation log completed.{'='*20} \n\n")
        
        except Exception as e:
            raise AppException(e, sys) from e
                        

