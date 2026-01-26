from dataclasses import dataclass
from typing import Dict

@dataclass
class DataIngestionConfig:
    """Configuration for data ingestion stage"""
    source_urls: Dict[str, str]  # URLs for books, ratings, users
    root_dir: str
    local_data_dir: str
    raw_data_dir: str
    ingested_dir: str


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