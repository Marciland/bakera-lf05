'''entrypoint for the API'''
import os
from argparse import ArgumentParser

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from modules.data_models import Date
from modules.database_handler import connect_to_db, fetch_data
from modules.downloader import download_data
from modules.file_handler import extract_file, read_file_formatted
from modules.sensor_data import (SensorInfo, filter_sensor_data,
                                 get_sensor_function)


def get_arguments():
    '''
    Parses arguments.

        Returns:
            args: given arguments
    '''
    parser = ArgumentParser(description='marciland.net API')
    parser.add_argument('-d', '--develop', action='store_true', default=False,
                        dest='develop', required=False,
                        help='Toggle for localhost database.')
    return parser.parse_args()


def main() -> FastAPI:
    '''
    Main entry point for uvicorn. Yields API with necessary routing.
    '''
    api = FastAPI()

    args = get_arguments()
    develop = args.develop
    host_name = 'localhost' if develop else 'feinstaub_database'

    config = {'hostName': host_name,
              'nameDB': 'postgres',
              'userDB': 'admin',
              'passwordDB': 'password'}

    filter_map = {0: 'min',
                  1: 'avg',
                  2: 'max'}

    download_path = os.path.join(os.getcwd(), 'downloaded_files')
    os.makedirs(download_path, exist_ok=True)

    @api.post('/insert_data', status_code=status.HTTP_201_CREATED)
    def insert_data(date: Date = Date(year=2022, month=1, day=1),
                    sensor_info: SensorInfo = SensorInfo(type='sds011', id=3659)):
        insert_function = get_sensor_function(sensor_info.type)
        file_paths = download_data(download_path, date, sensor_info)
        con = connect_to_db(config, commit=True)
        try:
            for path in file_paths.copy():
                new_path = None
                if '.gz' in path:
                    new_path = extract_file(path)
                    file_paths.remove(path)
                    file_paths.append(new_path)
                content = read_file_formatted(new_path if new_path else path)
                insert_function(con, content)
                return 'Erfolgreich hinzugefügt!'
        finally:
            for path in file_paths:
                os.remove(path)
            con.close()

    @api.get('/read_data', status_code=status.HTTP_200_OK)
    def read_data(date: Date = Depends(), sensor_info: SensorInfo = Depends()):
        match sensor_info.type:
            case 'sds011':
                query = 'select * from "ParticulateMatterData" where ' \
                    f'sensor_id = \'{sensor_info.id}\' and sensor_type = \'{sensor_info.type}\''
            case 'dht22':
                query = 'select * from "WeatherData" where ' \
                    f'sensor_id = \'{sensor_info.id}\' and sensor_type = \'{sensor_info.type}\''
            case _:
                raise HTTPException(detail=f'Unknown sensor type: {sensor_info.type}',
                                    status_code=status.HTTP_400_BAD_REQUEST)
        con = connect_to_db(config)
        try:
            sensor_data = fetch_data(con, query)
            if not sensor_data:
                return JSONResponse(content='Keine Daten gefunden!',
                                    status_code=status.HTTP_404_NOT_FOUND)
            return filter_sensor_data(sensor_data, date)
        finally:
            con.close()

    @api.post('/test_connection')
    def testing_database():
        connection = connect_to_db(config)
        connection.close()

    @api.get('/filter_temperature')
    def get_temperature(date: Date = Depends(),
                        sensor_info: SensorInfo = Depends(),
                        query_filter: int = 0):
        if sensor_info.type != 'dht22':
            raise HTTPException(detail='Aktuell wird nur dht22 unterstützt!',
                                status_code=status.HTTP_400_BAD_REQUEST)
        if query_filter not in filter_map:
            raise HTTPException(detail='0 = min, 1 = avg, 2 = max',
                                status_code=status.HTTP_400_BAD_REQUEST)
        connection = connect_to_db(config)
        try:
            statement = f'select {filter_map[query_filter]}(temperature) from "WeatherData" ' \
                        f'where sensor_type = \'{sensor_info.type}\' '\
                        f'and sensor_id = \'{sensor_info.id}\' ' \
                        f'and date(timestamp) = \'{date.year}-{date.month}-{date.day}\''
            return round(fetch_data(connection, statement)[0][0], 2)
        finally:
            connection.close()

    return api


if __name__ == '__main__':
    arguments = get_arguments()
    uvicorn.run('main:main',
                factory=True,
                host='0.0.0.0',
                port=9090,
                reload=arguments.develop)
