CREATE TABLE IF NOT EXISTS public."WeatherData" (
    id serial NOT NULL,
    sensor_uuid uuid NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    temperature numeric NOT NULL,
    humidity numeric NOT NULL,
    CONSTRAINT "WeatherData_pkey" PRIMARY KEY (id),
    CONSTRAINT "WeatherData_sensor_uuid_fkey" FOREIGN KEY (sensor_uuid) REFERENCES public."Sensor" (uuid) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
) TABLESPACE pg_default;
ALTER TABLE IF EXISTS public."WeatherData" OWNER to admin;