'''downloader handles all file downloads'''
import os

import requests
from fastapi import HTTPException, status

from modules.data_models import Date
from modules.sensor_data import SensorInfo


def download_data(download_path: str, date: Date, sensor_info: SensorInfo) -> list[str]:
    '''
    Downloads data based on date given. Returns all paths to downloaded files.
    '''
    if date.day:
        file_path = download_day(download_path,
                                 date.year, date.month, date.day,
                                 sensor_info)
        file_paths = [file_path]
    elif date.month:
        file_paths = download_month(download_path,
                                    date.year, date.month,
                                    sensor_info)
    else:
        file_paths = download_year(download_path,
                                   date.year,
                                   sensor_info)
    if not file_paths or file_paths.count(None) == len(file_paths):
        raise HTTPException(detail=f'Failed to download: {date.year}/{date.month}/{date.day}'
                            f' for {sensor_info.type}-{sensor_info.id}',
                            status_code=status.HTTP_404_NOT_FOUND)
    return file_paths


def download_file(base_path: str, url: str, file_name: str) -> str:
    '''Downloads a single file to the base_path.'''
    base_url = 'https://archive.sensor.community/2022/'
    uri = base_url + url + file_name
    response = requests.get(url=uri, timeout=10)
    full_path = os.path.join(base_path, file_name)
    if response.status_code == 404:
        response = requests.get(url=uri + '.gz', timeout=10)
        full_path += '.gz'
    if response.status_code != 200:
        return None
    with open(full_path, 'wb') as file_handle:
        file_handle.write(response.content)
    return full_path


def download_day(download_path: str, year: int, month: int, day: int,
                 sensor_info: SensorInfo) -> str:
    '''
    Downloads sensor data based on type and id for given day to download_path.
    '''
    url = f'{year}-{month:02d}-{day:02d}/'
    file_name = f'{year}-{month:02d}-{day:02d}_{sensor_info.type}_sensor_{sensor_info.id}.csv'
    return download_file(download_path, url, file_name)


def download_month(download_path: str, year: int, month: int, sensor_info: SensorInfo) -> str:
    '''
    Downloads sensor data based on type and id for given month to download_path.
    '''
    file_paths = []
    for day in range(1, 32):
        file_paths.append(download_day(download_path,
                                       year, month, day,
                                       sensor_info))
    return file_paths


def download_year(download_path: str, year: int, sensor_info: SensorInfo) -> str:
    '''
    Downloads sensor data based on type and id for given year to download_path.
    '''
    file_paths = []
    for month in range(1, 13):
        file_paths.append(download_month(download_path,
                                         year, month,
                                         sensor_info))
    return file_paths
