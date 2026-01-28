from dataclasses import dataclass
from typing import Dict

@dataclass
class DataIngestionConfig:
    """Configuration for data ingestion stage"""
    source_urls: Dict[str, str]
    raw_data_dir: str


@dataclass
class DataValidationConfig:
    """Configuration for data validation stage"""
    clean_data_dir: str
    serialized_objects_dir: str
    books_csv_file: str
    ratings_csv_file: str
    users_csv_file: str


@dataclass
class DataTransformationConfig:
    """Configuration for data transformation stage"""
    clean_data_file_path: str
    transformed_data_dir: str



@dataclass
class ModelTrainerConfig:
    """Configuration for model training stage"""
    transformed_data_file_dir: str
    trained_model_dir: str
    trained_model_name: str


@dataclass
class ModelRecommendationConfig:
    """Configuration for model recommendation stage"""
    book_pivot_serialized_objects: str
    final_rating_serialized_objects: str
    trained_model_path: str