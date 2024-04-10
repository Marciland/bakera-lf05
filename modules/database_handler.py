'''database handling like inserting data'''
import psycopg
from psycopg import Connection


def fetch_data(con: Connection, query: str) -> list:
    '''
    Reads based on query and returns data.
    '''
    cur = con.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    return rows


def connect_to_db(config: dict, commit: bool = False) -> Connection:
    '''
    Creates and returns a session in the database.
    '''
    return psycopg.connect(host=config['hostName'],
                           dbname=config['nameDB'],
                           user=config['userDB'],
                           password=config['passwordDB'],
                           autocommit=commit)
