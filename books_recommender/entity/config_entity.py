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


