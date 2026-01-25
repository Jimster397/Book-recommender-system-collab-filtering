import os
import sys
import ast 
import pandas as pd
import pickle
from books_recommender.logger import log
import logging
from books_recommender.config.configuration import AppConfiguration
from books_recommender.exception.exception_handler import AppException

class DataValidation:
    def __init__(self, app_config = AppConfiguration()):
        try:
            self.data_validation_config = app_config.get_data_validation_config()
        except Exception as e:
            raise AppException(e, sys) from e
        
    
    def preprocess_data(self):
        try:
            ratings = pd.read_csv(self.data_validation_config.ratings_csv_file, sep=";", on_bad_lines='skip', encoding='latin-1', low_memory=False)
            books = pd.read_csv(self.data_validation_config.books_csv_file, sep=";", on_bad_lines='skip', encoding='latin-1', low_memory=False)
            users = pd.read_csv(self.data_validation_config.users_csv_file, sep=";", on_bad_lines='skip', encoding='latin-1', low_memory=False)

            logging.info(f" Shape of ratings data file: {ratings.shape}")
            logging.info(f" Shape of books data file: {books.shape}")
            logging.info(f" Shape of users data file: {users.shape}")
            # Note: users data loaded for validation but not used in processing


            #Here Image URL columns is important for the poster. So, we will keep it
            books = books[['ISBN','Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher','Image-URL-L']]
            #Renaming the columns name in books
            books.rename(columns={"Book-Title":'title',
                                'Book-Author':'author',
                                "Year-Of-Publication":'year',
                                "Publisher":"publisher",
                                "Image-URL-L":"image_url"},inplace=True)
            

            # Remaning the columns name in ratings
            ratings.rename(columns={"User-ID":'user_id',
                                'Book-Rating':'rating'},inplace=True)
            
            # Filter users who rated more than 200 books
            x = ratings['user_id'].value_counts() > 200
            y = x[x].index
            ratings = ratings[ratings['user_id'].isin(y)]

            # Join ratings with books
            ratings_with_books = ratings.merge(books, on='ISBN')
            number_rating = ratings_with_books.groupby('title')['rating'].count().reset_index()
            number_rating.rename(columns={'rating':'num_of_rating'},inplace=True)
            final_rating = ratings_with_books.merge(number_rating, on='title')

            # Each book that has at least 50 user ratings
            final_rating = final_rating[final_rating['num_of_rating'] >= 50]

            # Dropping duplicates
            final_rating.drop_duplicates(['user_id','title'],inplace=True)
            logging.info(f" Shape of the final clean dataset: {final_rating.shape}")

            # Saving the cleaned data for transformation
            os.makedirs(self.data_validation_config.clean_data_dir, exist_ok=True)
            final_rating.to_csv(os.path.join(self.data_validation_config.clean_data_dir,'clean_data.csv'), index = False)
            logging.info(f"Saved cleaned data to {self.data_validation_config.clean_data_dir}")

            #Saving final_rating objects for Web app
            os.makedirs(self.data_validation_config.serialized_objects_dir, exist_ok=True)
            pickle.dump(final_rating,open(os.path.join(self.data_validation_config.serialized_objects_dir, "final_rating.pkl"),'wb'))
            logging.info(f"Saved final_rating serialization object to {self.data_validation_config.serialized_objects_dir}")

        except Exception as e:
            raise AppException(e, sys) from e
        
    def initiate_data_validation(self):
            try:
                logging.info(f"{'='*20}Data Validation log started.{'='*20} ")
                self.preprocess_data()
                logging.info(f"{'='*20}Data Validation log completed.{'='*20} \n\n")
        
            except Exception as e:
                raise AppException(e, sys) from e

