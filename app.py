from books_recommender.exception.exception_handler import AppException
import sys
import logging
from books_recommender.logger import log

try:
    a = 3/0
except Exception as e:
    logging.info(e)
    raise AppException(e, sys) from e