'''entrypoint for the API'''
import os

import uvicorn
from fastapi import FastAPI

from setup import (download_all_files, extract_all_files, insert_data_into_db,
                   read_file_formatted, connect_to_db, create_sensor_info)


def main() -> FastAPI:
    api = FastAPI()

    # config for database connection
    config = {'hostName': 'feinstaub_database',
              'nameDB': 'postgres',
              'userDB': 'admin',
              'passwordDB': 'password'}
    # define sensors
    sensor_types = {'sds011': 3659, 'dht22': 3660}

    @api.post('/setup')
    def start_setup():
        # define a base path where all files should be
        base_path = os.path.join(os.getcwd(), 'downloaded_files')
        # create the base directory for downloaded files
        os.makedirs(base_path, exist_ok=True)
        # downloads all files
        downloaded_file_paths = download_all_files(sensor_types, base_path)
        # determine which files need to be extracted by filtering with .gz
        paths_to_extract = []
        paths_to_not_extract = []
        for file_path in downloaded_file_paths:
            if '.gz' in file_path:
                paths_to_extract.append(file_path)
            else:
                paths_to_not_extract.append(file_path)
        # put files from that list back into old list after extraction
        all_files = paths_to_not_extract + extract_all_files(paths_to_extract)
        # create a session in the database
        connection = connect_to_db(config)
        try:
            # create sensor info in sensor table
            for sensor_type, sensor_id in sensor_types.items():
                for path in all_files:
                    # find any file that correlates to the sensor
                    if sensor_type in path and sensor_id in path:
                        # sensor info is needed for location/lat/lon
                        sensor_info = read_file_formatted(path)
                        break
                # create an entry in sensor table
                create_sensor_info(connection, sensor_type,
                                   sensor_id, sensor_info)
            for path in all_files:
                # read content from the file at path
                lines = read_file_formatted(path)
                # insert read data into the database
                insert_data_into_db(connection, lines)
        finally:
            connection.close()

    @api.post('/test_connection')
    def testing_database():
        connection = connect_to_db(config)
        connection.close()

    return api


if __name__ == '__main__':
    uvicorn.run('main:main', factory=True,
                host='0.0.0.0',
                port=9090,
                reload=True)
