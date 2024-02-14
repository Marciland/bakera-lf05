'''database handling like inserting data'''
from psycopg import Connection
import psycopg
from uuid import uuid4


def insert_data_into_db(connection: Connection, tablename: str, file_data: list[list]) -> None:
    # sensor_id;
    # sensor_type;
    # location;
    # lat;
    # lon;
    # timestamp;
    # P1;
    # durP1;
    # ratioP1;
    # P2;
    # durP2;
    # ratioP2
    pass


def connect_to_db(config: dict) -> Connection:
    '''
    Creates and returns a session in the database.
    '''
    return psycopg.connect(host=config['hostName'],
                           dbname=config['nameDB'],
                           user=config['userDB'],
                           password=config['passwordDB'])


def create_sensor_info(connection: Connection, sensor_type: str, sensor_id: int, sensor_info: list):
    cursor = connection.cursor()
    cursor.execute('insert into public."Sensor" (uuid, sensor_id, sensor_type, latitude, longitude, location) values (%s, %s, %s, %s, %s, %s)', (uuid4(), sensor_id, sensor_type, ..., ..., ...))


