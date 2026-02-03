import os
import sys
import pickle
import numpy as np
import pandas as pd
import logging
from books_recommender.logger import log
from books_recommender.config.configuration import AppConfiguration
from books_recommender.exception.exception_handler import AppException

class ModelEvaluator:
    def __init__(self, app_config = AppConfiguration()):
        try:
            self.evaluation_config = app_config.get_output_config()
        except Exception as e:
            raise AppException (e, sys) from e
    

    def evaluate(self):
        try:
            model = pickle.load(open(self.evaluation_config.trained_model_path, 'rb'))
            logging.info(f"Loaded trained model from {self.evaluation_config.trained_model_path}")
            book_pivot = pickle.load(open(self.evaluation_config.book_pivot_serialized_objects, 'rb'))
            final_rating = pickle.load(open(self.evaluation_config.final_rating_serialized_objects, 'rb'))
            logging.info(f"Columns in final_rating: {final_rating.columns.tolist()}")
            logging.info(f"Loaded book pivot and final rating data")

            grouped = final_rating.groupby('user_id')
            train_data = []
            test_data = []

            for user_id, user_ratings in grouped:
                ratings_list = user_ratings.values.tolist()


                split_point = len(ratings_list) // 2
                train = ratings_list[:split_point]
                test = ratings_list[split_point:]

                train_data.extend(train)
                test_data.extend(test)

            columns = ['user_id', 'ISBN', 'rating', 'title', 'author', 'year', 'publisher', 'image_url', 'num_of_rating']
            train_df = pd.DataFrame(train_data, columns = columns)
            test_df = pd.DataFrame(test_data, columns = columns)
            logging.info("Converted train and test data to DataFrames")


            logging.info("Calculating Recall @10...")

            recall_scores = []

            for user_id in test_df['user_id'].unique():
                user_test = test_df[(test_df['user_id'] == user_id) & (test_df['rating'] >= 8)]
                user_train = train_df[train_df['user_id'] == user_id]
                
                if len(user_train) == 0 or len(user_test) == 0:
                    continue
                
                # Get highly-rated books (8+)
                highly_rated_train = user_train[user_train['rating'] >= 8]
                
                if len(highly_rated_train) == 0:
                    continue
                

                all_recommended = []
                
                for _, row in highly_rated_train.iterrows():
                    sample_book = row['title']
                    
                    if sample_book not in book_pivot.index:
                        continue
                    
                    book_id = np.where(book_pivot.index == sample_book)[0][0]
                    
                    distance, suggestions = model.kneighbors(
                        book_pivot.iloc[book_id, :].values.reshape(1, -1), 
                        n_neighbors=11
                    )
                    
                    for i in range(1, len(suggestions[0])):
                        book_title = book_pivot.index[suggestions[0][i]]
                        all_recommended.append(book_title)
                
                # Get top 10 most frequently recommended books
                from collections import Counter
                book_counts = Counter(all_recommended)
                top_10_books = [book for book, count in book_counts.most_common(10)]
                
                # Calculate recall
                actual_books = set(user_test['title'].tolist())
                recommended_books_set = set(top_10_books)
                matches = actual_books.intersection(recommended_books_set)
                
                if len(actual_books) > 0:
                    recall = len(matches) / min(10, len(actual_books))
                    recall_scores.append(recall)
            average_recall = sum(recall_scores) / len(recall_scores)
            logging.info(f"Recall @10: {average_recall}")

        except Exception as e:
            raise AppException(e, sys) from e 


    
    def initiate_model_evaluation(self):
        try:
            logging.info(f"{'='*20}Model evaluator log started.{'='*20} ")
            self.evaluate()
            logging.info(f"{'='*20}Model evaluator log completed.{'='*20} \n\n")
        except Exception as e:
            raise AppException(e, sys) from e    