'''setup module that provides functionality to prepare the database content'''
from .downloader import download_all_files
from .file_handler import extract_all_files, read_file_formatted
from .database_handler import insert_data_into_db, connect_to_db, create_sensor_info
