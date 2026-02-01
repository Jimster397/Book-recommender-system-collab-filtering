import os
import sys
import pickle
import streamlit as st
import numpy as np
from books_recommender.logger import log
import logging
from books_recommender.pipeline.training_pipeline import TrainingPipeline
from books_recommender.config.configuration import AppConfiguration
from books_recommender.exception.exception_handler import AppException


class Recommendation:
    def __init__(self, app_config = AppConfiguration()):
        try:
            self.recommendation_config = app_config.get_recommendation_config()
        except Exception as e:
            raise AppException(e, sys) from e
        


    def fetch_poster(self, suggestion):
        try:
            book_name = []
            ids_index = []
            poster_url = []
            book_pivot = pickle.load(open(self.recommendation_config.book_pivot_serialized_objects,'rb'))
            final_rating = pickle.load(open(self.recommendation_config.final_rating_serialized_objects,'rb'))

            for book_id in suggestion:
                book_name.append(book_pivot.index[book_id])

            for name in book_name[0]:
                ids = np.where(final_rating['title'] == name)[0][0]
                ids_index.append(ids)

            for idx in ids_index:
                url = final_rating.iloc[idx]['image_url']
                poster_url.append(url)

            return poster_url
        
        except Exception as e:
            raise AppException(e, sys) from e
        
    def recommend_book(self, book_name):
        try: 
            books_list = []
            model = pickle.load(open(self.recommendation_config.trained_model_path,'rb'))
            book_pivot = pickle.load(open(self.recommendation_config.book_pivot_serialized_objects,'rb'))
            book_id = np.where(book_pivot.index == book_name)[0][0]
            distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6)

            poster_url = self.fetch_poster(suggestion)
            
            for i in range(1, len(suggestion[0])):  
                book = book_pivot.index[suggestion[0][i]]
                books_list.append(book)
            
            return books_list, poster_url[1:]
        except Exception as e:
            raise AppException(e, sys) from e
        
    
    def train_engine(self):
        try:
            obj = TrainingPipeline()
            obj.start_training_pipeline()
            st.text("Training Completed!")
            logging.info(f"Recommended successfully!")
        except Exception as e:
            raise AppException(e, sys) from e
        

    def recommendation_engine(self, selected_books):
        try:
            recommended_books,poster_url = self.recommend_book(selected_books)
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.text(recommended_books[0])
                st.image(poster_url[0])
            with col2:
                st.text(recommended_books[1])
                st.image(poster_url[1])
            with col3:
                st.text(recommended_books[2])
                st.image(poster_url[2])
            with col4:
                st.text(recommended_books[3])
                st.image(poster_url[3])
            with col5:
                st.text(recommended_books[4])
                st.image(poster_url[4])                
        except Exception as e:
            raise AppException(e, sys) from e
        


if __name__ == "__main__":
    st.set_page_config(
        page_title="Book Recommender System",
        page_icon="📚",
        layout="wide"
    )
    
    st.markdown("""
        <style>
        /* Import fonts */
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Roboto:wght@400;600&display=swap');
        
        /* Main app background */
        .stApp {
            background-color: #1a1a2e;  /* Dark navy */
        }

        [data-testid="stAppViewContainer"] {
            background-color: #1a1a2e;  /* Dark navy */
        }

        /* Make all text white for dark background */
        p, div, span, label {
            color: #ffffff !important;
        }

        h1, h2, h3 {
            color: #ffffff !important;
        }
                
        
        /* Title styling */
        h1 {
            color: #1a1a2e;
            font-family: 'Playfair Display', serif;
            text-align: center;
            padding: 20px 0;
            font-size: 3rem;
        }
        
        /* Subtitle styling */
        h3 {
            color: #16213e;
            font-family: 'Roboto', sans-serif;
            text-align: center;
            font-style: italic;
            font-weight: 400;
        }
        
        /* Subheader styling */
        h2 {
            color: #0f4c75;
            font-family: 'Roboto', sans-serif;
            border-bottom: 3px solid #3282b8;
            padding-bottom: 10px;
            margin-top: 30px;
        }
        
        /* Caption text */
        .stCaption {
            color: #546e7a;
            font-size: 14px;
        }
        
        /* Button styling */
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 25px;
            padding: 12px 30px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        /* Selectbox styling */
        .stSelectbox label {
            color: #1a1a2e;
            font-size: 18px;
            font-weight: 600;
            font-family: 'Roboto', sans-serif;
        }
        
        .stSelectbox > div > div {
            border-radius: 10px;
            border: 2px solid #3282b8;
        }
        
        /* Horizontal line */
        hr {
            border: 0;
            height: 2px;
            background: linear-gradient(to right, transparent, #3282b8, transparent);
            margin: 30px 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("Book Recommender System")
    st.markdown("---")
    
    obj = Recommendation()

    st.subheader("Model Training")
    st.caption("Click below to train or retrain the recommendation model")
    if st.button('Train Recommender System'):
        obj.train_engine()
    
    st.markdown("---")
    

    st.subheader("Get Book Recommendations")
    st.caption("Select a book you enjoyed, and we'll suggest similar titles")
    
    book_names = pickle.load(open('artifacts/data_ingestion/serialized_objects/book_names.pkl', 'rb'))
    
    selected_books = st.selectbox(
        "Choose a book from the dropdown",
        book_names
    )

    if st.button('Show Recommendations'):
        obj.recommendation_engine(selected_books)