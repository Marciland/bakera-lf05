'''downloader handles all file downloads'''
import multiprocessing
import os

import requests


def download_file(base_path: str, url: str, filename: str) -> str:
    '''Downloads a single file to the base_path.'''
    base_url = 'https://archive.sensor.community/2022/'
    uri = base_url + url + filename
    response = requests.get(url=uri, timeout=10)
    full_path = os.path.join(base_path, filename)
    if response.status_code == 404:
        response = requests.get(url=uri + '.gz', timeout=10)
        full_path += '.gz'
    if response.status_code != 200:
        return None
    with open(full_path, 'wb') as file_handle:
        file_handle.write(response.content)
    return full_path


def download_sensor_files(base_path: str, sensor_type: str, sensor_id: int):
    '''Download all files for a given sensor.'''
    file_paths = []
    starmap = []
    for month in range(1, 2): # TODO undo
        for day in range(1, 32):
            starmap.append((base_path,
                            f'2022-{month:02d}-{day:02d}/',
                            f'2022-{month:02d}-{day:02d}_{sensor_type}_sensor_{sensor_id}.csv'))
    with multiprocessing.Pool() as pool:
        file_paths = pool.starmap(download_file, starmap)
    return file_paths


def download_all_files(sensor_types: dict, base_path: str) -> list[str]:
    '''
    Downloads all files necessary for the database content.
    Returns a list of file_paths for all files downloaded.
    '''
    if not os.path.exists(base_path):
        raise FileNotFoundError('base_path does not exist')
    file_paths = []
    for sensor_type, sensor_id in sensor_types.items():
        file_paths += download_sensor_files(base_path,
                                             sensor_type,
                                             sensor_id)
    return file_paths
