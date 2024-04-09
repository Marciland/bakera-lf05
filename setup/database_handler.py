'''database handling like inserting data'''
import psycopg
from psycopg import Connection


def insert_data_into_db(con: Connection, file_data: list[list[str]], sensor_types: list[str]) -> None:
    sensor_type = file_data[0][1]
    if sensor_type == sensor_types[0]:
        return insert_sds011(con, file_data)
    if sensor_type == sensor_types[1]:
        return insert_dht22(con, file_data)
    raise NotImplementedError()


def insert_sds011(con: Connection, file_data: list[list[str]]) -> None:
    for line in file_data:
        sensor_id = line[0]
        sensor_type = line[1]
        location = line[2]
        lat = line[3]
        lon = line[4]
        timestamp = line[5]
        p1 = line[6]
        durP1 = line[7]
        ratioP1 = line[8]
        p2 = line[9]
        durP2 = line[10]
        ratioP2 = line[11]


def insert_dht22(con: Connection, file_data: list[list[str]]) -> None:
    for line in file_data:
        sensor_id = line[0]
        sensor_type = line[1]
        location = line[2]
        lat = line[3]
        lon = line[4]
        timestamp = line[5]
        temperature = line[6]
        humidity = line[7]


def connect_to_db(config: dict) -> Connection:
    '''
    Creates and returns a session in the database.
    '''
    return psycopg.connect(host=config['hostName'],
                           dbname=config['nameDB'],
                           user=config['userDB'],
                           password=config['passwordDB'])


def create_sensor_info(con: Connection, sensor_type: str, sensor_id: int, sensor_info: list):
    '''
    Insert sensor data into the database.
    '''
    cursor = con.cursor()
    cursor.execute('insert into public."Sensor" '
                   '(sensor_id, sensor_type, latitude, longitude, location) '
                   'values (%s, %s, %s, %s, %s, %s)',
                   (sensor_id, sensor_type, sensor_info[3], sensor_info[4], sensor_info[2]))
