import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    if not os.path.exists('logs'):   #creating the logs folder for the app.log file.
        os.makedirs('logs')

    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10 * 1024 * 1024, backupCount=10)  #NOW its 10MB
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    file_handler.setLevel(logging.INFO)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
