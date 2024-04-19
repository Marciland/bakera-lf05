'''SQL Statements used in database interactions.'''

SDS011_READ = 'select * from "ParticulateMatterData" ' \
    'where sensor_id = \'%s\' and sensor_type = \'%s\''
DHT22_READ = 'select * from "WeatherData" ' \
    'where sensor_id = \'%s\' and sensor_type = \'%s\''
DHT22_READ_FILTERED = 'select %s(%s) from "WeatherData" ' \
    'where sensor_type = \'%s\' '\
    'and sensor_id = \'%s\' ' \
    'and date(timestamp) = \'%s-%s-%s\''
SDS011_READ_FILTERED = 'select %s("%s") from "ParticulateMatterData" ' \
    'where sensor_type = \'%s\' '\
    'and sensor_id = \'%s\' ' \
    'and date(timestamp) = \'%s-%s-%s\''
SDS011_WRITE = 'insert into "ParticulateMatterData" ' \
    '("timestamp", "P1", "durP1", "ratioP1", ' \
    '"P2", "durP2", "ratioP2", "sensor_id", "sensor_type") ' \
    'select %s,%s,%s,%s,%s,%s,%s,%s,%s ' \
    'where not exists ( select * from "ParticulateMatterData" ' \
    'where timestamp = %s and sensor_id = %s and sensor_type = %s)'
DHT22_WRITE = 'insert into "WeatherData" ' \
    '("timestamp", "temperature", "humidity", ' \
    '"sensor_id", "sensor_type") ' \
    'select %s,%s,%s,%s,%s ' \
    'where not exists (select * from "WeatherData" ' \
    'where timestamp = %s and sensor_id = %s and sensor_type = %s)'
