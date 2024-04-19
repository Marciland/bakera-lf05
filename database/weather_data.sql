CREATE TABLE IF NOT EXISTS public."WeatherData" (
    id serial NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    temperature numeric NOT NULL,
    humidity numeric NOT NULL,
    sensor_id numeric NOT NULL,
    sensor_type text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "WeatherData_pkey" PRIMARY KEY (id),
    CONSTRAINT "WeatherData_sensor_id_sensor_type_fkey" FOREIGN KEY (sensor_id, sensor_type) REFERENCES public."Sensor" (sensor_id, sensor_type) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
) TABLESPACE pg_default;
ALTER TABLE IF EXISTS public."WeatherData" OWNER to admin;