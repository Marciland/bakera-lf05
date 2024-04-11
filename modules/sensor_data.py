'''Handling sensor data.'''
from typing import Callable

from fastapi import HTTPException, status
from psycopg import Connection, Cursor
from pydantic import BaseModel

from modules.data_models import Date


class SensorInfo(BaseModel):
    '''
    Necessary information about a sensor.
    '''
    type: str = 'dht22'
    id: int = 3660


class Sds011Data(BaseModel):
    '''
    Database content for a sds011 sensor.
    '''
    timestamp: str
    p1: str | int
    dur_p1: str | int
    ratio_p1: str | int
    p2: str | int
    dur_p2: str | int
    ratio_p2: str | int
    sensor_info: SensorInfo
    insert_query: str = 'insert into "ParticulateMatterData" ' \
        '("timestamp", "P1", "durP1", "ratioP1", ' \
        '"P2", "durP2", "ratioP2", "sensor_id", "sensor_type") '\
        'values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'

    def get_insert_data(self) -> tuple:
        '''
        Generates a tuple needed for database transaction.
        '''
        return (str(self.timestamp),
                str(self.p1), str(self.dur_p1), str(self.ratio_p1),
                str(self.p2), str(self.dur_p2), str(self.ratio_p2),
                str(self.sensor_info.id), str(self.sensor_info.type),)


class Dht22Data(BaseModel):
    '''
    Database content for a dht22 sensor.
    '''
    timestamp: str
    temperature: str | int
    humidity: str | int
    sensor_info: SensorInfo
    insert_query: str = 'insert into "WeatherData" ' \
        '("timestamp", "temperature", "humidity", ' \
        '"sensor_id", "sensor_type") '\
        'values (%s,%s,%s,%s,%s)'

    def get_insert_data(self) -> tuple:
        '''
        Generates a tuple needed for database transaction.
        '''
        return (str(self.timestamp),
                str(self.temperature), str(self.humidity),
                str(self.sensor_info.id), str(self.sensor_info.type),)


def filter_sensor_data(sensor_data: list, date: Date) -> dict:
    '''
    Returns only entries based on filter.
    '''
    if date.day:
        return filter_day(sensor_data, date)
    if date.month:
        return filter_month(sensor_data, date)
    return filter_year(sensor_data, date)


def filter_day(sensor_data: list, date: Date) -> dict:
    '''
    Returns all entries matching day/month/year.
    '''
    filtered_data = {}
    for entry in sensor_data:
        timestamp = entry[1]
        if timestamp.day != date.day:
            continue
        if timestamp.month != date.month:
            continue
        if timestamp.year != date.year:
            continue
        filtered_data.update({entry[0]: format_entry(entry)})
    return filtered_data


def filter_month(sensor_data: list, date: Date) -> dict:
    '''
    Returns all entries matching month/year.
    '''
    filtered_data = {}
    for entry in sensor_data:
        timestamp = entry[1]
        if timestamp.month != date.month:
            continue
        if timestamp.year != date.year:
            continue
        filtered_data.update({entry[0]: format_entry(entry)})
    return filtered_data


def filter_year(sensor_data: list, date: Date) -> dict:
    '''
    Returns all entries matching year.
    '''
    filtered_data = {}
    for entry in sensor_data:
        timestamp = entry[1]
        if timestamp.year != date.year:
            continue
        filtered_data.update({entry[0]: format_entry(entry)})
    return filtered_data


def format_entry(entry: list) -> dict:
    '''
    Beautifies the database entry.
    sds011 has an entry length of 10.
    dht22 has an entry length of 6.
    '''
    if len(entry) == 10:
        return format_sds011(entry)
    if len(entry) == 6:
        return format_dht22(entry)
    raise NotImplementedError()


def format_sds011(entry: list) -> dict:
    '''
    Beatify database entry.
    '''
    return {
        'timestamp': entry[1],
        'P1': entry[2],
        'durP1': entry[3],
        'ratioP1': entry[4],
        'P2': entry[5],
        'durP2': entry[6],
        'ratioP2': entry[7]
    }


def format_dht22(entry: list) -> dict:
    '''
    Beatify database entry.
    '''
    return {
        'timestamp': entry[1],
        'temperature': entry[2],
        'humidity': entry[3]
    }


def get_sensor_function(sensor_type: str) -> Callable:
    '''
    Returns a function callable based on type if type is valid.
    '''
    match sensor_type:
        case 'sds011':
            insert_function = add_sds011_data
        case 'dht22':
            insert_function = add_dht22_data
        case _:
            raise HTTPException(detail=f'Unknown sensor type: {sensor_type}',
                                status_code=status.HTTP_400_BAD_REQUEST)
    return insert_function


def add_sds011_data(con: Connection, file_data: list[list[str]]) -> None:
    '''
    Inserts into ParticulateMatterData due to sensor type being sds011.
    '''
    cur = con.cursor()
    for line in file_data:
        data = Sds011Data(timestamp=line[5],
                          p1=line[6] if line[6] else 0,
                          dur_p1=line[7] if line[7] else 0,
                          ratio_p1=line[8] if line[8] else 0,
                          p2=line[9] if line[9] else 0,
                          dur_p2=line[10] if line[10] else 0,
                          ratio_p2=line[11] if line[11] else 0,
                          sensor_info=SensorInfo(id=line[0],
                                                 type=line[1].lower())
                          )
        insert_sensor_data(cur, data)
    cur.close()


def add_dht22_data(con: Connection, file_data: list[list[str]]) -> None:
    '''
    Inserts into WeatherData due to sensor type being dht22.
    '''
    cur = con.cursor()
    for line in file_data:
        data = Dht22Data(timestamp=line[5],
                         temperature=line[6] if line[6] else 0,
                         humidity=line[7] if line[7] else 0,
                         sensor_info=SensorInfo(id=line[0],
                                                type=line[1].lower()))
        insert_sensor_data(cur, data)
    cur.close()


def insert_sensor_data(cur: Cursor, data: BaseModel) -> None:
    '''
    Generic data insertion for any sensor model.
    '''
    cur.execute(data.insert_query, data.get_insert_data())
